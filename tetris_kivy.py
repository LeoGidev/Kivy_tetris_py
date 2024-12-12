from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
from kivy.clock import Clock
from kivy.core.window import Window
import random

# Configuración del tablero
GRID_SIZE = 20  # Tamaño de cada celda
BOARD_WIDTH = 10
BOARD_HEIGHT = 20

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
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.board = [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        self.current_piece = None
        self.current_pos = [0, 4]
        self.game_over = False

        self.lines_cleared = 0  # Líneas eliminadas
        self.level = 1  # Nivel inicial
        self.speed = 0.5  # Velocidad inicial (segundos entre actualizaciones)

        # Eventos de teclado
        Window.bind(on_key_down=self.on_key_down)

        # Actualización periódica
        Clock.schedule_interval(self.update, self.speed)

        self.start_new_piece()

    def start_new_piece(self):
        """Generar una nueva pieza"""
        self.current_piece = random.choice(list(SHAPES.values()))
        self.current_pos = [0, 4]

        if self.check_collision(self.current_piece, self.current_pos):
            self.game_over = True
            print("Game Over!")

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
        """Elimina filas completas del tablero y actualiza el nivel"""
        cleared = 0
        new_board = [row for row in self.board if any(cell == 0 for cell in row)]
        cleared = BOARD_HEIGHT - len(new_board)
        while len(new_board) < BOARD_HEIGHT:
            new_board.insert(0, [0 for _ in range(BOARD_WIDTH)])
        self.board = new_board

        self.lines_cleared += cleared
        if cleared > 0:
            print(f"Líneas eliminadas: {self.lines_cleared}")
            self.update_level()



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

    def on_key_down(self, instance, key, *args):
        """Control de teclado"""
        if self.game_over:
            return
        if key == 276:  # Flecha izquierda
            self.move_piece(-1, 0)
        elif key == 275:  # Flecha derecha
            self.move_piece(1, 0)
        elif key == 274:  # Flecha abajo
            self.move_piece(0, 1)
        elif key == 273:  # Flecha arriba
            self.rotate_piece()

    def update(self, dt):
        """Actualización periódica del juego"""
        if self.game_over:
            return
        if not self.check_collision(self.current_piece, [self.current_pos[0] + 1, self.current_pos[1]]):
            self.current_pos[0] += 1
        else:
            self.place_piece()
        self.draw_board()

    def draw_board(self):
        """Dibuja el tablero y la pieza actual"""
        self.canvas.clear()
        with self.canvas:
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

class TetrisApp(App):
    def build(self):
        return TetrisGame()

if __name__ == '__main__':
    TetrisApp().run()
