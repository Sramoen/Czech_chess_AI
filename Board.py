from chessboard import Rook,Bishop,Knight,Pawn
import copy
import time
import numpy as np


class Board:
    def __init__(self,ai_starts=False):
        self.victory = 0
        self.best_move = None
        
        self.pieces_w = [Rook([0,0],1,np.uint8(1)),Rook([7,0],1,np.uint8(2)),
                         Knight([1,0],1,np.uint(3)),Knight([6,0],1,np.uint8(4)),
                         Bishop([2,0],1,np.uint8(5)),Bishop([5,0],1,np.uint8(6)),
                         ]
        self.pieces_b = [Rook([0,7],0,np.uint8(7)),Rook([7,7],0,np.uint8(8)),
                         Knight([1,7],0,np.uint8(9)),Knight([6,7],0,np.uint8(10)),
                         Bishop([2,7],0,np.uint8(11)),Bishop([5,7],0,np.uint8(14)),
                         ]
        self.pawns_w = [Pawn([-1,-1],1,np.uint8(12),False)]
        self.pawns_b = [Pawn([-1,-1],0,np.uint8(13),False)]


        self.iter = 0
        self.depth = None
        self.ai_move = ai_starts
        self.side_to_move = int(not ai_starts)
        
    def make_move(self,move):
        x = move[0]
        y = move[1]
        if move[2] == np.uint8(12):
                self.pieces_w.append(Pawn([x,y],1,np.uint8(12),True))
        elif move[2] == np.uint8(13):    
                self.pieces_b.append(Pawn([x,y],0,np.uint8(13),True))
        else:
            for piece in self.pieces_w+self.pieces_b:         
                if piece.name == move[2]:
                    piece.set_position(x,y)
                    # if piece.name == 10:
                    #     print("Dělám tah černým jezdcem: ",piece._position)
                    break

    def unmake_move(self,name):
        if name == np.uint8(12):
            self.pieces_w.pop()
            return
        elif name == np.uint8(13):
            self.pieces_b.pop()
            return
        for piece in self.pieces_w+self.pieces_b:
            if piece.name == name:
                piece.set_position_unmake(piece.previous_position[-1][0],piece.previous_position[-1][1])
                # if piece.name == 10:

                #     print("Vracím tah černým jezdcem: ",piece._position)

                break
        
    def legal_moves(self,max_player):
        moves = []

        if max_player:
            for piece in self.pieces_w[:6]:
                moves = moves+piece.generate_moves(self.pieces_w+self.pieces_b)
            moves = self.pawns_w[0].generate_moves(moves,max_player)+moves
        else:
            for piece in self.pieces_b[:6]:
                moves = moves+piece.generate_moves(self.pieces_w+self.pieces_b)
            moves = self.pawns_b[0].generate_moves(moves,max_player)+moves
        return moves

    def get_AI_move(self,board,depth,max_player=0):

        self.depth = depth
        print(self.side_to_move)
        root = self.minmax(board, depth,max_player=max_player)
        print(root)
        # self.print_tree(self,root)

        return root,self.iter

    def minmax(self,board,depth=1,max_player=True,alpha=-100000, beta=10000,move=None):
        if board.victory or depth == 0:
            eva = self.eval(move,max_player)
            return eva,None
            
        if max_player: #maximize
                score = -100000
                moves = self.legal_moves(max_player)
                for move in moves:
                    board.make_move(move)
                    evaluation = self.minmax(board,depth-1,False,alpha,beta,move=move)[0]
                    if evaluation > score:
                        score = evaluation
                        if depth==self.depth:
                            self.best_move = move

                    board.unmake_move(move[2])
                    alpha = max(alpha, score)
                    if alpha >= beta:
                        break  # Beta cutoff
                    self.iter+=1
        else:#minimaze
                score = 10000
                moves = self.legal_moves(max_player)
                for move in moves:
                    board.make_move(move)
                    evaluation = self.minmax(board,depth-1,True,alpha,beta,move=move)[0]
                    if evaluation < score:
                        score = evaluation
                        if depth==self.depth:
                            self.best_move = move
                    board.unmake_move(move[2])
                    beta = min(beta, score)
                    if alpha >= beta:
                        break  # Beta cutoff
                    self.iter+=1

        return score,self.best_move

    def eval(self,move,max_player):
        score = 0
        for piece in self.pieces_w:
            if piece.name == np.uint8(12):
                score += 100
        if max_player:
            number_of_moves_w = len(self.legal_moves(max_player))
        else:
            number_of_moves_w = len(self.legal_moves(not max_player))
        for piece in self.pieces_b:
            if piece.name == np.uint8(13):
                score -= 100
        if not max_player:          
            number_of_moves_b = len(self.legal_moves(max_player))
        else:
            number_of_moves_b = len(self.legal_moves(not max_player))
        score += (number_of_moves_w - number_of_moves_b)*10
        return score


if __name__ == "__main__":
    board = Board()
    t1 = time.time()
    root = board.get_AI_move(board,5,max_player=0)
    t2 = time.time()
    print(t2-t1)
    print(root)
    


