
import numpy as np

class Pieces():
    def __init__(self,color,piece_keys_zobras_hasing):
        self.color = color
        self.rook_moves = None
        self.bishop_moves = None
        self.knight_moves = None
        self.board_max = 2**64
        self.piece_keys_zobras_hasing = piece_keys_zobras_hasing
        self.name = None

    def pop_LSB(self,b):
        index = (b & -b).bit_length() - 1
        b &= b - 1
        return index,b
    
    def clear_file(self,file):
        return 0x0101010101010101 << file
    
    def update_hash(self,from_square_index,to_square_index,hash_value):
        # XOR out the Zobrist key for the piece at the "from" square

        if from_square_index is not None:
            # print(self.piece_keys_zobras_hasing[piece][from_square_index])
            hash_value ^= self.piece_keys_zobras_hasing[self.name][from_square_index]
        if to_square_index is not None:
            # print(self.piece_keys_zobras_hasing[piece][from_square_index])
            # XOR in the Zobrist key for the piece at the "to" square
            hash_value ^= self.piece_keys_zobras_hasing[self.name][to_square_index]
            # XOR side_to_move
        if not self.color:
            hash_value ^= 1
        return hash_value

class Bishop(Pieces):
    
    def __init__(self,color,piece_keys_zobras_hasing):
        super().__init__(color,piece_keys_zobras_hasing)             
        self.name = 3
        self.piece_keys_zobras_hasing = piece_keys_zobras_hasing
        self.color = color
        self.spot1 = ~self.clear_file(7)
        self.spot2 = ~self.clear_file(0)

    def all_posible_moves(self,index, occupied_bitmap):
        # Initialize an empty bitmap to store legal moves
        piece_bitmap = 1 << index   
        legal_moves_bitmap = 0
        # Compute legal moves for each direction using bitwise operations
        for direction in range(4):
            # Compute the possible moves in the current direction
            possible_moves = piece_bitmap

            # Apply the shift corresponding to the current direction
            if direction == 0:  # Up left
                possible_moves <<= 9
                possible_moves &= self.spot2
            elif direction == 1:  # Down left
                possible_moves >>= 9
                possible_moves &= self.spot1
            elif direction == 2:  # Upr right
                possible_moves <<= 7
                possible_moves &= self.spot1

            elif direction == 3:  # Down right
                possible_moves >>= 7
                possible_moves &= self.spot2


            # Keep shifting as long as there are no blocking pieces or we reach the edge of the board
            while not (possible_moves & int(occupied_bitmap)) and possible_moves and possible_moves<self.board_max:
                # Update legal moves bitmap
                legal_moves_bitmap |= possible_moves
                # Further shift in the same direction
                if direction == 0:  # Up
                    possible_moves <<= 9
                    possible_moves &= self.spot2

                elif direction == 1:  # Down
                    possible_moves >>= 9
                    possible_moves &= self.spot1

                elif direction == 2:  # Left
                    possible_moves <<= 7
                    possible_moves &= self.spot1

                elif direction == 3:  # Right
                    possible_moves >>= 7
                    possible_moves &= self.spot2


        return legal_moves_bitmap
    
    def generate_moves(self,pieces,board,hash):
        piece = pieces[2]
        moves = {}
        self.bishop_moves = 0
        while piece:
            square_of_first_knight,piece = self.pop_LSB(piece)
            knight_moves = self.all_posible_moves(square_of_first_knight,board)
            while knight_moves:
                index, knight_moves = self.pop_LSB(knight_moves)
                hash_value = self.update_hash(square_of_first_knight,index,hash)
                moves[hash_value] = {"move": [square_of_first_knight,index,self.name],"score": None,"depth":None,"seen":False}
        return moves

class Knight(Pieces):

    def __init__(self,color,piece_keys_zobras_hasing):
        super().__init__(color,piece_keys_zobras_hasing)
        self.name = 2
        self.piece_keys_zobras_hasing = piece_keys_zobras_hasing
        self.color = color
        self.spot_1_clip = ~(self.clear_file(0) | self.clear_file(1))
        self.spot_2_clip = ~self.clear_file(0)
        self.spot_3_clip = ~self.clear_file(7)
        self.spot_4_clip = ~(self.clear_file(6) | self.clear_file(7))

        self.spot_5_clip = ~(self.clear_file(6) | self.clear_file(7))
        self.spot_6_clip = ~self.clear_file(7)
        self.spot_7_clip = ~self.clear_file(0)
        self.spot_8_clip = ~(self.clear_file(0) | self.clear_file(1))

    def shift_within_range(self,bitboard, shift_amount):
        shifted_board = bitboard << shift_amount
        shift = shifted_board & ((1 << 63)-1)
        return shift

        
    def all_posible_moves(self,index,board):
        bitmap = 1 << index

        spot_1 = self.shift_within_range((bitmap & self.spot_1_clip),6)
        spot_2 = self.shift_within_range((bitmap & self.spot_2_clip),15)
        spot_3 = self.shift_within_range((bitmap & self.spot_3_clip),17)
        spot_4 = self.shift_within_range((bitmap & self.spot_4_clip),10)

        spot_5 = (bitmap & self.spot_5_clip) >> 6
        spot_6 = (bitmap & self.spot_6_clip) >> 15
        spot_7 = (bitmap & self.spot_7_clip) >> 17
        spot_8 = (bitmap & self.spot_8_clip) >> 10

        return (spot_1 | spot_2 | spot_3 | spot_4 | spot_5 | spot_6 | spot_7 | spot_8) & ~board
    
    def generate_moves(self,pieces,board,hash):
        piece = pieces[1]
        moves = {}
        self.knight_moves = 0
        while piece:
            square_of_first_knight,piece = self.pop_LSB(piece)
            knight_moves = self.all_posible_moves(square_of_first_knight,board)

            while knight_moves:
                index, knight_moves = self.pop_LSB(knight_moves)
                hash_value = self.update_hash(square_of_first_knight,index,hash)
                moves[hash_value] = {"move": [square_of_first_knight,index,self.name],"score": None,"depth":None,"seen":False}
        return moves

class Rook(Pieces):
    def __init__(self,color,piece_keys_zobras_hasing):
        super().__init__(color,piece_keys_zobras_hasing)
        self.color = color          
        self.piece_keys_zobras_hasing = piece_keys_zobras_hasing
        self.name = 1
        self.spot1 = ~self.clear_file(7)
        self.spot2 = ~self.clear_file(0)
    def all_posible_moves(self,index, occupied_bitmap):
        # Initialize an empty bitmap to store legal moves
        piece_bitmap = 1 << index   
        legal_moves_bitmap = 0


        # Compute legal moves for each direction using bitwise operations
        for direction in range(4):
            # Compute the possible moves in the current direction
            possible_moves = int(piece_bitmap)
            # Apply the shift corresponding to the current direction
            if direction == 0:  # Up
                possible_moves <<= 8
            elif direction == 1:  # Down
                possible_moves >>= 8
            elif direction == 2:  # Left
                possible_moves <<= 1
                possible_moves &=self.spot2
            elif direction == 3:  # Right
                possible_moves >>= 1
                possible_moves&=self.spot1
            # Keep shifting as long as there are no blocking pieces or we reach the edge of the board
            while not (possible_moves & occupied_bitmap) and possible_moves and possible_moves <self.board_max:
                # Update legal moves bitmap
                legal_moves_bitmap |= possible_moves

                # Further shift in the same direction
                if direction == 0:  # Up
                    possible_moves <<= 8
                elif direction == 1:  # Down
                    possible_moves >>= 8
                elif direction == 2:  # Left
                    possible_moves <<= 1
                    possible_moves&=self.spot2

                elif direction == 3:  # Right
                    possible_moves >>= 1
                    possible_moves&=self.spot1


        return legal_moves_bitmap
    
    def generate_moves(self,pieces,board,hash):
        piece = pieces[0]
        moves = {}
        self.rook_moves = 0
        while piece:
            square_of_first_knight,piece = self.pop_LSB(piece)
            knight_moves = self.all_posible_moves(square_of_first_knight,board)
            while knight_moves:
                index, knight_moves = self.pop_LSB(knight_moves)
                hash_value = self.update_hash(square_of_first_knight,index,hash)
                moves[hash_value] = {"move": [square_of_first_knight,index,self.name],"score": None,"depth":None,"seen":False}
        return moves
    
class Pawn(Pieces):
    def __init__(self,color,piece_keys_zobras_hasing):
        super().__init__(color,piece_keys_zobras_hasing)
        self.piece_keys_zobras_hasing = piece_keys_zobras_hasing
        self.color = color   
        self.name = 4

    def generate_moves(self,moves,hash):
        count = {}
        moves_p = {}
        for coord in moves:
            # Convert the coordinate to a tuple to make it hashable
            coord = moves[coord]["move"][1]
            if not coord in count:
                count.update({coord:1})
            else:
                count[coord]+=1
            if count[coord] == 3:
                hash_value = self.update_hash(None,coord,hash)
                moves_p[hash_value] = {"move": [None,coord,self.name],"score": None,"depth":None,"seen":False}
        moves.update(moves_p)
        return moves
    

        