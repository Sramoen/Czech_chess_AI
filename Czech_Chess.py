import pygame
import game_functions
from Settings import Settings
 # pygame setup
pygame.init()
settings = Settings()
screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))


# Pygame loop
while True:
    if (not settings.board.victory) and (not settings.board.draw):
        game_functions.check_events(settings.board,settings.front_pawns,settings.boardAI,
                                    settings.square,settings.SCREEN_WIDTH,settings.SCREEN_HEIGHT)
        game_functions.update_piece(settings.board.pieces_w+settings.board.pieces_b+settings.front_pawns)
    else:
        if game_functions.game_over_screen(screen,settings.board,settings.SCREEN_WIDTH,settings.SCREEN_HEIGHT):
            settings = Settings()
            continue
        else:
            break
    screen.fill("Brown")
    game_functions.draw_chessboard(screen,settings.square)
    game_functions.draw_arrow(screen,settings.board.arrow,settings.square)
    game_functions.draw_pieces(screen,settings.board.pieces_w+settings.board.pieces_b+settings.front_pawns)
    game_functions.print_evaluation(screen,settings.board.eval,settings.SCREEN_WIDTH,settings.SCREEN_HEIGHT)
    game_functions.check_victory(settings.board.pieces_w+settings.board.pieces_b,settings.board)
    game_functions.draw_depth(screen,settings.SCREEN_WIDTH,settings.SCREEN_HEIGHT,settings.boardAI.depth)



    pygame.display.flip()


pygame.quit()


