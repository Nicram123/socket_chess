import pygame
from constants import BLACK, ROWS, COLS, SQUARE_SIZE, WHITE, WHITE2, GREEN, RED, position
import math as m
from figure import Pawn, King, Knight, Bishop, Queen, Rook

class Board:
  PADDING = 10
  
  
  
  def __init__(self):
    self.board = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
        ]
    self.IMAGES = self.load_images()
    self.pieces = self.initialize_pieces()
    

  
  def repeat_manual_deepcopy(self, new_board):
      new_board.board = [ row[:] for row in self.board ]  
      new_board.pieces = { k: {'type': v['type'], 'obj': v['obj'], 'image': v['image']} for k, v in self.pieces.items() }
      return new_board
  
  

  def draw_text_centered(self, screen, color):
    text = f'WIN : {color}' 
    font = pygame.font.SysFont('Arial', 72)  
    text_surface = font.render(text, True, RED)
    text_rect = text_surface.get_rect(center=position)
    screen.blit(text_surface, text_rect)
    
  def manual_deepcopy(self):
        new_board = Board()
        new_board.board = [ row[:] for row in self.board ]  # Głęboka kopia listy list
        new_board.pieces = { k: {'type': v['type'], 'obj': v['obj'], 'image': v['image']} for k, v in self.pieces.items() }
        return new_board

  def draw_pieces(self, win):
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece:
                    win.blit(self.pieces[(row, col)]['image'], (col * SQUARE_SIZE, row * SQUARE_SIZE))
    
  def return_figure_obj(self, curr_pos_x, curr_pos_y):
    x, y = self.return_xy(curr_pos_x, curr_pos_y)
    if (y, x) in self.pieces:
      return self.pieces[(y, x)]['obj']
    return None
  
  def return_xy(self, curr_pos_x, curr_pos_y):
    return curr_pos_x // SQUARE_SIZE, curr_pos_y // SQUARE_SIZE
  
  def load_images(self):
      pieces = ['bB', 'bK', 'bN', 'bP', 'bQ', 'bR', 'wB', 'wK', 'wN', 'wP', 'wQ', 'wR']
      images = {}
      for piece in pieces:
          image = pygame.image.load(f'{piece}.png').convert_alpha() # objekty obsługują przezroczystość - convert_alpha()
          image.set_colorkey(WHITE)  # Ustawienie białego tła jako przezroczyste
          images[piece] = image
      return images
    
  def initialize_pieces(self):
        pieces = {}
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                obj = self.create_figure_obj(piece)
                if piece:
                    pieces[(row, col)] = {'image': self.IMAGES[piece], 'type': piece, 'obj': obj}
        return pieces
      
  def create_figure_obj(self, piece):
    #'bR', 'bN', 'bB', 'bQ', 'bK', 'bP'
    if piece:
            color = 'black' if piece[0] == 'b' else 'white'
            if piece[1] == 'R':
                return Rook(color)
            elif piece[1] == 'N':
                return Knight(color)
            elif piece[1] == 'B':
                return Bishop(color)
            elif piece[1] == 'Q':
                return Queen(color)
            elif piece[1] == 'K':
                return King(color)
            elif piece[1] == 'P':
                return Pawn(color)
  
  def draw_squares(self,win):
    win.fill(WHITE)
    for row in range(ROWS):
        for col in range(row % 2, ROWS, 2):
           pygame.draw.rect(win,GREEN,(row*SQUARE_SIZE,col*SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE))

  def draw(self,win):
     self.draw_squares(win)
     
  
   
  
  
  
              
              