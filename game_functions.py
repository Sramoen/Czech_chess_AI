import pygame
import sys
from chessboard import Pawn

def draw_pieces(screen,pieces,images):
    for piece in pieces:
        if piece.name == ("r1" or "r2"):
            image = images[0]
        elif piece.name == ("r3" or "r4"):
            image = images[1]
        elif piece.name == ("k1" or "k2"):
            image = images[2]
            
        elif piece.name == ("k3" or "k3"):
            image = images[3]
            
        elif piece.name == ("b1" or "b2"):
            image = images[4] 

        elif piece.name == ("b3" or "b4"):
            image = images[5] 
            
        elif piece.name == ("p1"):
            image = images[6]
        
        elif piece.name == ("p2"):
            image = images[7]
        piece.draw(screen,image)



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

def check_events(board,front_pawns):
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

                                if piece.name == "p1":
                                    if piece.move == False:
                                        if piece.check_move(x,y,pieces):
                                            new_pawn = Pawn([x,y],1,"p1",True)
                                            board.pieces_w.append(new_pawn)
                                            board.side_to_move = not board.side_to_move
                                            board.ai_move = not board.ai_move

                                            piece.position  = piece.previous_position
                                        else:
                                            piece.position  = piece.previous_position
                                    else:
                                        piece.position = piece.previous_position
                                    
                                elif piece.name == "p2":
                                    if piece.move == False:
                                        if piece.check_move(x,y,pieces):
                                            new_pawn = Pawn([x,y],0,"p2",True)
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
                                        piece.position = [x,y]
                                        board.side_to_move = not board.side_to_move
                                        board.ai_move = not board.ai_move


                                    else:
                                        piece.position = piece.previous_position

    else:
        move = board.get_AI_move(board,1)

        for piece in pieces:
            if piece.name == move[0][1][2]:
                if piece.name == "p1":
                    new_pawn = Pawn([move[0][1][0],move[0][1][1]],1,"p1",True)
                    board.pieces_w.append(new_pawn)
                elif piece.name == "p2":
                    new_pawn = Pawn([move[0][1][0],move[0][1][1]],0,"p2",True)
                    board.pieces_w.append(new_pawn)
                else:
                    piece.position = [move[0][1][0],move[0][1][1]]
        board.ai_move = not board.ai_move
        board.side_to_move = not board.side_to_move

def check_victory(pieces,board):
    w = 0
    b = 0
    for piece in pieces:
        if piece.name == "p1":
            w+=1
        elif piece.name == "p2":
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

        