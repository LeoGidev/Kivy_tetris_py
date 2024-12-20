from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
import random
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window

Window.size = (600, 800)  # Define el tamaño de la ventana principal

# Configuración del tablero
GRID_SIZE = 10  # Tamaño de cada celda


#BOARD_WIDTH = Window.size[0]
#BOARD_WIDTH = 10
#BOARD_HEIGHT = Window.size[1]
#BOARD_HEIGHT = 20
# Calcula BOARD_WIDTH y BOARD_HEIGHT dinámicamente
BOARD_WIDTH = Window.size[0] // GRID_SIZE
BOARD_HEIGHT = Window.size[1] // GRID_SIZE
#GRID_SIZE = min(Window.size[0] // BOARD_WIDTH, Window.size[1] // BOARD_HEIGHT)

# Formas de las piezas (Tetrominós)
SHAPES = {
    'I': [[1, 1, 1, 1]],
    'O': [[1, 1], [1, 1]],
    'T': [[0, 1, 0], [1, 1, 1]],
    'S': [[0, 1, 1], [1, 1, 0]],
    'Z': [[1, 1, 0], [0, 1, 1]],
    'J': [[1, 0, 0], [1, 1, 1]],
    'L': [[0, 0, 1], [1, 1, 1]]
}

class TetrisGame(Widget):
    def __init__(self, score_label, level_label, next_piece_label, **kwargs):
        super().__init__(**kwargs)
        self.board = [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        self.current_piece = None
        self.current_pos = [0, 4]
        self.next_piece = random.choice(list(SHAPES.values()))
        self.game_over = False

        self.lines_cleared = 0  # Líneas eliminadas
        self.level = 1  # Nivel inicial
        self.speed = 0.5  # Velocidad inicial (segundos entre actualizaciones)
        self.score = 0  # Sistema de puntuación

        # Referencias a las etiquetas externas
        self.score_label = score_label
        self.level_label = level_label
        self.next_piece_label = next_piece_label  # Ahora se acepta correctamente

        # Eventos de teclado
        Window.bind(on_key_down=self.on_key_down)

        # Actualización periódica
        Clock.schedule_interval(self.update, self.speed)

        self.start_new_piece()


    def start_new_piece(self):
        """Generar una nueva pieza"""
        self.current_piece = self.next_piece
        self.next_piece = random.choice(list(SHAPES.values()))
        self.current_pos = [0, 4]
        # Actualiza la vista de la pieza siguiente
        self.update_next_piece_display()

        if self.check_collision(self.current_piece, self.current_pos):
            self.game_over = True
            print("Game Over!")
    
    def update_next_piece_display(self):
        """Actualiza la etiqueta con la representación de la siguiente pieza."""
        next_piece_text = "\n".join(
            "".join("[]" if cell else "  " for cell in row) for row in self.next_piece
        )
        self.next_piece_label.text = f"Next:\n{next_piece_text}"

    def check_collision(self, piece, pos):
        """Verifica si una pieza colisiona con los bordes o con otras piezas"""
        for y, row in enumerate(piece):
            for x, cell in enumerate(row):
                if cell:
                    new_x = pos[1] + x
                    new_y = pos[0] + y
                    if (new_x < 0 or new_x >= BOARD_WIDTH or
                        new_y >= BOARD_HEIGHT or
                        (new_y >= 0 and self.board[new_y][new_x])):
                        return True
        return False

    def place_piece(self):
        """Coloca la pieza en el tablero y elimina filas completas"""
        for y, row in enumerate(self.current_piece):
            for x, cell in enumerate(row):
                if cell:
                    self.board[self.current_pos[0] + y][self.current_pos[1] + x] = 1
        self.clear_lines()
        self.start_new_piece()

    def clear_lines(self):
        """Elimina filas completas del tablero y actualiza el nivel y la puntuación"""
        new_board = [row for row in self.board if any(cell == 0 for cell in row)]
        cleared = BOARD_HEIGHT - len(new_board)
        while len(new_board) < BOARD_HEIGHT:
            new_board.insert(0, [0 for _ in range(BOARD_WIDTH)])
        self.board = new_board

        self.lines_cleared += cleared
        if cleared > 0:
            self.score += (cleared ** 2) * 100  # Incrementar puntuación según las líneas eliminadas
            self.score_label.text = f"Score: {self.score}"
            print(f"Líneas eliminadas: {self.lines_cleared}, Score: {self.score}")
            self.update_level()

    def update_level(self):
        """Aumenta el nivel y ajusta la velocidad"""
        new_level = self.lines_cleared // 10 + 1  # Subir nivel cada 10 líneas
        if new_level > self.level:
            self.level = new_level
            self.speed = max(0.1, self.speed - 0.05)  # Reducir velocidad (límites)
            Clock.unschedule(self.update)
            Clock.schedule_interval(self.update, self.speed)
            self.level_label.text = f"Level: {self.level}"
            print(f"Nivel: {self.level}, Velocidad: {self.speed:.2f}s")

    def move_piece(self, dx, dy):
        """Mueve la pieza actual"""
        new_pos = [self.current_pos[0] + dy, self.current_pos[1] + dx]
        if not self.check_collision(self.current_piece, new_pos):
            self.current_pos = new_pos

    def rotate_piece(self):
        """Rota la pieza actual"""
        new_piece = [list(row) for row in zip(*self.current_piece[::-1])]
        if not self.check_collision(new_piece, self.current_pos):
            self.current_piece = new_piece

    def on_key_down(self, window, key, scancode, codepoint, modifiers):
        if key == 276:  # Flecha izquierda
            self.move_left()
        elif key == 275:  # Flecha derecha
            self.move_right()
        elif key == 273:  # Flecha arriba
            self.rotate()
        elif key == 274:  # Flecha abajo
            self.move_down()

    def move_left(self):
        """Mueve la pieza a la izquierda."""
        self.move_piece(-1, 0)

    def move_right(self):
        """Mueve la pieza a la derecha."""
        self.move_piece(1, 0)

    def move_down(self):
        """Mueve la pieza hacia abajo más rápido."""
        self.move_piece(0, 1)

    def rotate(self):
        """Rota la pieza actual."""
        self.rotate_piece()

    def update(self, dt):
        """Actualización periódica del juego"""
        if self.game_over:
            self.show_game_over()
            return
        if not self.check_collision(self.current_piece, [self.current_pos[0] + 1, self.current_pos[1]]):
            self.current_pos[0] += 1
        else:
            self.place_piece()
        self.draw_board()

    def draw_board(self):
        """Dibuja el tablero, la pieza actual y la siguiente pieza"""
        self.canvas.clear()
        with self.canvas:
            # Fondo del área del juego
            Color(0.1, 0.2, 0.2)
            Rectangle(pos=(0, 0), size=(BOARD_WIDTH * GRID_SIZE, BOARD_HEIGHT * GRID_SIZE))
            #Rectangle(pos=(0, 0), size=(Window.size))

            # Dibuja las piezas fijas en el tablero
            for y, row in enumerate(self.board):
                for x, cell in enumerate(row):
                    if cell:
                        Color(0, 1, 0)
                        Rectangle(pos=(x * GRID_SIZE, (BOARD_HEIGHT - y - 1) * GRID_SIZE),
                                  size=(GRID_SIZE, GRID_SIZE))

            # Dibuja la pieza actual
            for y, row in enumerate(self.current_piece):
                for x, cell in enumerate(row):
                    if cell:
                        Color(1, 0, 0)
                        Rectangle(pos=((self.current_pos[1] + x) * GRID_SIZE,
                                       (BOARD_HEIGHT - self.current_pos[0] - y - 1) * GRID_SIZE),
                                  size=(GRID_SIZE, GRID_SIZE))
    
    def show_game_over(self):
        """Muestra el texto de Game Over"""
        self.canvas.clear()
        with self.canvas:
            Color(1, 0, 0, 1)  # Color rojo
            Rectangle(pos=(0, 0), size=Window.size)
        self.add_widget(Label(text="GAME OVER", font_size=48, color=(1, 1, 1, 1), pos=Window.center))



class TetrisApp(App):
    def build(self):
        root = FloatLayout()
        
        info_panel = BoxLayout(orientation='vertical', size_hint=(0.3, 1), pos_hint={"right": 1})
        with info_panel.canvas.before:
            Color(0.1, 0.1, 0.1, 1)
            rect = Rectangle()

        def update_rect(instance, value):
            rect.pos = instance.pos
            rect.size = instance.size

        info_panel.bind(pos=update_rect, size=update_rect)

        score_label = Label(text="Score: 0", font_size=20, color=(1, 1, 0, 1))
        level_label = Label(text="Level: 1", font_size=20, color=(1, 1, 0, 1))
        next_piece_label = Label(text="Next:\n", font_size=20, color=(1, 1, 0, 1), halign="left", valign="middle")
        next_piece_label.text_size = next_piece_label.size

        info_panel.add_widget(score_label)
        info_panel.add_widget(level_label)
        info_panel.add_widget(next_piece_label)  # Añade la etiqueta al panel de información

        game_area = BoxLayout()
        with game_area.canvas.before:
            Color(1, 0, 0, 1)  # Color rojo
            Rectangle(pos=(0, 0), size=(600, 800))


    

        tetris_game = TetrisGame(score_label, level_label, next_piece_label)  # Pasa la etiqueta

        game_area.add_widget(tetris_game)

        root.add_widget(game_area)
        root.add_widget(info_panel)

        return root



        


if __name__ == '__main__':
    TetrisApp().run()
