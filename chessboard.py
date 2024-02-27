SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700

offset_x = -100
offset_y = 50

import copy

class Pieces():
    def __init__(self,position,color):
        self.position = position
        self.previous_position = copy.deepcopy(self.position)

        self.color = color
        self.square_size = 1

    def get_position(self):
        return self.position
    
    def set_position(self,x,y):
        self.previous_position = copy.deepcopy(self.position)
        self.position[0] = x
        self.position[1] = y


class Bishop(Pieces):
    
    def __init__(self,position,color,name):
        super().__init__(position,color)        
        self.name = name

    def check_move(self,x,y,pieces,pygame_pawn_check=False):
        number_of_squares_x = x - self.position[0]
        number_of_squares_y = y - self.position[1]

        if (abs(number_of_squares_x) == abs(number_of_squares_y)) and (number_of_squares_y!=0):
            if x > self.position[0]:
                step_x = self.square_size
            else:
                step_x = -self.square_size

            if y > self.position[1]:
                step_y = self.square_size
            else:
                step_y = -self.square_size

            for piece in pieces:
                for i,j in zip(range(self.position[0]+step_x,x+step_x,step_x),
                                range(self.position[1]+step_y,y+step_y,step_y)):
                    if piece.get_position() == (i,j):
                        return False
        else:
            return False
        return True


class Knight(Pieces):

    def __init__(self,position,color,name):
        super().__init__(position,color)   
        self.name = name

    def check_move(self,x,y,pieces,pygame_pawn_check=False):
        if ((self.position[0] + self.square_size*2 == x or self.position[0] - self.square_size*2==x)\
            and (self.position[1] + self.square_size == y or self.position[1] - self.square_size==y))\
        or ((self.position[1] + self.square_size*2 == y or self.position[1] - self.square_size*2==y)\
            and (self.position[0] + self.square_size == x or self.position[0] - self.square_size==x)):
            for piece in pieces:
                if piece.get_position() == (x,y):
                    return False
            return True
    
class Rook(Pieces):
    def __init__(self,position,color,name):
        super().__init__(position,color)          
        self.name = name
       
    def check_move(self,x,y,pieces,pygame_pawn_check=False):
        # print("here in rook")

        if x == self.position[0] and y != self.position[1]:

            min_y, max_y = sorted([self.position[1],y])
            if pygame_pawn_check:
                if self.position[1] == min_y:
                    step_min = self.square_size
                    step_max = self.square_size
                else:
                    step_min = 0
                    step_max = 0
            else:
                    step_min = 0
                    step_max = self.square_size 
            for piece in pieces:
                for i in range(min_y+step_min,max_y+step_max,self.square_size):
                    if piece.position == [x,i]:
                        if self.position != [x,i]:
                    
                            return False

        elif y == self.position[1] and x != self.position[0]:
            min_x, max_x = sorted([self.position[0],x])
            if pygame_pawn_check:
                if self.position[0] == min_x:
                    step_min = self.square_size
                    step_max = self.square_size
                else:
                    step_min = 0
                    step_max = 0
            else:
                    step_min = 0
                    step_max = self.square_size

            for piece in pieces:
                for i in range(min_x+step_min,max_x+step_max,self.square_size):
                    if piece.position == [i,y]:
                        if self.position != [i,y]:

                            return False
        else:
            return False

        
        return True   


class Pawn(Pieces):
    def __init__(self,position,color,name):
        super().__init__(position,color)   
        self.name = name
    def check_move(self,x,y,pieces):
        # print("here in pawn")

        number_of_pieces = 0
        for piece in pieces:
            if isinstance(piece,Pawn):
                continue
            if piece.color == self.color:
                if piece.check_move(x,y,pieces,pygame_pawn_check=True):
                    number_of_pieces += 1
            if number_of_pieces == 3:
                return True
        return False

        