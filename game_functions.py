import pygame
import sys
from chessboard_pygame import Pawn,Rook,Bishop,Knight
import numpy as np

def draw_pieces(screen,pieces):
    """Draw all pieces.
        Args:
            scrren(): pygame object.
            pieces(Piece): all pieces to draw.
    """
    for piece in pieces:
        piece.draw(screen)

def draw_arrow(screen, arrow,square, color=(0,0,0)):
    """Draw arrow after move.
        Args:
            screen(): pygame object.
            arrow(list,tuple): start and end coordinate of arrow.
            square(int): size of square on the chessboard.
            color(tuple): tuple of color of arrow, default(0,0,0).
    """
    if arrow is not None:
        end = arrow[1]
        offset = 40

        if arrow[0] is not None:
            start = arrow[0]

            # Draw the line
            pygame.draw.line(screen, color, start, end, 2)
        pygame.draw.rect(screen,(200,0,0),(end[0]-offset,end[1]-offset,square,square))
    

# Function to draw the chessboard
def draw_chessboard(screen,square_size):
    """Draw chessboard.
        Args:
            screen(): pygame object.
    """
    WHITE = (255, 255, 255)
    GRAY = (128, 128, 128)


    for row in range(8):
        for col in range(8):
            if (row + col) % 2 == 0:
                color = WHITE
            else:
                color = GRAY
            pygame.draw.rect(screen, color, (col * square_size, row * square_size, square_size, square_size))



def check_events(board,front_pawns,boardAI,square_size,screen_width,screen_height):
    """Check events that happen in chessboard.
        Args:
            board(Board_pygame): pygame representation of board.
            front_pawns(list): List of Pawn class, pawns on the front of the board.
            boardAI(Board): Board representation of AI.
            square_size(int): size of square.
            screen_width(int): width of screen.
            screen_height(int): height of screen.
    """
    pieces = board.pieces_w+board.pieces_b+front_pawns
    #Check if Human can make a move, if not make AI move
    if not board.ai_move:
        for event in pygame.event.get():
            #If qut - exit
            if (event.type == pygame.QUIT):
                sys.exit()
            #If clicked - checke for change in depth or piece movement
            elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x,mouse_y = pygame.mouse.get_pos()
                    mouse_x = mouse_x
                    mouse_y = mouse_y
                    if is_mouse_over_up_arrow([mouse_x,mouse_y],screen_width,screen_height):
                        increase_number(boardAI)
                    elif is_mouse_over_down_arrow([mouse_x,mouse_y],screen_width,screen_height):
                        decrease_number(boardAI)
                    else:
                        for piece in pieces:
                            if piece.check_piece(mouse_x,mouse_y,board.side_to_move):
                                piece.dragging = True
                                piece.previous_position = piece.position.copy()

            # If mouseup - check if move is possible and make it
            elif event.type == pygame.MOUSEBUTTONUP:
                # Stop dragging any piece

                        for piece in pieces:
                            if piece.dragging:
                                piece.dragging = False
                                #Get coordinates of move
                                x = piece.rect
                                y = round(x[1] / square_size)
                                x = round(x[0] / square_size)
                                #Check if cordinates on board
                                if not piece.check_board(x,y):
                                    piece.position  = piece.previous_position
                                    break

                                if (piece.name == np.uint8(12)) or (piece.name == np.uint8(13)):
                                    #Make pawn move
                                    pawn_move(pieces,piece,board,x,y)                                
                                else:
                                    #Make piece move
                                    piece_move(pieces,piece,board,x,y)
    else:
        #Get and make AI move
        AI_move(boardAI,board,square_size)
        

def pawn_move(pieces,piece,board,x,y):
    """Make pawn move.
        Args:
            pieces(lits): pieces on chessboard
            piece(Piece): piece (pawn) to move.
            board(Board_pygame): pygame representation of board.
            x(int): x position to move piece.
            y(int): y position to move piece.
    """
    # If not possible move == return piece to inital square
    if piece.move == False:
        if piece.check_move(x,y,pieces):
            #White pawn
            if piece.name == np.uint8(12):
                new_pawn = Pawn([x,y],1,np.uint8(12),True)
                board.pieces_w.append(new_pawn)
            #Black pawn
            else:
                new_pawn = Pawn([x,y],1,np.uint8(12),True)
                board.pieces_b.append(new_pawn)
            new_pawn.previous_position = None
            board.move_save_for_AI = new_pawn
            board.side_to_move = not board.side_to_move
            board.ai_move = not board.ai_move
            #Save position - for checking threefold repetition
            position = board.flatten([piece.position for piece in board.pieces_w + board.pieces_b])+[1]
            board.positions.append(int(''.join(map(str, position))))
            board.check_threefold_repetition()

            piece.position  = piece.previous_position
        else:
            piece.position  = piece.previous_position
    else:
        piece.position = piece.previous_position
def piece_move(pieces,piece,board,x,y):
    """Make piece move.
        Args:
            pieces(lits): pieces on chessboard
            piece(Piece): piece (pawn) to move.
            board(Board_pygame): pygame representation of board.
            x(int): x position to move piece.
            y(int): y position to move piece.
    """
    #Check if move possible - else return piece to initial square
    if piece.check_move(x,y,pieces):
        board.move_save_for_AI = piece
        piece.position = [x,y]
        board.side_to_move = not board.side_to_move
        board.ai_move = not board.ai_move
        #Save position - for checking threefold repetition
        position = board.flatten([piece.position for piece in board.pieces_w + board.pieces_b])+[1]
        board.positions.append(int(''.join(map(str, position))))
        board.check_threefold_repetition()

    else:
        piece.position = piece.previous_position

def AI_move(boardAI,board,square):
        """Make AI move.
            Args:
                boardAI(Board): AI representation of board.
                board(Board_pygame): pygame representation of board.
                square(int): size of square on the board.
        """
        #Ai is on the move - update his board since the last time
        move = update_boardAI(board.move_save_for_AI)
        boardAI.make_move(move,not board.side_to_move)
        #Get Ai move
        move = boardAI.get_AI_move(boardAI,max_player=0)
        board.eval = move[0][0]
        #Update pygame board
        update_pygame(move,board,square)

        #Save position - checking for three fold repetition
        position = board.flatten([piece.position for piece in board.pieces_w + board.pieces_b])+[0]
        board.positions.append(int(''.join(map(str, position))))
        board.check_threefold_repetition()

        #Set human to move and change side to move
        board.ai_move = not board.ai_move
        board.side_to_move = not board.side_to_move

def print_evaluation(screen,eval,screen_width,screein_height):
    """Print evaluation of AI on the pygame board.
            Args:
                screen(): pygame object.
                eval(int): AI evaluation of position.
                screen_width(int): width of screen.
                screein_height(int):  height of screen.
    """
    font = pygame.font.Font(None, 20)
    text_surface = font.render(f"Eval AI:{eval}", True, (0,0,0))
    text_rect = text_surface.get_rect()
    text_rect.bottomright = (screen_width - 10, screein_height - 10) # Position at top-left corner
    screen.blit(text_surface, text_rect)

def update_pygame(move,board,square):
    """Update pygame board afte AI moved.
        Args:
            move(list): move made by AI.
            board(Board): board representation pygame.
            square(int): size of square on the pygame board.
    """
    cur_x = move[0][1][1] % 8
    cur_y = move[0][1][1] // 8
    if move[0][1][0] is not None:
        prev_x = move[0][1][0] % 8
        prev_y = move[0][1][0] // 8
        for piece in board.pieces_w[:6]+board.pieces_b[:6]:
            if piece.position[0] == prev_x and piece.position[1]==prev_y:
                piece.position = [cur_x,cur_y]
                board.arrow = [[prev_x*square+40,prev_y*square+40],[cur_x*square+40,cur_y*square+40]]

    else:
        if not board.side_to_move:
            board.pieces_b.append(Pawn([cur_x,cur_y],0,np.uint8(13),True))
        else:
            board.pieces_w.append(Pawn([cur_x,cur_y],1,np.uint8(12),True))
        board.arrow = [None,[cur_x*square+40,cur_y*square+40]]

    
def update_boardAI(piece):
    """Update pygame board after Human moved.
        Args:
            piece(Piece): piece which moved.
    """
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
    """Check if either side won. If so end game
        Args:
            pieces(list): List of pieces.
            board(Board_pygame): Pygame representation of board
    """
    w = 0
    b = 0
    for piece in pieces:
        if piece.name == np.uint8(12):
            w+=1
        elif piece.name == np.uint8(13):
            b+=1
    if w ==8:
        board.victory = not board.victory

    elif b==8:
        board.victory = 2

def update_piece(pieces):
    """Update piece location when dragging.
        Args:
            pieces(list): List of pieces.
    """
    for piece in pieces:
        if piece.dragging:
            mouse_x,mouse_y = pygame.mouse.get_pos()
            piece.update_position((mouse_x,mouse_y))

def game_over_screen(screen,board,screen_width,screen_height):
    """Screen after game ended - check if user wants to play again. Print Game over and Play again text on screen.
            Args:
                screen(): pygame object.
                board(Board_pygame): pygame representation of board.
                screen_width(int): width of screen.
                screein_height(int):  height of screen.
    """    
    font = pygame.font.Font(None, 36)
    if board.draw:
        text = "Game over. Draw by three-fold repetition!"
    elif board.victory==1:
        text = "Game over. White won!"
    else:
        text = "Game over. Black won!"
    game_over_text = font.render(text, True, (0,0,0))
    text_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2))
    pygame.draw.rect(screen, (173,216,230), text_rect)
    screen.blit(game_over_text, text_rect)

    play_again_text = font.render("Play Again", True, (0,0,0))
    play_again_rect = play_again_text.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
    pygame.draw.rect(screen, (173,216,230), play_again_rect)
    screen.blit(play_again_text, play_again_rect)

    pygame.display.flip()
    #Wait for user input - Play again or quit
    while True:


        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if play_again_rect.collidepoint(mouse_pos):
                    return True  # Start the game again
                
def draw_depth(screen,screen_width,screen_height,depth_of_AI):
    """Draw depth on the board and the polygons, so user can change depth.
            Args:
                screen(): pygame object.
                screen_width(int): width of screen.
                screein_height(int):  height of screen.
                depth_of_AI(int): depth AI should search.
    """      
    font = pygame.font.SysFont(None, 20)
    text = font.render(f"Depth of AI: {depth_of_AI}", True, (0,0,0))
    text_rect = text.get_rect()
    text_rect.bottomright = (screen_width - 10, screen_height - 100) # Position at top-left corner

    screen.blit(text,text_rect)
    # Draw up arrow
    pygame.draw.polygon(screen, (0,0,0), [(screen_width - 50, screen_height - 120),
                                     (screen_width - 40, screen_height - 120), (screen_width - 45, screen_height - 130)])
    # Draw down arrow
    pygame.draw.polygon(screen, (0,0,0), [(screen_width - 50, screen_height - 90),
                                     (screen_width - 40, screen_height - 90), (screen_width - 45, screen_height - 80)])
def increase_number(boardAI):
    """Increase depth.
            Args:
                boardAI(Board): Board representation of AI.
    """      
    boardAI.depth += 1

def decrease_number(boardAI):
    """Decrease depth.
            Args:
                boardAI(Board): Board representation of AI.
    """      
    boardAI.depth -= 1
    if boardAI.depth <= 0:
        boardAI.depth = 1

def is_mouse_over_up_arrow(mouse_pos,screen_width,screen_height):
    """Check if mouse and polygon (increase depth) collide.
            Args:
                mouse_pos(list): Mouse coordinates.
                screen_width(int): width of screen.
                screein_height(int):  height of screen.
    """   
    return (screen_width - 50 <= mouse_pos[0] <= screen_width - 40 and
            screen_height - 130 <= mouse_pos[1] <= screen_height - 120)
def is_mouse_over_down_arrow(mouse_pos,screen_width,screen_height):
    """Check if mouse and polygon (decrease depth) collide.
            Args:
                mouse_pos(list): Mouse coordinates.
                screen_width(int): width of screen.
                screein_height(int):  height of screen.
    """   
    return (screen_width - 50 <= mouse_pos[0] <= screen_width - 40 and
            screen_height - 95 <= mouse_pos[1] <= screen_height - 80)