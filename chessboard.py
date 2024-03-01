import pygame



import copy

class Pieces():
    def __init__(self,position,color):
        self._position = position
        self.previous_position = copy.deepcopy(self._position)
        self.square = 87
        self.color = color
        self.square_size = 1
        self.dragging = False
        self.rect = pygame.Rect(self._position[0]*self.square, self._position[1]*self.square, 80, 80)

    @property
    def position(self):
        return self._position
    @position.setter
    def position(self,x):
        self._position = x.copy()
        self.rect[0] = x[0]*self.square
        self.rect[1] = x[1]*self.square

    def set_position(self,x,y):
        self.previous_position = copy.deepcopy(self._position)
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

                    return False
            return True
    
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
            for piece in pieces:
                for i in range(min_y+step_min,max_y+step_max,self.square_size):
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

            for piece in pieces:
                for i in range(min_x+step_min,max_x+step_max,self.square_size):
                    if piece._position == [i,y]:
                        if self._position != [i,y]:

                            return False
        else:
            return False

        
        return True   


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

        