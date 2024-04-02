import pygame
import copy
import numpy as np

class Pieces():
    """Class for piece representation in pygame."""
    def __init__(self,position,color):
        """Initialize pygame piece.

            Args:
                position(list): coordinates of piece.
                color(bool): color of piece, False if black, True if White.
        """
        self._position = position
        self.previous_position = [copy.deepcopy(self._position)]
        self.square = 87
        self.color = color
        self.square_size = 1
        self.dragging = False
        self.rect = pygame.Rect(self._position[0]*self.square, self._position[1]*self.square, 80, 80)
        self.move_save_for_AI = None

    #Used property to make MR. Dobrovsky proud :)
    @property
    def position(self):
        return self._position
    @position.setter
    def position(self,x):
        self._position = x.copy()
        self.rect[0] = x[0]*self.square
        self.rect[1] = x[1]*self.square

    def set_position(self,x,y):
        self.previous_position.append(copy.deepcopy(self._position))
        self._position[0] = x
        self._position[1] = y

    def set_position_unmake(self,x,y):
        self.previous_position.pop()
        self._position[0] = x
        self._position[1] = y

    def check_piece(self,mouse_x,mouse_y,color):
        """Check if piece collide with mouse.
            Args:
                mouse_x(int): x coordinate of mouse.
                mouse_y(int): y coordinate of mouse.
                color(bool): color of piece.
        """
        if self.color == color:
            return self.rect.collidepoint((mouse_x,mouse_y))
        
    def draw(self,screen,image):
        """Draw piece.
        Args:
            screen(): pygame object.
            image(list): pygame image.
        """
        screen.blit(image,[self.rect[0],self.rect[1]])

    def update_position(self,mouse):
        """Update position of pice to center of mouse.
            Arge:
                mouse(list): coordinates of mouse.
        """
        self.rect[0] = self._position[0]*87
        self.rect[1] = self._position[1]*87
        self.rect.center = mouse

    def check_board(self,x,y):
        """Check if piece is still in the board.
            Args:
                x(int): x coordinate.
                y(int): y coordinate.
        """
        return ((x <= 7) and (y <= 7) and (x>=0) and (y>=0))        
        
class Bishop(Pieces):
    """Class for represeting bishop."""
    
    def __init__(self,position,color,name):
        """Initialize bishop.
            Args:
                position(list): position of bishop.
                color(bool): color of bishop.
                name(int): name of bishop.
        """
        super().__init__(position,color)        
        self.name = name

    def is_empty(self,stepx,stepy,pieces):
            """Check if the square is empty.
            
                Args:
                    stepx(int): new x position of piece.
                    stepx(int): new y position of piece.
                    pieces(list): list of all pieces.
            """
            for piece in pieces:    
                if piece._position == [self._position[0]+stepx,self._position[1]+stepy]:
                    return False
            return True          

    def check_move(self,x,y,pieces,pawn_check=False):
        """Check if the move is possible.
            Args:
                x(int): x coordinate of move.
                y(int): y coordinate of move
                pices(list): list of pieces.
                pawn_check(bool): True if check_move is used fro checking pawn move.
        """
        number_of_squares_x = x - self._position[0]
        number_of_squares_y = y - self._position[1]

        if (abs(number_of_squares_x) == abs(number_of_squares_y)) and (number_of_squares_y!=0):
            if x > self._position[0]:
                step_x = self.square_size
            else:
                step_x = -self.square_size

            if y > self._position[1]:
                step_y = self.square_size
            else:
                step_y = -self.square_size

            for piece in pieces:
                for i,j in zip(range(self._position[0]+step_x,x+step_x,step_x),
                                range(self._position[1]+step_y,y+step_y,step_y)):
                    if piece._position == [i,j]:
                        return False
        else:
            return False
        return True


class Knight(Pieces):
    """Class for represeting knight."""
    def __init__(self,position,color,name):
        """Initialize knight.
            Args:
                position(list): position of knight.
                color(bool): color of knight.
                name(int): name of knight.
        """
        super().__init__(position,color)   
        self.name = name
            
    def check_move(self,x,y,pieces,pawn_check=False):
        """Check if the move is possible.
            Args:
                x(int): x coordinate of move.
                y(int): y coordinate of move
                pices(list): list of pieces.
                pawn_check(bool): True if check_move is used fro checking pawn move.
        """
        if ((self._position[0] + self.square_size*2 == x or self._position[0] - self.square_size*2==x)\
            and (self._position[1] + self.square_size == y or self._position[1] - self.square_size==y))\
        or ((self._position[1] + self.square_size*2 == y or self._position[1] - self.square_size*2==y)\
            and (self._position[0] + self.square_size == x or self._position[0] - self.square_size==x)):
            for piece in pieces:
                if piece._position == [x,y]:
                    print("Figurka je: ", piece._position,piece.name)
                    return False
            return True
        return False
    def is_empty(self,pieces,x,y):
        """Check if the square is empty.
        
            Args:
                x(int): new x position of piece.
                y(int): new y position of piece.
                pieces(list): list of all pieces.
        """
        for piece in pieces:
            if piece._position == [x,y]:
                return False
        return True
    
class Rook(Pieces):
    """Class for represeting rook."""

    def __init__(self,position,color,name):
        """Initialize rook.
            Args:
                position(list): position of rook.
                color(bool): color of rook.
                name(int): name of rook.
        """
        super().__init__(position,color)          
        self.name = name 
    def check_move(self,x,y,pieces,pawn_check=False):
        """Check if the move is possible.
            Args:
                x(int): x coordinate of move.
                y(int): y coordinate of move
                pices(list): list of pieces.
                pawn_check(bool): True if check_move is used fro checking pawn move.
        """
        if x == self._position[0] and y != self._position[1]:

            min_y, max_y = sorted([self._position[1],y])
            if pawn_check:
                if self._position[1] == min_y:
                    step_min = self.square_size
                    step_max = self.square_size
                else:
                    step_min = 0
                    step_max = 0
            else:
                    step_min = 0
                    step_max = self.square_size
            for i in range(min_y+step_min,max_y+step_max,self.square_size):
                for piece in pieces:
                    if piece._position == [x,i]:
                            if self._position != [x,i]:
                    
                                return False

        elif y == self._position[1] and x != self._position[0]:
            min_x, max_x = sorted([self._position[0],x])
            if pawn_check:
                if self._position[0] == min_x:
                    step_min = self.square_size
                    step_max = self.square_size
                else:
                    step_min = 0
                    step_max = 0
            else:
                    step_min = 0
                    step_max = self.square_size
            for i in range(min_x+step_min,max_x+step_max,self.square_size):
                for piece in pieces:
                    if piece._position == [i,y]:
                        if self._position != [i,y]:

                            return False
        else:
            return False

        
        return True
    
    def is_empty(self,stepx,stepy,pieces):
        """Check if the square is empty.
        
            Args:
                stepx(int): new x position of piece.
                stepy(int): new y position of piece.
                pieces(list): list of all pieces.
        """
        for piece in pieces:    
            if piece._position == [self._position[0]+stepx,self._position[1]+stepy]:
                return False    
        return True

class Pawn(Pieces):
    """Class for representing pawn."""
    def __init__(self,position,color,name,move):
        """Initialize knight.
            Args:
                position(list): position of pawn.
                color(bool): color of pawn.
                name(int): name of pawn.
        """
        super().__init__(position,color)   
        self.name = name
        self.move = move
    def check_move(self,x,y,pieces):
        """Check if the move is possible.
            Args:
                x(int): x coordinate of move.
                y(int): y coordinate of move
                pices(list): list of pieces.
                pawn_check(bool): True if check_move is used fro checking pawn move.
        """
        if not self.move:
            number_of_pieces = 0
            for piece in pieces:
                if isinstance(piece,Pawn):
                    continue
                if piece.color == self.color:
                    if piece.check_move(x,y,pieces,pawn_check=True):
                        number_of_pieces += 1
                if number_of_pieces == 3:
                    return True
        return False
    

class Board_pygame:
    """Class for representing pygame board."""
    def __init__(self,ai_starts=False):
        """Initialization of pygame board class.
        Args:
            ai_starts (bool): False (default) if AI play as black.
        """
        self.victory = 0
        self.best_move = None
        
        self.pieces_w = [Rook([0,7],1,np.uint8(1)),Rook([7,7],1,np.uint8(2)),
                         Knight([1,7],1,np.uint(3)),Knight([6,7],1,np.uint8(4)),
                         Bishop([2,7],1,np.uint8(5)),Bishop([5,7],1,np.uint8(6)),
                         ]
        self.pieces_b = [Rook([0,0],0,np.uint8(7)),Rook([7,0],0,np.uint8(8)),
                         Knight([1,0],0,np.uint8(9)),Knight([6,0],0,np.uint8(10)),
                         Bishop([2,0],0,np.uint8(11)),Bishop([5,0],0,np.uint8(14)),
                         ]
        self.pawns_w = [Pawn([-1,-1],1,np.uint8(12),False)]
        self.pawns_b = [Pawn([-1,-1],0,np.uint8(13),False)]


        self.iter = 0
        self.depth = None
        self.ai_move = ai_starts
        self.side_to_move = int(not ai_starts)
        self.moves_b = None
        self.moves_w = None
        self.arrow = None