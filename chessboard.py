
class Pieces():
    """Class for AI pieces."""

    def __init__(self,color):
        """
        Initialize piece.

        Args:
            color (bool): False (default) black piece.
        """
        self.color = color
        self.board_max = 2**64

    def pop_LSB(self,b):
        """Pop least significant bit and return index and changed bitboard.
        
        Args:
            b(int): bitboard.
        """
        index = (b & -b).bit_length() - 1
        b &= b - 1
        return index,b
    
    def clear_file(self,file):
        """Clear file (horizontal) and return it.
        
            Args:
                file(int): file which should be cleared.
        """
        return 0x0101010101010101 << file 
    
class Bishop(Pieces):
    """Class for represeting bishop."""
    def __init__(self,color):
        """Initialize bishop.
            Args:
                color(bool): color of bishop.
        """
        super().__init__(color)             
        self.name = 3
        self.spot1 = ~self.clear_file(7)
        self.spot2 = ~self.clear_file(0)

    def all_posible_moves(self,index, occupied_bitmap):
        """Get all possible moves of bishop.
            Args:
                index(int): index of starting position.
                occupied_bitmap(int): bitmap of all pieces in current board.
        """
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
    
    def generate_moves(self,pieces,board):
        """Generate all possible moves of piece.
            Args:
                pieces(list,tuple): List of bitmaps for pieces.
                board(int): all pieces bitmap.
        """
        piece = pieces[2]
        moves = []
        self.bishop_moves = 0
        while piece:
            square_of_first_bishop,piece = self.pop_LSB(piece)
            bishop_moves = self.all_posible_moves(square_of_first_bishop,board)
            while bishop_moves:
                index, bishop_moves = self.pop_LSB(bishop_moves)
                moves.append([square_of_first_bishop,index,self.name])
        return moves

class Knight(Pieces):
    """Class for represeting knight."""

    def __init__(self,color):
        """Initialize Knight.
            Args:
                color(bool): color of Knight.
        """
        super().__init__(color)
        self.name = 2
        self.spot_1_clip = ~(self.clear_file(0) | self.clear_file(1))
        self.spot_2_clip = ~self.clear_file(0)
        self.spot_3_clip = ~self.clear_file(7)
        self.spot_4_clip = ~(self.clear_file(6) | self.clear_file(7))

        self.spot_5_clip = ~(self.clear_file(6) | self.clear_file(7))
        self.spot_6_clip = ~self.clear_file(7)
        self.spot_7_clip = ~self.clear_file(0)
        self.spot_8_clip = ~(self.clear_file(0) | self.clear_file(1))

    def shift_within_range(self,bitboard, shift_amount):
        """Shift knight if possible (still on board).
            Args:
                bitboard(int): bitboard of knight.
                shift_amount(int): how much shift.
        """
        shifted_board = bitboard << shift_amount
        shift = shifted_board & ((1 << 63)-1)
        return shift

        
    def all_posible_moves(self,index,board):
        """Get all possible moves of knight.
            Args:
                index(int): index of starting position.
                occupied_bitmap(int): bitmap of all pieces in current board.
        """
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
    
    def generate_moves(self,pieces,board):
        """Generate all possible moves of piece.
            Args:
                pieces(list,tuple): List of bitmaps for pieces.
                board(int): all pieces bitmap.
        """
        piece = pieces[1]
        moves = []
        self.knight_moves = 0
        while piece:
            square_of_first_knight,piece = self.pop_LSB(piece)
            knight_moves = self.all_posible_moves(square_of_first_knight,board)

            while knight_moves:
                index, knight_moves = self.pop_LSB(knight_moves)
                moves.append([square_of_first_knight,index,self.name])
        return moves

class Rook(Pieces):
    """Class for represeting knight."""

    def __init__(self,color):
        """Initialize Rook.
            Args:
                color(bool): color of Rook.
        """
        super().__init__(color)          
        self.name = 1
        self.spot1 = ~self.clear_file(7)
        self.spot2 = ~self.clear_file(0)
    def all_posible_moves(self,index, occupied_bitmap):
        """Get all possible moves of rook.
            Args:
                index(int): index of starting position.
                occupied_bitmap(int): bitmap of all pieces in current board.
        """
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
    
    def generate_moves(self,pieces,board):
        """Generate all possible moves of piece.
            Args:
                pieces(list,tuple): List of bitmaps for pieces.
                board(int): all pieces bitmap.
        """
        piece = pieces[0]
        moves = []
        self.rook_moves = 0
        while piece:
            square_of_first_rook,piece = self.pop_LSB(piece)
            rook_moves = self.all_posible_moves(square_of_first_rook,board)
            while rook_moves:
                index, rook_moves = self.pop_LSB(rook_moves)
                moves.append([square_of_first_rook,index,self.name])
        return moves
    
class Pawn(Pieces):
    """Class for representing pawn."""
    def __init__(self,color):
        super().__init__(color)
        """Initialize Pawn.
            Args:
                color(bool): color of Pawn.
        """   
        self.name = 4

    def generate_moves(self,moves):
        """Generate all possible moves of pawn.
            Args:
            moves(list,tuple): all moves from other pieces.
        """
        count = {}
        triplets = []
        for coord in moves:
            # Convert the coordinate to a tuple to make it hashable
            coord_tuple = coord[1]
            count[coord_tuple] = count.get(coord_tuple, 0) + 1
            #If square is attacked three times - append move
            if count[coord_tuple] == 3:
                triplets.append([None,coord[1],self.name])
        return triplets
    

        