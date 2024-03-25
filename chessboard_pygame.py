import pygame
import copy
import numpy as np

class Pieces():
    def __init__(self,position,color):
        self._position = position
        self.previous_position = [copy.deepcopy(self._position)]
        self.square = 87
        self.color = color
        self.square_size = 1
        self.dragging = False
        self.rect = pygame.Rect(self._position[0]*self.square, self._position[1]*self.square, 80, 80)
        self.move_save_for_AI = None

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
        if self.color == color:
            return self.rect.collidepoint((mouse_x,mouse_y))
        
    def draw(self,screen,image):
        screen.blit(image,[self.rect[0],self.rect[1]])

    def update_position(self,mouse):
        self.rect[0] = self._position[0]*87
        self.rect[1] = self._position[1]*87
        self.rect.center = mouse

    def check_board(self,x,y):
        return ((x <= 7) and (y <= 7) and (x>=0) and (y>=0))        
        
class Bishop(Pieces):
    
    def __init__(self,position,color,name):
        super().__init__(position,color)        
        self.name = name

    def is_empty(self,stepx,stepy,pieces):
            for piece in pieces:    
                if piece._position == [self._position[0]+stepx,self._position[1]+stepy]:
                    return False
            return True          

    def check_move(self,x,y,pieces,pawn_check=False):
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
    def generate_moves(self,pieces):
        moves = []

        step = 1
        x,y = self._position
        while x-step >=0 and y+step <=7: #vlevo nahoru
            if not self.is_empty(-step,step,pieces):
                break
            moves.append([x-step,y+step,self.name])
            step +=1
        step = 1
        while x+step <=7 and y+step <=7: #vpravo nahoru
            if not self.is_empty(step,step,pieces):
                break
            moves.append([x+step,y+step,self.name])
            step +=1
        step =1
        while x-step>=0 and y-step >=0: #vlevo dolů
            if not self.is_empty(-step,-step,pieces):
                break
            moves.append([x-step,y-step,self.name])
            step +=1
        step = 1
        while x+step <=7 and y-step >=0: #vpravo dolů
            if not self.is_empty(step,-step,pieces):
                break
            moves.append([x+step,y-step,self.name])
            step +=1

        return moves  


class Knight(Pieces):

    def __init__(self,position,color,name):
        super().__init__(position,color)   
        self.name = name
            
    def check_move(self,x,y,pieces,pawn_check=False):
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
        for piece in pieces:
            if piece._position == [x,y]:
                return False
        return True
    def generate_moves(self,pieces):
        moves = []
        x,y = self._position
        deltas = [(2, 1), (1, 2), (-2, 1), (-1, 2), (2, -1), (1, -2), (-2, -1), (-1, -2)]
        for dx, dy in deltas:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x <= 7 and 0 <= new_y <= 7:
                if not self.is_empty(pieces,new_x,new_y):
                    continue
                moves.append([new_x, new_y,self.name])
        # print("Tahy jezdcem",moves)
        return moves
    
class Rook(Pieces):
    def __init__(self,position,color,name):
        super().__init__(position,color)          
        self.name = name 
    def check_move(self,x,y,pieces,pawn_check=False):
        # print("here in rook")

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
            for piece in pieces:    
                if piece._position == [self._position[0]+stepx,self._position[1]+stepy]:
                    return False    
            return True
           
    def generate_moves(self,pieces):

        x, y = self._position
        moves = []
        step = 1
        while x+step <=7: #vlevo nahoru
            if not self.is_empty(step,0,pieces):
                break
            moves.append([x+step,y,self.name])
            step +=1
        step = 1
        while y+step <=7: #vlevo nahoru
            if not self.is_empty(0,step,pieces):
                break
            moves.append([x,y+step,self.name])
            step +=1
        step = 1
        while y-step >=0: #vlevo nahoru
            if not self.is_empty(0,-step,pieces):
                break
            moves.append([x,y-step,self.name])
            step +=1
        step = 1
        while x-step >=0: #vlevo nahoru
            if not self.is_empty(-step,0,pieces):
                break
            moves.append([x-step,y,self.name])
            step +=1

        return moves

class Pawn(Pieces):
    def __init__(self,position,color,name,move):
        super().__init__(position,color)   
        self.name = name
        self.move = move
    def check_move(self,x,y,pieces):

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
    
    def generate_moves(self,moves,max_player):
        count = {}
        triplets = []
        for coord in moves:
            # Convert the coordinate to a tuple to make it hashable
            coord_tuple = tuple(coord[:2])
            count[coord_tuple] = count.get(coord_tuple, 0) + 1
            if count[coord_tuple] == 3:
                triplets.append([coord[0],coord[1],13-max_player])
        return triplets
class Board_pygame:
    def __init__(self,ai_starts=False):
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