import Board
from chessboard_pygame import Pawn,Board_pygame
import numpy as np
class Settings():
    """
    Class for setting pygame chessboard environment.
    """
    def __init__(self):
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 696
        self.square = 87

        #Create boards
        self.board = Board_pygame() #white starts
        self.boardAI = Board.Board(depth=3) #initial depth of AI


        self.front_pawns = [Pawn([8,3],1,np.uint8(12),False),
                    Pawn([8,4],0,np.uint8(13),False)]