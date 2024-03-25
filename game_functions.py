import pygame
import sys
from chessboard_pygame import Pawn,Rook,Bishop,Knight
import numpy as np
import Board
def draw_pieces(screen,pieces,images):
    for piece in pieces:
        if piece.name == (np.uint8(1) or np.uint8(2)):
            image = images[0]
        elif piece.name == (np.uint8(3) or np.uint8(4)):
            image = images[1]
        elif piece.name == (np.uint8(5) or np.uint8(6)):
            image = images[2]
            
        elif piece.name == (np.uint8(7) or np.uint8(8)):
            image = images[3]
            
        elif piece.name == (np.uint8(9) or np.uint8(10)):
            image = images[4] 

        elif piece.name == (np.uint8(11) or np.uint8(14)):
            image = images[5] 
            
        elif piece.name == (np.uint8(12)):
            image = images[6]
        
        elif piece.name == (np.uint8(13)):
            image = images[7]
        piece.draw(screen,image)

def draw_arrow(screen, arrow, color=(0,0,0), arrow_size=10):
    if arrow is not None:
        end = arrow[1]
        offset = 40

        if arrow[0] is not None:
            start = arrow[0]

            # Draw the line (shaft of the arrow)
            pygame.draw.line(screen, color, start, end, 2)
        pygame.draw.rect(screen,(200,0,0),(end[0]-offset,end[1]-offset,87,87))
    

# Function to draw the chessboard
def draw_chessboard(screen):
    # Define colors
    WHITE = (255, 255, 255)
    GRAY = (128, 128, 128)
    SCREEN_WIDTH = 700
    SQUARE_SIZE = SCREEN_WIDTH // 8

    for row in range(8):
        for col in range(8):
            if (row + col) % 2 == 0:
                color = WHITE
            else:
                color = GRAY
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


pygame.display.set_caption("Chessboard")

def check_events(board,front_pawns,boardAI):
    """Respond to keypresses and mouse events"""
    pieces = board.pieces_w+board.pieces_b+front_pawns
    SQUARE_SIZE = 87
    if not board.ai_move:
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x,mouse_y = pygame.mouse.get_pos()
                    mouse_x = mouse_x
                    mouse_y = mouse_y
                    for piece in pieces:
                        if piece.check_piece(mouse_x,mouse_y,board.side_to_move):
                            piece.dragging = True
                            piece.previous_position = piece.position.copy()

                            
            elif event.type == pygame.MOUSEBUTTONUP:
                # Stop dragging any piece

                        for piece in pieces:
                            if piece.dragging:
                                piece.dragging = False
                                x = piece.rect
                                y = round(x[1] / SQUARE_SIZE)
                                x = round(x[0] / SQUARE_SIZE)
                                if not piece.check_board(x,y):
                                    piece.position  = piece.previous_position
                                    break

                                if piece.name == np.uint8(12):
                                    if piece.move == False:
                                        if piece.check_move(x,y,pieces):

                                            new_pawn = Pawn([x,y],1,np.uint8(12),True)
                                            new_pawn.previous_position = None
                                            board.move_save_for_AI = new_pawn

                                            board.pieces_w.append(new_pawn)
                                            board.side_to_move = not board.side_to_move
                                            board.ai_move = not board.ai_move

                                            piece.position  = piece.previous_position
                                        else:
                                            piece.position  = piece.previous_position
                                    else:
                                        piece.position = piece.previous_position
                                    
                                elif piece.name == np.uint8(13):
                                    if piece.move == False:
                                        if piece.check_move(x,y,pieces):
                                            new_pawn = Pawn([x,y],0,np.uint8(13),True)
                                            new_pawn.previous_position = None

                                            board.move_save_for_AI = new_pawn
                                            board.pieces_b.append(new_pawn)
                                            board.side_to_move = not board.side_to_move
                                            piece.position  = piece.previous_position
                                            board.ai_move = not board.ai_move


                                        else:
                                            piece.position  = piece.previous_position
                                    else:
                                            piece.position  = piece.previous_position

                                
                                else:

                                    if piece.check_move(x,y,pieces):
                                        board.move_save_for_AI = piece
                                        piece.position = [x,y]
                                        board.side_to_move = not board.side_to_move
                                        board.ai_move = not board.ai_move


                                    else:
                                        piece.position = piece.previous_position
        

    else:

        move = update_boardAI(board.move_save_for_AI)

        boardAI.make_move(move,not board.side_to_move)
        move = boardAI.get_AI_move(boardAI,depth=3,max_player=0)
        print(move)
        update_pygame(move,board)

        board.ai_move = not board.ai_move
        board.side_to_move = not board.side_to_move

def update_pygame(move,board):
    print(move[0][1])
    cur_x = move[0][1][1] % 8
    cur_y = move[0][1][1] // 8
    print("in update",cur_x,cur_y)
    if move[0][1][0] is not None:
        prev_x = move[0][1][0] % 8
        prev_y = move[0][1][0] // 8
        print(prev_x,prev_y)
        for piece in board.pieces_w[:6]+board.pieces_b[:6]:
            if piece.position[0] == prev_x and piece.position[1]==prev_y:
                print("updating")
                piece.position = [cur_x,cur_y]
                board.arrow = [[prev_x*87+40,prev_y*87+40],[cur_x*87+40,cur_y*87+40]]

    else:
        if not board.side_to_move:
            board.pieces_b.append(Pawn([cur_x,cur_y],0,np.uint8(13),True))
        else:
            board.pieces_w.append(Pawn([cur_x,cur_y],1,np.uint8(12),True))
        board.arrow = [None,[cur_x*87+40,cur_y*87+40]]

    
def update_boardAI(piece):
    if piece.previous_position is not None:
        prev = piece.previous_position[0]+8*piece.previous_position[1]
    cur = piece.position[0]+8*piece.position[1]

    if isinstance(piece,Rook):
        move = [prev,cur,1]
    elif isinstance(piece,Knight):
        move = [prev,cur,2]
    elif isinstance(piece,Bishop):
        move = [prev,cur,3]
    elif isinstance(piece,Pawn):
        move = [None,cur,4]
    return move

def check_victory(pieces,board):
    w = 0
    b = 0
    for piece in pieces:
        if piece.name == np.uint8(12):
            w+=1
        elif piece.name == np.uint8(13):
            b+=1
    if w ==8:
        print("White wins")
        board.victory = not board.victory

    elif b==8:
        print("Black wins")
        board.victory = not board.victory

def update_piece(pieces):
    for piece in pieces:
        if piece.dragging:
            mouse_x,mouse_y = pygame.mouse.get_pos()
            piece.update_position((mouse_x,mouse_y))

