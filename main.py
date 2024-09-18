import pygame
from constants import BLACK, ROWS, COLS, SQUARE_SIZE, WHITE, WHITE2, GREEN, WIDTH, HEIGHT
from board import Board
from figure import Figure
import pickle
import socket
import select

FPS = 60
WIN = pygame.display.set_mode((WIDTH,HEIGHT))


pygame.init()




def main():
  run = True
  
  clock = pygame.time.Clock()
  board = Board()
  figure = Figure(None)
  board.draw(WIN)
  board.draw_pieces(WIN)
  clock = pygame.time.Clock()
  
  ifCapturing = False
  pos = None
  obj_temp = None
  obj = None
  
  mouseXtemp, mouseYtemp = None, None
  mouseX, mouseY = None, None
  flag = False
  
  while run:
    clock.tick(FPS)
    
    
    for event in pygame.event.get():
      
      
      if event.type == pygame.QUIT:
        run = False

      if event.type == pygame.MOUSEBUTTONDOWN:

        mouse_position = pygame.mouse.get_pos() 
        obj_temp = obj
        mouseXtemp, mouseYtemp = mouseX, mouseY
        
        if ( obj != None 
            and figure.changingThePawnAuthorityFlag == True 
            and len(figure.options) > 0 
            and figure.options['x'] != mouse_position[0] 
            and figure.options['y'] != mouse_position[1] 
            and obj_temp.changingThePawnAuthorityFlagNoMoreThanOne != 0
            and board.board[mouseY][mouseX][1] == 'P'):
          obj_temp.changingThePawnAuthority(mouse_position[0], mouse_position[1], board, WIN, figure)
          obj_temp.changingThePawnAuthorityFlagNoMoreThanOne -= 1
          figure.changingThePawnAuthorityFlag = False
          
    
        obj = board.return_figure_obj(mouse_position[0], mouse_position[1]) 
      

        if obj == None or pos != None and not figure.deselect(pos,mouse_position[0], mouse_position[1]):
          figure.deselect_red_pieces(board, WIN)
          if figure.end == True:
              board.draw_text_centered(WIN, figure.winColor)
          
        
          if ifCapturing == False and obj_temp != None and pos != None and figure.deselect(pos,mouse_position[0], mouse_position[1]):
           
            if figure.end == False:
              obj_temp.move(figure, pos, mouse_position[0], mouse_position[1], board, WIN) #
            
           
            mouseX, mouseY = figure.return_xy(mouse_position[0], mouse_position[1])
          
          ifCapturing = False
        
        mouseX, mouseY = figure.return_xy(mouse_position[0], mouse_position[1])
       
      
        if obj :  
          mouseX, mouseY = figure.return_xy(mouse_position[0], mouse_position[1])
        
          if (  ( mouseX != mouseXtemp 
              or mouseY != mouseYtemp )
              and pos != None 
              and (mouseX, mouseY) in pos 
              and board.board[mouseY][mouseX] != None and obj_temp != None
              and board.pieces[(mouseY, mouseX)]['obj'].color != obj_temp.color 
              ): 
            
            if figure.end == False:
              obj_temp.capturing_a_pawn(figure, WIN, board, mouseX, mouseY, mouseXtemp, mouseYtemp)
            else:
              board.draw_text_centered(WIN, figure.winColor)
            
            ifCapturing = True
            
            
            continue
          
          if figure.end == False:
            pos = obj.show_red_circle(WIN, mouse_position[0], mouse_position[1], board, True)
          else:
              board.draw_text_centered(WIN, figure.winColor)
        
    
    pygame.display.update()  
          
  pygame.quit()
main()



