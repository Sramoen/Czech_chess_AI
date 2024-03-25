from chessboard import Rook,Bishop,Knight,Pawn
from numba import jit,uint64 
import time
import numpy as np
import concurrent.futures
import random
import gmpy2
class Board:
    def __init__(self,ai_starts=False):
        self.victory = 0
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

    def calculate_hash(self):
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
        # XOR out the Zobrist key for the piece at the "from" square

        if from_square_index is not None:
            # print(self.piece_keys_zobras_hasing[piece][from_square_index])
            self.hash_value ^= self.piece_keys_zobras_hasing[piece][from_square_index]
        if to_square_index is not None:
            # print(self.piece_keys_zobras_hasing[piece][from_square_index])
            # XOR in the Zobrist key for the piece at the "to" square
            self.hash_value ^= self.piece_keys_zobras_hasing[piece][to_square_index]
            # XOR side_to_move
        if max_player:
            self.hash_value ^= 1


    def get_all_pieces_bitboard(self):
        # Flatten the board_rep array and apply bitwise OR operation along the first axis
        white_pieces_bitboard = self.rooks_w|self.knight_w|self.bishop_w|self.pawn_w
        black_pieces_bitboard = self.rooks_b|self.knight_b|self.bishop_b|self.pawn_b
        all_pieces_bitboard = white_pieces_bitboard|black_pieces_bitboard
        return all_pieces_bitboard
    
    def update_bitboard(self,mask,move):
        self.previous_bitboard_piece.append(mask)
        mask &= ~(1 << move[0])

        mask |= (1<<move[1])
        return mask
    
    def make_move(self,move,max_player):
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
        moves = []
        all_pieces_bitboard = self.get_all_pieces_bitboard()
        if max_player:
            for piece in self.pieces_w[:-1]:
                moves = moves+piece.generate_moves([self.rooks_w,self.knight_w,self.bishop_w,self.pawn_w]
                                                   ,all_pieces_bitboard)
            moves = self.pieces_w[-1].generate_moves(moves)+moves
        else:
            for piece in self.pieces_b[:-1]:
                moves = moves+piece.generate_moves([self.rooks_b,self.knight_b,self.bishop_b,self.pawn_b]
                                                   ,all_pieces_bitboard)
            moves = self.pieces_b[-1].generate_moves(moves)+moves
        return moves

    def get_AI_move(self,board,depth,max_player=0):
 
        self.previous_bitboard_piece = []
        self.transposition_table = {}
        self.iter = 0

        self.depth = depth
        root = self.minmax(board, depth,max_player=max_player)
        self.make_move(root[1],0)

        return root,self.iter
    

    def minmax(self,board,depth=1,max_player=True,alpha=-100000, beta=10000,move=None):
        if depth == 0:
            eva = self.eval()
            return eva,None
            
        if max_player: #maximize
                score = -100000
                moves_w = self.legal_moves(max_player)
                self.moves_w = moves_w
                for move in moves_w:
                    board.make_move(move,max_player)
                    temp = self.check_hashes(depth)
                    if temp[0]:
                        evaluation = temp[1]
                        if evaluation < score:
                            score = evaluation
                            if depth==self.depth:
                                self.best_move = move
                        board.unmake_move(max_player,move)
                        alpha = max(alpha, score)
                        if alpha >= beta:
                            break  # Beta cutoff
                        self.iter+=1
                        continue
                    if self.check_victory_w():
                          print(bin(self.pawn_w))
                          board.unmake_move(max_player,move)
                          score = 100000
                          self.best_move = move

                          return score,self.best_move

                    evaluation = self.minmax(board,depth-1,False,alpha,beta,move=move)[0]

                    if evaluation > score:
                        score = evaluation
                        if depth==self.depth:
                            self.best_move = move
                    self.add_hash_to_trans_table(temp[1],evaluation,depth)
                    board.unmake_move(max_player,move)
                    alpha = max(alpha, score)
                    if alpha >= beta:
                        break  # Beta cutoff
                    self.iter+=1
        else:#minimaze
                score = 10000
                moves_b = self.legal_moves(max_player)
                self.moves_b = moves_b

                for move in moves_b:
                    board.make_move(move,max_player)
                    temp = self.check_hashes(depth)
                    if temp[0]:
                        evaluation = temp[1]
                        if evaluation < score:
                            score = evaluation
                            if depth==self.depth:
                                self.best_move = move
                        board.unmake_move(max_player,move)
                        beta = min(beta, score)
                        if alpha >= beta:
                            break  # Beta cutoff
                        self.iter+=1
                        continue
                    if self.check_victory_b():
                          board.unmake_move(max_player,move)
                          score = -100000
                          self.best_move = move
                          return score,self.best_move
                    evaluation = self.minmax(board,depth-1,True,alpha,beta,move=move)[0]
                    
                    if evaluation < score:
                        score = evaluation
                        if depth==self.depth:
                            self.best_move = move
                    self.add_hash_to_trans_table(temp[1],evaluation,depth)
                    board.unmake_move(max_player,move)
                    beta = min(beta, score)
                    if alpha >= beta:
                        break  # Beta cutoff
                    self.iter+=1

        return score,self.best_move



    def check_hashes(self,depth):

        # Retrieve an entry
        retrieved_entry = self.transposition_table.get(self.hash_value)
        if retrieved_entry:
            if retrieved_entry["depth"] >= depth: 
                return True,retrieved_entry["score"],retrieved_entry["depth"]
        return False,self.hash_value,None

    def check_victory_w(self):
        if self.count_pawns(self.pawn_w) == 8:
            return True
        return False
    def check_victory_b(self):
        if self.count_pawns(self.pawn_b) == 8:
            return True
        return False
    def add_hash_to_trans_table(self,hash,evaluation,depth):
        self.transposition_table[hash] = {"score": evaluation,"depth":depth}

    def count_pawns(self,pawns):
        pawns = pawns
        count = 0
        while pawns > 0:
            count = count + 1
            pawns = pawns & (pawns-1)
        return count

    def eval(self):
        score = 0
        score += self.count_pawns(self.pawn_w)
        score -= self.count_pawns(self.pawn_b)
        score*=100
        legal_moves_w = self.legal_moves(1)
        legal_moves_b = self.legal_moves(0) 
        score += ((len(legal_moves_w)-len(legal_moves_b))*8)
        # score += ((len(legal_moves_w)-len(self.moves_w)-len(legal_moves_b)+len(self.moves_b))*20)
        # for move in legal_moves_w:
        #     if move[2]==4:
        #         score+=50
        # for move in legal_moves_b:
        #     if move[2]==4:
        #         score-=50
        return score


if __name__ == "__main__":
    board = Board()
    t1 = time.time()
    root = board.get_AI_move(board,5,max_player=0)
    t2 = time.time()
    print(t2-t1)
    print(root)
    


