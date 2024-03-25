# Example file showing a basic pygame "game loop"
import pygame
from chessboard_pygame import Pawn,Board_pygame
import game_functions
import Board
import numpy as np
 # pygame setup
pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((800, 700))
clock = pygame.time.Clock()
running = True
square = 87
#Settings
board = Board_pygame() #white starts
boardAI = Board.Board()

r1 = pygame.transform.scale((pygame.image.load("D:\AAA_kodování\Alg_um_int\obrazky\WRook.png")),(80,80))
r0 = pygame.transform.scale((pygame.image.load("D:\AAA_kodování\Alg_um_int\obrazky\BRook.png")),(80,80))
k1 = pygame.transform.scale((pygame.image.load("D:\AAA_kodování\Alg_um_int\obrazky\WKnight.png")),(80,80))
k0 = pygame.transform.scale((pygame.image.load("D:\AAA_kodování\Alg_um_int\obrazky\BKnight.png")),(80,80))
b1 = pygame.transform.scale((pygame.image.load("D:\AAA_kodování\Alg_um_int\obrazky\WBishop.png")),(80,80))
b0 = pygame.transform.scale((pygame.image.load("D:\AAA_kodování\Alg_um_int\obrazky\BBishop.png")),(80,80))
p1 = pygame.transform.scale((pygame.image.load("D:\AAA_kodování\Alg_um_int\obrazky\WPawn.png")),(80,80))
p0 = pygame.transform.scale((pygame.image.load("D:\AAA_kodování\Alg_um_int\obrazky\BPawn.png")),(80,80))
draw_pieces_list = [r1,k1,b1,r0,k0,b0,p1,p0]

offset_x = -100
offset_y = 50
front_pawns = [Pawn([8,3],1,np.uint8(12),False),
               Pawn([8,4],0,np.uint8(13),False)]


while running:

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("brown")
    if not board.victory:         
        game_functions.check_events(board,front_pawns,boardAI)
        game_functions.update_piece(board.pieces_w+board.pieces_b+front_pawns)
    else:
        break
    game_functions.draw_chessboard(screen)
    game_functions.draw_arrow(screen,board.arrow)
    game_functions.draw_pieces(screen,board.pieces_w+board.pieces_b+front_pawns,draw_pieces_list)
    game_functions.check_victory(board.pieces_w+board.pieces_b,board)



    pygame.display.flip()


pygame.quit()


