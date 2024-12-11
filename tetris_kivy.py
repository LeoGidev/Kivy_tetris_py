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
        self.current_pos = [0, 4]  # Inicialmente arriba y centrado
        self.game_over = False

        # Eventos de teclado
        Window.bind(on_key_down=self.on_key_down)

        # Actualización periódica
        Clock.schedule_interval(self.update, 0.5)  # Cada 0.5 segundos

        self.start_new_piece()

    def start_new_piece(self):
        """Generar una nueva pieza"""
        self.current_piece = random.choice(list(SHAPES.values()))
        self.current_pos = [0, 4]

        if self.check_collision(self.current_piece, self.current_pos):
            self.game_over = True
            print("Game Over!")