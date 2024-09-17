import pygame
from constants import position, BLACK, ROWS, COLS, SQUARE_SIZE, WHITE, WHITE2, GREEN, RED, SCREEN_WIDTH, PROMOTION_MENU_WIDTH, SCREEN_HEIGHT, PROMOTION_MENU_HEIGHT, PIECE_SIZE, MARGIN, queen_img, rook_img, bishop_img, knight_img
import copy


class Figure():
  PADDING = 12
  only_one_can_be_destroyed = 0
  changingThePawnAuthorityFlag = False
  options = {}
  end = False
  winColor = None
  
  def __init__(self, color):
    self.color = color 
    self.changingThePawnAuthorityFlagNoMoreThanOne = 1
    self.number_of_mov = 0
    self.new_board = None # haloo 
    
    
    

    if self.color == 'white':
      self.direction = 1 
    else:
      self.direction = -1
      
  def oppositeColor(self, colr):
    if colr[0] == 'w':
      colr = 'black'
    else:
      colr = 'white'
    return colr
  
  def escapeFromTheIsInCheck(self, win, board, flag, curr_pos_x, curr_pos_y, moves):
    movesTemp = copy.copy(moves)
    for x, y in moves:
      if ( (x, y) != (curr_pos_x, curr_pos_y) and self.isEscapeFromTheIsInCheck(win, board, flag, (x, y), (curr_pos_x, curr_pos_y)) 
          or (x, y) != (curr_pos_x, curr_pos_y) and self.check_in_on_yourself(board, win,  curr_pos_x, curr_pos_y, x, y) ): # 
        element_to_remove = (x, y)
        movesTemp.remove(element_to_remove)
      elif (x, y) != (curr_pos_x, curr_pos_y):
          self.drawRedCircle(win, x, y)     
    moves = movesTemp
    return moves
  
  def check_in_on_yourself(self, board, win,  curr_pos_x, curr_pos_y, new_row, new_col):
    colr = self.color[:]  
    moveFrom = (curr_pos_x, curr_pos_y)
    moveTo = (new_row, new_col)
    simulated_board = self.simulate_move(board, moveTo, moveFrom)
    if self.is_in_check(simulated_board, win, colr, False) : 
      return True
    return False
  
      
  def changingThePawnAuthority(self, mouseX, mouseY, board, win, figure):
    obj = None
    col = 'b'
    x = figure.options['x']
    y = figure.options['y'] 
    
    if self.color == 'black':
       col = 'w'
    for option, img, pos in figure.options['opts']:
      
      rect = pygame.Rect(pos[0], pos[1], PIECE_SIZE, PIECE_SIZE)
      x1, y1 = pos[0] + PIECE_SIZE, pos[1] + PIECE_SIZE
      if pos[0] < mouseX < x1 and pos[1] < mouseY < y1:
        if option == 'queen':
          obj = Queen(col)
          obj.changingThePawnAuthorityFlagNoMoreThanOne = 0
          img = col + 'Q' + '.png'
          img = pygame.image.load(f'{img}').convert_alpha()
          typ = col + 'Q'
          board.board[y][x] = typ
          del board.pieces[(y, x)] 
          board.pieces[(y, x)] = {'obj': obj, 'image': img, 'type': typ}
          break
        elif option == 'rook':
          obj = Rook(col)
          obj.changingThePawnAuthorityFlagNoMoreThanOne = 0
          img = col + 'R' + '.png'
          img = pygame.image.load(f'{img}').convert_alpha()
          typ = col + 'R'
          board.board[y][x] = typ
          del board.pieces[(y, x)] 
          board.pieces[(y, x)] = {'obj': obj, 'image': img, 'type': typ} 
          break  
        elif option == 'bishop':
          obj = Bishop(col)
          obj.changingThePawnAuthorityFlagNoMoreThanOne = 0
          img = col + 'B' + '.png' 
          img = pygame.image.load(f'{img}').convert_alpha()
          typ = col + 'B'
          board.board[y][x] = typ
          del board.pieces[(y, x)] 
          board.pieces[(y, x)] = {'obj': obj, 'image': img, 'type': typ}
          break
        elif option == 'knight':
          obj = Knight(col)
          obj.changingThePawnAuthorityFlagNoMoreThanOne = 0
          img = col + 'N' + '.png'
          img = pygame.image.load(f'{img}').convert_alpha()
          typ = col + 'N' 
          board.board[y][x] = typ
          del board.pieces[(y, x)] 
          board.pieces[(y, x)] = {'obj': obj, 'image': img, 'type': typ}
          break
      else:
          obj = Queen(col)
          obj.changingThePawnAuthorityFlagNoMoreThanOne = 0
          img = col + 'Q' + '.png'
          img = pygame.image.load(f'{img}').convert_alpha()
          typ = col + 'Q'
          board.board[y][x] = typ
          board.pieces[(y, x)] = {'obj': obj, 'image': img, 'type': typ}
      figure.deselect_red_pieces(board, win)
      
  def ifCheckMateOccurs(self, board, win, figure):
    if self.is_checkmte(board, win): # mat 
      board.draw_text_centered(win, self.color)
      figure.end = True
      figure.winColor = self.color
 
  # Mat 
  
  def is_checkmte(self, board, win):
    colr = self.color[:]
    colr = self.oppositeColor(colr)
    if not self.is_in_check(board, win, colr, False):
      return False
    possible_moves = self.generate_all_attacking_moves_mte(win, board, colr[0])
    
    for item in possible_moves:
      for moveTo in item['to']:
        moveFrom = item['from']
        simulated_board = self.simulate_move(board, moveTo, moveFrom)
        if not self.is_in_check(simulated_board, win, colr, False):     
          return False
    return True   # mat 
  
  def generate_all_attacking_moves_mte(self, win, board, colr):
    moves = []
    for row in range(ROWS):
      for col in range(COLS):
        piece = board.board[row][col]
        if piece and self.color[0] != piece[0]: #  colr == piece[0]
          moves.append({'from':(col, row) , 'to': board.pieces[(row, col)]['obj'].generate_red_circle(win, col * SQUARE_SIZE, row * SQUARE_SIZE, board, False)})
    return moves
  
  
  def show_promotion_menu(self, screen, mouseX, mouseY, obj):
    if obj.color == 'black':
      square_size = -2.6 * SQUARE_SIZE
    else:
      square_size = SQUARE_SIZE
    menu_x = (mouseX * SQUARE_SIZE) 
    menu_y = (mouseY * SQUARE_SIZE + square_size)
    options = [
        ('queen', queen_img, (menu_x, menu_y)), 
        ('rook', rook_img, (menu_x, menu_y + PIECE_SIZE + MARGIN)),
        ('bishop', bishop_img, (menu_x, menu_y + 2 * (PIECE_SIZE + MARGIN))),
        ('knight', knight_img, (menu_x, menu_y + 3 * (PIECE_SIZE + MARGIN)))
    ]
    for option, img, pos in options:
        screen.blit(img, pos)
    pygame.display.flip()
    self.changingThePawnAuthorityFlag = True
    return options
  
  def simulate_move(self, board, moveTo, moveFrom):
    if self.new_board == None:
      self.new_board = board.manual_deepcopy()
    else:
      self.new_board = board.repeat_manual_deepcopy(self.new_board)
    moveFrom = (moveFrom[1], moveFrom[0])
    moveTo = (moveTo[1], moveTo[0])
    temp = self.new_board.board[moveFrom[0]][moveFrom[1]]
    self.new_board.board[moveFrom[0]][moveFrom[1]] = None
    self.new_board.board[moveTo[0]][moveTo[1]] = temp
    obj = self.new_board.pieces[( moveFrom[0], moveFrom[1] )]['obj'] 
    img = self.new_board.pieces[( moveFrom[0], moveFrom[1] )]['image'] 
    typ = self.new_board.pieces[( moveFrom[0], moveFrom[1] )]['type']
    del self.new_board.pieces[( moveFrom[0], moveFrom[1] )] 
    self.new_board.pieces[( moveTo[0], moveTo[1] )] = {'obj': obj, 'image': img, 'type': typ}
    return self.new_board
  
  # Szach
  def is_in_check(self, board, win, colr, flag):              
    king_position = self.find_king_position(board, colr[0])    
    colr = self.oppositeColor(colr)
    opponent_moves = self.generate_all_attacking_moves(win, board, colr[0], flag)
    for item in opponent_moves:
      for move in item['to']:
        if self.move_targets(king_position, move):
          return True
    return False
  
  # escape 
  def isEscapeFromTheIsInCheck(self, win, board, flag, moveTo, moveFrom): 
    colr = self.color[:]
    if self.is_in_check(board, win, colr, False):
      simulated_board = self.simulate_move(board, moveTo, moveFrom)
      if self.is_in_check(simulated_board, win, colr, False):
        return True
      else:
        return False
    else:
      return False
  
  def generate_all_attacking_moves(self, win, board, colr, flag):
    moves = []
    for row in range(ROWS):
      for col in range(COLS):
        piece = board.board[row][col]
        if piece and colr == piece[0]: # 
          moves.append({'from':(row, col) , 'to': board.pieces[(row, col)]['obj'].generate_red_circle(win, col * SQUARE_SIZE, row * SQUARE_SIZE, board, flag)})
    return moves
  
  
  
  def move_targets(self, king_position, move):
    return king_position == move
  
  def find_king_position(self, board, colr):
    for row in range(ROWS):
      for col in range(COLS):
        piece = board.board[row][col]
        if piece and piece[1] == 'K' and colr == piece[0]: # self.color[0] != piece[0]
          return (col, row)
    return None
    
  
  def drawRedCircle(self, win, col, row):
    x, y = self.calc_pos(col, row)
    radius = SQUARE_SIZE//2 - self.PADDING * 2
    pygame.draw.circle(win, RED, (x,y), radius)
    
  def calc_pos(self, col, row):
    x = SQUARE_SIZE * col + SQUARE_SIZE // 2
    y = SQUARE_SIZE * row + SQUARE_SIZE // 2
    return x, y
  
  def return_xy(self, curr_pos_x, curr_pos_y):
    return curr_pos_x // SQUARE_SIZE, curr_pos_y // SQUARE_SIZE
  
  def deselect_red_pieces(self, board, win):
    board.draw(win)
    board.draw_pieces(win)
    
  def deselect(self, pos, mouseX, mouseY):
    mouseX, mouseY = self.return_xy(mouseX, mouseY)
    for x, y in pos:
      if mouseX == x and mouseY == y:
        return True
    return False
  
  def move(self, figure, pos, mouseX, mouseY, board, win):
    self.number_of_mov += 1
    mouseX, mouseY = figure.return_xy(mouseX, mouseY)
    typ = board.pieces[(pos[0][1], pos[0][0])]['type']
    board.board[pos[0][1]][pos[0][0]] = None  # Poprawiamy planszę
    board.board[mouseY][mouseX] = typ
    obj = board.pieces[(pos[0][1], pos[0][0])]['obj']
    img = board.pieces[(pos[0][1], pos[0][0])]['image']
    del board.pieces[(pos[0][1], pos[0][0])] 
    board.pieces[(mouseY, mouseX)] = {'obj': obj, 'image': img, 'type': typ} #Poprawiamy przypisanie
    figure.deselect_red_pieces(board, win)
    if ( ( mouseY == 0 or mouseY == 7 ) 
    and board.board[mouseY][mouseX] != None 
    and self.changingThePawnAuthorityFlagNoMoreThanOne != 0 
    and board.board[mouseY][mouseX][1] == 'P'):
          options = obj.show_promotion_menu(win, mouseX, mouseY, self)
          figure.options = { 'opts':options, 'x':mouseX, 'y':mouseY }
    self.ifCheckMateOccurs(board, win, figure)    
    
  def is_valid_position(self, new_row, new_col):
    return 0 <= new_row <= 7 and 0 <= new_col <= 7
  
  
    
  def is_valid(self, new_row, new_col, board, curr_pos_x, curr_pos_y):
    if (self.is_valid_position(new_row, new_col) 
        and board.board[new_col][new_row] is None 
         or self.is_valid_position(new_row, new_col) and board.board[new_col][new_row] is not None 
             and board.pieces[(new_col, new_row)]['obj'].color != board.pieces[(curr_pos_y, curr_pos_x)]['obj'].color):
      if board.board[new_col][new_row] is not None:
        self.only_one_can_be_destroyed += 1
      return True
    return False 
  
  def capturing_a_pawn(self, figure, win, board, mouseX, mouseY, mouseXtemp, mouseYtemp):  # zbicie pionka
    self.number_of_mov += 1
    typ = board.pieces[(mouseYtemp, mouseXtemp)]['type']
    obj = board.pieces[(mouseYtemp, mouseXtemp)]['obj']
    img = board.pieces[(mouseYtemp, mouseXtemp)]['image']
    board.board[mouseY][mouseX] = typ
    board.board[mouseYtemp][mouseXtemp] = None
    del board.pieces[(mouseYtemp, mouseXtemp)] 
    board.pieces[(mouseY, mouseX)] = {'obj': obj, 'image': img, 'type': typ}
    self.deselect_red_pieces(board, win)
    if ( ( mouseY == 0 or mouseY == 7 ) 
        and board.board[mouseY][mouseX] != None 
        and self.changingThePawnAuthorityFlagNoMoreThanOne != 0
        and board.board[mouseY][mouseX][1] == 'P'):
          options = figure.show_promotion_menu(win, mouseX, mouseY, self)
          figure.options = { 'opts':options, 'x':mouseX, 'y':mouseY }
    self.ifCheckMateOccurs(board, win, figure)
  
class Pawn(Figure): # pionek
  def __init__(self, color):
    super().__init__(color)
  
  def is_valid(self, new_row, new_col, board, curr_pos_x, curr_pos_y):
    if (self.is_valid_position(new_row, new_col) 
        and board.board[new_col][new_row] is None 
         ):
      return True
    return False 
    
  def show_red_circle(self, win, curr_pos_x, curr_pos_y, board, flag):
    x, y = self.return_xy(curr_pos_x, curr_pos_y)
    moves = [(x, y)]
    direction = self.direction
    if self.is_valid(x, y - direction, board, x, y):
        moves.append((x, y - direction))
        if self.number_of_mov == 0 and self.is_valid(x, y - 2 * direction, board, x, y):
            moves.append((x, y - 2 * direction))
    capture_directions = [(1, -direction), (-1, -direction)]
    for a, b in capture_directions:
        new_row, new_col = x + a, y + b
        if (self.is_valid_position(new_row, new_col)
            and board.board[new_col][new_row] is not None
            and board.pieces[(new_col, new_row)]['obj'].color != self.color):
            moves.append((new_row, new_col))
    return self.escapeFromTheIsInCheck(win, board, flag, x, y, moves)
    

  def generate_red_circle(self,win, curr_pos_x, curr_pos_y, board, flag):
    x, y = self.return_xy(curr_pos_x, curr_pos_y)
    moves = [(x, y)]
    direction = self.direction
    if self.is_valid(x, y - direction, board, x, y):
        moves.append((x, y - direction))
        if self.number_of_mov == 0 and self.is_valid(x, y - 2 * direction, board, x, y):
            moves.append((x, y - 2 * direction))
    capture_directions = [(1, -direction), (-1, -direction)]
    for a, b in capture_directions:
        new_row, new_col = x + a, y + b
        if (self.is_valid_position(new_row, new_col)
            and board.board[new_col][new_row] is not None
            and board.pieces[(new_col, new_row)]['obj'].color != self.color):
            moves.append((new_row, new_col))
    return moves
  

class Rook(Figure): # wieza
  def __init__(self, color):
    super().__init__(color)
    
  def show_red_circle(self,win,  curr_pos_x, curr_pos_y, board, flag):
    curr_pos_x, curr_pos_y = self.return_xy(curr_pos_x, curr_pos_y)
    moves = []
    moves.append((curr_pos_x, curr_pos_y))
    directions = [
      (0, 1), (0, -1), (-1, 0), (1, 0)
    ]
    for x, y in directions:
      new_row, new_col = curr_pos_x + x, curr_pos_y + y
      while self.only_one_can_be_destroyed != 1 and self.is_valid(new_row, new_col, board, curr_pos_x, curr_pos_y):  
        moves.append((new_row, new_col))    
        new_row, new_col = new_row + x, new_col + y  
      self.only_one_can_be_destroyed = 0
    return self.escapeFromTheIsInCheck(win, board, flag, curr_pos_x, curr_pos_y, moves)
    
  
  def generate_red_circle(self,win,  curr_pos_x, curr_pos_y, board, flag):
    curr_pos_x, curr_pos_y = self.return_xy(curr_pos_x, curr_pos_y)
    moves = []
    moves.append((curr_pos_x, curr_pos_y))
    directions = [
      (0, 1), (0, -1), (-1, 0), (1, 0)
    ]
    for x, y in directions:
      new_row, new_col = curr_pos_x + x, curr_pos_y + y
      while self.only_one_can_be_destroyed != 1 and self.is_valid(new_row, new_col, board, curr_pos_x, curr_pos_y):
        moves.append((new_row, new_col))    
        new_row, new_col = new_row + x, new_col + y  
      self.only_one_can_be_destroyed = 0
    return moves
  
class Knight(Figure): # skoczek(koń)
  def __init__(self, color):
    super().__init__(color)
       
  def show_red_circle(self,win,  curr_pos_x, curr_pos_y, board, flag):
    moves = []
    curr_pos_x, curr_pos_y = self.return_xy(curr_pos_x, curr_pos_y)
    moves.append((curr_pos_x, curr_pos_y))
    directions = [
      (2, 1), (2, -1), (-2, 1), (-2, -1), 
      (1, 2), (1, -2), (-1, 2), (-1, -2)
    ]
    for x, y in directions:
      new_row, new_col = curr_pos_x + x, curr_pos_y + y
      if self.is_valid(new_row, new_col, board, curr_pos_x, curr_pos_y):
        moves.append((new_row, new_col))
    # sprawdzam czy po ruszeniu sie swoim pionkiem nie zaszachowałem się sam 
    return self.escapeFromTheIsInCheck(win, board, flag, curr_pos_x, curr_pos_y, moves)
    
 
  def generate_red_circle(self,win,  curr_pos_x, curr_pos_y, board, flag):
    moves = []
    curr_pos_x, curr_pos_y = self.return_xy(curr_pos_x, curr_pos_y)
    moves.append((curr_pos_x, curr_pos_y))
    directions = [
      (2, 1), (2, -1), (-2, 1), (-2, -1), 
      (1, 2), (1, -2), (-1, 2), (-1, -2)
    ]
    for x, y in directions:
      new_row, new_col = curr_pos_x + x, curr_pos_y + y
      if self.is_valid(new_row, new_col, board, curr_pos_x, curr_pos_y):
        moves.append((new_row, new_col))
    return moves  

class Bishop(Figure): # Goniec
  def __init__(self, color):
    super().__init__(color)
  
  def show_red_circle(self,win,  curr_pos_x, curr_pos_y, board, flag):
    curr_pos_x, curr_pos_y = self.return_xy(curr_pos_x, curr_pos_y)
    moves = []
    moves.append((curr_pos_x, curr_pos_y))
    directions = [
      (1, 1), (1, -1), (-1, -1), (-1, 1)
    ]
    for x, y in directions:
      new_row, new_col = curr_pos_x + x, curr_pos_y + y
      while self.only_one_can_be_destroyed != 1 and self.is_valid(new_row, new_col, board, curr_pos_x, curr_pos_y):
        moves.append((new_row, new_col))
        new_row, new_col = new_row + x, new_col + y  
      self.only_one_can_be_destroyed = 0
    return self.escapeFromTheIsInCheck(win, board, flag, curr_pos_x, curr_pos_y, moves)
    
    
    
  def generate_red_circle(self,win,  curr_pos_x, curr_pos_y, board, flag):
    curr_pos_x, curr_pos_y = self.return_xy(curr_pos_x, curr_pos_y)
    moves = []
    moves.append((curr_pos_x, curr_pos_y))
    directions = [
      (1, 1), (1, -1), (-1, -1), (-1, 1)
    ]
    for x, y in directions:
      new_row, new_col = curr_pos_x + x, curr_pos_y + y
      while self.only_one_can_be_destroyed != 1 and self.is_valid(new_row, new_col, board, curr_pos_x, curr_pos_y):
        moves.append((new_row, new_col))
        new_row, new_col = new_row + x, new_col + y  
      self.only_one_can_be_destroyed = 0
    return moves
  
class Queen(Figure): # Hetman
  def __init__(self, color):
    super().__init__(color)
    
    
  def show_red_circle(self,win, curr_pos_x, curr_pos_y, board, flag):
    curr_pos_x, curr_pos_y = self.return_xy(curr_pos_x, curr_pos_y)
    moves = []
    moves.append((curr_pos_x, curr_pos_y))
    directions = [
      (1, 1), (1, -1), (-1, -1), (-1, 1), (0, 1), (0, -1), (-1, 0), (1, 0)
    ]
    for x, y in directions:
      new_row, new_col = curr_pos_x + x, curr_pos_y + y
      while self.only_one_can_be_destroyed != 1 and self.is_valid(new_row, new_col, board, curr_pos_x, curr_pos_y):
          moves.append((new_row, new_col))
          new_row, new_col = new_row + x, new_col + y  
      self.only_one_can_be_destroyed = 0
    return self.escapeFromTheIsInCheck(win, board, flag, curr_pos_x, curr_pos_y, moves)
    
    
  def generate_red_circle(self,win, curr_pos_x, curr_pos_y, board, flag):
    curr_pos_x, curr_pos_y = self.return_xy(curr_pos_x, curr_pos_y)
    moves = []
    moves.append((curr_pos_x, curr_pos_y))
    directions = [
      (1, 1), (1, -1), (-1, -1), (-1, 1), (0, 1), (0, -1), (-1, 0), (1, 0)
    ]
    for x, y in directions:
      new_row, new_col = curr_pos_x + x, curr_pos_y + y
      while self.only_one_can_be_destroyed != 1 and self.is_valid(new_row, new_col, board, curr_pos_x, curr_pos_y):
          moves.append((new_row, new_col))
          new_row, new_col = new_row + x, new_col + y  
      self.only_one_can_be_destroyed = 0
    return moves
  
  
class King(Figure):
  def __init__(self, color):
    super().__init__(color)
  
  
  
  def show_red_circle(self,win, curr_pos_x, curr_pos_y, board, flag):
    curr_pos_x, curr_pos_y = self.return_xy(curr_pos_x, curr_pos_y)
    moves = []
    moves.append((curr_pos_x, curr_pos_y))
    directions = [
      (1, 1), (1, -1), (-1, -1), (-1, 1), (0, 1), (0, -1), (-1, 0), (1, 0)
    ]
    for x, y in directions:
      new_row, new_col = curr_pos_x + x, curr_pos_y + y
      if self.only_one_can_be_destroyed != 1 and self.is_valid(new_row, new_col, board, curr_pos_x, curr_pos_y):
        moves.append((new_row, new_col))
        new_row, new_col = new_row + x, new_col + y  
      self.only_one_can_be_destroyed = 0
    return self.escapeFromTheIsInCheck(win, board, flag, curr_pos_x, curr_pos_y, moves)
    
  
  def generate_red_circle(self,win, curr_pos_x, curr_pos_y, board, flag):
    curr_pos_x, curr_pos_y = self.return_xy(curr_pos_x, curr_pos_y)
    moves = []
    moves.append((curr_pos_x, curr_pos_y))
    directions = [
      (1, 1), (1, -1), (-1, -1), (-1, 1), (0, 1), (0, -1), (-1, 0), (1, 0)
    ]
    for x, y in directions:
      new_row, new_col = curr_pos_x + x, curr_pos_y + y
      if self.only_one_can_be_destroyed != 1 and self.is_valid(new_row, new_col, board, curr_pos_x, curr_pos_y):
        moves.append((new_row, new_col))
        new_row, new_col = new_row + x, new_col + y  
        self.only_one_can_be_destroyed = 0
    return moves
  