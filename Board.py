from chessboard import Rook,Bishop,Knight,Pawn
import time
import numpy as np
import random
import random


INF = float('inf')


class Board:
    """Class for board representation for AI"""

    def __init__(self,ai_starts=False):
        """
        Initialize chess board

        Args:
            ai_starts (bool): False (default) if AI play as black.
        """
        self.best_move = None
        
        self.rooks_w = int(0)
        self.rooks_w |= 1 << 63  # h1 
        self.rooks_w |= 1 << 56  # a1 

        self.rooks_b = int(0)
        self.rooks_b |= 1 << 0  # h8 
        self.rooks_b |= 1 << 7  # a8 
        
        self.knight_w = int(0)
        self.knight_w |= 1 << 62  # g1 
        self.knight_w |= 1 << 57  # b1 
        self.knight_b = int(0)
        self.knight_b|= 1 << 1  # g8
        self.knight_b|= 1 << 6  #  b8

        self.bishop_w = int(0)
        self.bishop_w|= 1 << 61  # f1 
        self.bishop_w|= 1 << 58  # c1 
        self.bishop_b = int(0)
        self.bishop_b|= 1 << 2  # f8
        self.bishop_b|= 1 << 5  # c8 

        self.pawn_w = int(0) #0
        self.pawn_b = int(0) #0

        self.previous_bitboard_piece = []

        self.pieces_w = [Rook(True),Knight(True),Bishop(True),Pawn(True)]
        self.pieces_b = [Rook(False),Knight(False),Bishop(False),Pawn(False)]

        self.piece_keys_zobras_hasing = {
            1: [random.randint(0, 2**64 - 1) for _ in range(64)],
            2: [random.randint(0, 2**64 - 1) for _ in range(64)],
            3: [random.randint(0, 2**64 - 1) for _ in range(64)],
            4: [random.randint(0, 2**64 - 1) for _ in range(64)],
            5: [random.randint(0, 2**64 - 1) for _ in range(64)],
            6: [random.randint(0, 2**64 - 1) for _ in range(64)],
            7: [random.randint(0, 2**64 - 1) for _ in range(64)],
            8: [random.randint(0, 2**64 - 1) for _ in range(64)]
        }
        self.iter = 0
        self.depth = None
        self.ai_move = ai_starts
        self.side_to_move = int(not ai_starts)
        self.moves_b = None
        self.moves_w = None
        self.hash_value = self.calculate_hash()
        self.transposition_table = {}
        self.history_table = {}

    def calculate_hash(self):
        """
        Calculate hash of initial position with zobrist hashing.
        """
        hash_value = 0
        for piece, bitboard in [(1, self.rooks_w), (5, self.rooks_b), 
                                (2, self.knight_w), (6, self.knight_b), 
                                (3, self.bishop_w), (7,self.bishop_b),
                                (4,self.pawn_w),(8,self.pawn_b)]:
            for square_index in range(64):
                if bitboard & (1 << square_index):
                    hash_value ^= self.piece_keys_zobras_hasing[piece][square_index]
        if self.side_to_move:
            hash_value ^= 1
        return hash_value
    
    def update_hash(self,piece,from_square_index,to_square_index,max_player):
        """
        Update hash after move was made.
        Args:
            piece (int): Which piece is updated.
            from_square_index (int): From which square piece moved.
            to_square_index (int): To which square piece moved.
            max_player (bool): if maximazing player is on the move.

        """
        #Made XOR operation if not none (no pawns), move from which piece moved is set to zero in hash
        if from_square_index is not None:
            self.hash_value ^= self.piece_keys_zobras_hasing[piece][from_square_index]
            #Made XOR operation if not none (no pawns when unmake move),
            # to square which piece moved is set to one in hash
        if to_square_index is not None:
            self.hash_value ^= self.piece_keys_zobras_hasing[piece][to_square_index]
            # XOR side_to_move
        if max_player:
            self.hash_value ^= 1


    def get_all_pieces_bitboard(self):
        """
        Flatten the board_rep array and apply bitwise OR operation along the first axis
        """
        white_pieces_bitboard = self.rooks_w|self.knight_w|self.bishop_w|self.pawn_w
        black_pieces_bitboard = self.rooks_b|self.knight_b|self.bishop_b|self.pawn_b
        all_pieces_bitboard = white_pieces_bitboard|black_pieces_bitboard
        return all_pieces_bitboard
    
    def update_bitboard(self,mask,move):
        """
        Update bitboard.
        Args:
            mask(int): bitboard which has to change.
            move(list,tuple): Move which is updated.
        """
        self.previous_bitboard_piece.append(mask)
        #Remove from_square index to biboard
        mask &= ~(1 << move[0])
        #Put to_square index to bitboard
        mask |= (1<<move[1])
        return mask
    
    def make_move(self,move,max_player):
        """
        Make move on board.
        Args:
            max_player(bool): True if maximizing player.
            move(list,tuple): Move which is updated.
        """
        if max_player:
            if move[2] == 4:
                self.previous_bitboard_piece.append(self.pawn_w)
                self.pawn_w |= (1 << move[1])
                self.update_hash(4,None,move[1],max_player)
            elif move[2] ==3:
                self.bishop_w = self.update_bitboard(self.bishop_w,move)
                self.update_hash(3,move[0],move[1],max_player)

            elif move[2] ==2:
                self.knight_w = self.update_bitboard(self.knight_w,move)
                self.update_hash(2,move[0],move[1],max_player)

            elif move[2] ==1:
                self.rooks_w = self.update_bitboard(self.rooks_w,move)
                self.update_hash(1,move[0],move[1],max_player)
                
        else:
            
            if move[2] == 4:
                self.previous_bitboard_piece.append(self.pawn_b)
                self.pawn_b |= (1 << move[1])
                self.update_hash(8,None,move[1],max_player)
            
            elif move[2] ==3:
                self.bishop_b = self.update_bitboard(self.bishop_b,move)
                self.update_hash(7,move[0],move[1],max_player)
            elif move[2] ==2:
                self.knight_b = self.update_bitboard(self.knight_b,move)
                self.update_hash(6,move[0],move[1],max_player)
            elif move[2] ==1:
                self.rooks_b = self.update_bitboard(self.rooks_b,move)
                self.update_hash(5,move[0],move[1],max_player)

    def unmake_move(self,max_player,move):
        """
        Unmake move on board.
        Args:
            max_player(bool): True if maximizing player.
            move(list,tuple): Move which is updated.
        """
        if max_player:
            if move[2] == 4:
                self.update_hash(4,move[1],move[0],max_player)
                self.pawn_w = self.previous_bitboard_piece.pop()   
            elif move[2] ==3:
                self.update_hash(3,move[1],move[0],max_player)
                self.bishop_w = self.previous_bitboard_piece.pop()
            elif move[2] ==2:
                self.update_hash(2,move[1],move[0],max_player)
                self.knight_w = self.previous_bitboard_piece.pop()
            elif move[2] ==1:
                self.update_hash(1,move[1],move[0],max_player)
                self.rooks_w = self.previous_bitboard_piece.pop()
        else:
            if move[2] == 4:
                self.update_hash(8,move[1],move[0],max_player)
                self.pawn_b = self.previous_bitboard_piece.pop()
            elif move[2] ==3:
                self.update_hash(7,move[1],move[0],max_player)
                self.bishop_b = self.previous_bitboard_piece.pop()
            elif move[2] ==2:
                self.update_hash(6,move[1],move[0],max_player)
                self.knight_b = self.previous_bitboard_piece.pop()
            elif move[2] ==1:
                self.update_hash(5,move[1],move[0],max_player)
                self.rooks_b = self.previous_bitboard_piece.pop()
        
    def legal_moves(self,max_player):
        """
        Get all possible moves.
        Args:
            max_player(bool): True if maximizing player.
        """
        moves = []
        all_pieces_bitboard = self.get_all_pieces_bitboard()
        if max_player:
            #Generate moves for each piece except pawn
            for piece in self.pieces_w[:-1]:
                moves = moves+piece.generate_moves([self.rooks_w,self.knight_w,self.bishop_w,self.pawn_w]
                                                   ,all_pieces_bitboard)
            #Generate moves for pawn
            moves = self.pieces_w[-1].generate_moves(moves)+moves
        else:
            for piece in self.pieces_b[:-1]:
                #Generate moves for each piece except pawn
                moves = moves+piece.generate_moves([self.rooks_b,self.knight_b,self.bishop_b,self.pawn_b]
                                                   ,all_pieces_bitboard)
            #Generate moves for pawn
            moves = self.pieces_b[-1].generate_moves(moves)+moves
        # moves = self.sort_moves(moves)
        return moves
    def sort_moves(self,moves):
        moves1 = sorted(moves, key=self.custom_sort)
        return moves1

    def custom_sort(self,sublist):
        if tuple(sublist) in self.history_table:
            return 0  # Sublist is in the dictionary, sort it first
        else:
            return 1  # Sublist is not in the dictionary, sort it later


    def get_AI_move(self,board,depth,max_player=0):
        """
        Get best move by AI in current position.

        Args:
            board(Board): board, where move should be generated.
            depth(int): max depth of search.
            max_player(bool): False (default) if AI plays as black.
        """
        #Reset previous positions of pieces and transposition table 
        self.previous_bitboard_piece = []
        self.transposition_table = {}
        self.iter = 0

        self.depth = depth
        root = self.minmax(board, depth,max_player=max_player)
        self.make_move(root[1],0)

        return root,self.iter
    

    def minmax(self,board,depth=1,max_player=True,alpha=-INF, beta=INF,move=None):
        """
        Minimax algorithm.

        Args:
            board(Board): board, where move should be generated.
            depth(int): depth of search.
            max_player(bool): False (default) if AI plays as black.
            alpha(float): alpha for alpha beta prunning default(-INF).
            beta(float): beta for alpha beta prunning default(INF).
            move(list,tuple): move returned by minmax node, default(None).
        """
        if depth == 0:
            eva = self.eval(max_player)
            return eva,None
            
        if max_player: #maximize
                score = -INF

                #Get all legal moves
                moves_w = self.legal_moves(max_player)
                self.moves_w = moves_w
                for move in moves_w:
                    #make move on board
                    board.make_move(move,max_player)
                    #Check if hash in transpostion table
                    temp = self.check_hashes(depth)
                    if temp[0]:
                        #Get evaluation of already searched move
                        evaluation = temp[1]
                        if evaluation < score:
                            score = evaluation
                            if depth==self.depth:
                                self.best_move = move
                        #Unmake move
                        board.unmake_move(max_player,move)
                        #Try alpha beta prunning or continue
                        alpha = max(alpha, score)
                        if alpha >= beta:
                            # self.update_history(move,depth,max_player)
                            break  # Beta cutoff
                        self.iter+=1
                        continue
                
                    if self.check_victory_w():
                          board.unmake_move(max_player,move)
                          score = INF
                          self.best_move = move
                          return score,self.best_move

                    #Recurtion
                    evaluation = self.minmax(board,depth-1,False,alpha,beta,move=move)[0]

                    #Update evaluation and best move
                    if evaluation > score:
                        score = evaluation
                        if depth==self.depth:
                            self.best_move = move
                    #Update transpostion table
                    self.add_hash_to_trans_table(temp[1],evaluation,depth)
                    #Unmake move
                    board.unmake_move(max_player,move)
                    #Try alpha beta prunning
                    alpha = max(alpha, score)
                    if alpha >= beta:
                        # self.update_history(move,depth,max_player)
                        break  # Beta cutoff
                    self.iter+=1
        else:#minimaze
                score = INF
                #Get all legal moves

                moves_b = self.legal_moves(max_player)
                self.moves_b = moves_b

                for move in moves_b:
                    #make move on board
                    board.make_move(move,max_player)
                    #Check if hash in transpostion table
                    temp = self.check_hashes(depth)
                    if temp[0]:
                        #Get evaluation of already searched move and uppdate score
                        evaluation = temp[1]
                        if evaluation < score:
                            score = evaluation
                            if depth==self.depth:
                                self.best_move = move
                        #Unmake move
                        board.unmake_move(max_player,move)
                        beta = min(beta, score)
                        #Try alpha beta prunning or continue
                        if alpha >= beta:
                            # self.update_history(move,depth,max_player)
                            break  # Beta cutoff
                        self.iter+=1
                        continue
                    if self.check_victory_b():
                          board.unmake_move(max_player,move)
                          score = -INF
                          self.best_move = move
                          return score,self.best_move
                    #Recursiton
                    evaluation = self.minmax(board,depth-1,True,alpha,beta,move=move)[0]
                    #Update score if nessacery
                    if evaluation < score:
                        score = evaluation
                        if depth==self.depth:
                            self.best_move = move
                    #Update transposition table
                    self.add_hash_to_trans_table(temp[1],evaluation,depth)
                    board.unmake_move(max_player,move)
                    #Try alpha beta prunning
                    beta = min(beta, score)
                    if alpha >= beta:
                        # self.update_history(move,depth,max_player)
                        break  # Beta cutoff
                    self.iter+=1

        return score,self.best_move
    
    def update_history(self, move, depth,max_player):
        move_tup = tuple(move)
        if move_tup in self.history_table:
            self.history_table[move_tup] += depth * depth
        else:
            self.history_table[move_tup] = depth * depth

    def check_hashes(self,depth):
        """
        Check if current hash is in the transposition table.
        
        Args:
            depth(int): depth of search.
        """
        # Retrieve an entry
        retrieved_entry = self.transposition_table.get(self.hash_value)
        if retrieved_entry:
            if retrieved_entry["depth"] >= depth: 
                return True,retrieved_entry["score"],retrieved_entry["depth"]
        return False,self.hash_value,None

    def check_victory_w(self):
        """
        Check if white won.
        """
        if self.count_pawns(self.pawn_w) == 8:
            return True
        return False
    def check_victory_b(self):
        """
        Check if black won.
        """
        if self.count_pawns(self.pawn_b) == 8:
            return True
        return False
    def add_hash_to_trans_table(self,hash,evaluation,depth):
        """Add hash to transposition table.
        
        Args:
            hash(int): Zobrist hash of current position.
            evaluation(int): Evaluation of current position.
            depth(int): depth of search.
        """
        self.transposition_table[hash] = {"score": evaluation,"depth":depth}

    def count_pawns(self,pawns):
        """Count number of pawns in bitboard
        
            Args:
                pawns(int): bitboard of pawns
        """
        pawns = pawns
        count = 0
        while pawns > 0:
            count = count + 1
            pawns = pawns & (pawns-1)
        return count

    def eval(self,max_player):
        """Evaluate current state of board.
        
            Args:
                max_player(bool): False if minimazing player True otherwise.
        """
        score = 0
        #First part of evaluation - count pawns
        score += self.count_pawns(self.pawn_w)
        score -= self.count_pawns(self.pawn_b)
        score*=100

        #Second part of evaluation - mobility - count number of moves for each side
        legal_moves_w = self.legal_moves(1)
        legal_moves_b = self.legal_moves(0) 
        score += ((len(legal_moves_w)-len(legal_moves_b))*8)

        #Third part of evaluation - is mobility better than before move?
        if max_player:
            score += (10*(len(legal_moves_w)-len(self.moves_w)))
        else:
            score -= (10*(len(legal_moves_b)-len(self.moves_b)))

        #Foruth part of evaluation - How many pawns you can make?
        for move in legal_moves_w:
            if move[2]==4:
                score+=20
        for move in legal_moves_b:
            if move[2]==4:
                score-=20
        return score


if __name__ == "__main__":
    board = Board()
    t1 = time.time()
    root = board.get_AI_move(board,5,max_player=0)
    t2 = time.time()
    print(t2-t1)
    print(root)
    


