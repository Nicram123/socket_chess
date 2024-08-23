import pygame
import sys
WIDTH, HEIGHT = 600, 600

ROWS, COLS = 8, 8

SQUARE_SIZE = WIDTH // ROWS

position = (WIDTH // 2, HEIGHT // 2)

GREEN = (118, 150, 86)
WHITE = (238, 238, 210)
WHITE2 = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# pasek prommowania 

# Stałe
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
PROMOTION_MENU_WIDTH = 100
PROMOTION_MENU_HEIGHT = 400
PIECE_SIZE = 50
MARGIN = 0

# Kolory
BACKGROUND_COLOR = (255, 255, 255)
BUTTON_COLOR = (200, 200, 200)
HOVER_COLOR = (150, 150, 150)

# Inicjalizacja ekranu
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Załaduj obrazy pionków
queen_img = pygame.image.load('bqueen.jpg')
rook_img = pygame.image.load('brook.jpg')
bishop_img = pygame.image.load('bbish.jpg')
knight_img = pygame.image.load('bknight.jpg')

# Skalowanie obrazów
queen_img = pygame.transform.scale(queen_img, (PIECE_SIZE, PIECE_SIZE))
rook_img = pygame.transform.scale(rook_img, (PIECE_SIZE, PIECE_SIZE))
bishop_img = pygame.transform.scale(bishop_img, (PIECE_SIZE, PIECE_SIZE))
knight_img = pygame.transform.scale(knight_img, (PIECE_SIZE, PIECE_SIZE))