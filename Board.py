from chessboard import Rook,Bishop,Knight,Pawn
import copy
import time


class Board:
    def __init__(self,ai_starts=False):
        self.victory = 0
        self.square = 1
        self.best_move = None
        
        self.pieces_w = [Rook([0,0],1,"r1"),Rook([7,0],1,"r2"),
                         Knight([1,0],1,"k1"),Knight([6,0],1,"k2"),
                         Bishop([2,0],1,"b1"),Bishop([5,0],1,"b2"),
                         ]
        self.pieces_b = [Rook([0,7],0,"r3"),Rook([7,7],0,"r4"),
                         Knight([1,7],0,"k3"),Knight([6,7],0,"k4"),
                         Bishop([2,7],0,"b3"),Bishop([5,7],0,"b4"),
                         ]
        self.pawns_w = [Pawn([-1,-1],1,"p1",False)]
        self.pawns_b = [Pawn([-1,-1],0,"p2",False)]


        self.iter = 0
        self.depth = None
        self.ai_move = ai_starts
        self.side_to_move = int(not ai_starts)
        self.moves=None
        self.best_score_w = None
        self.best_score_b = None
    def make_move(self,move):
        x = move[0]
        y = move[1]
        if move[2] == "p1":
                self.pieces_w.append(Pawn([x,y],1,"p1",True))
        elif move[2] == "p2":    
                self.pieces_b.append(Pawn([x,y],0,"p2",True))
        else:
            for piece in self.pieces_w+self.pieces_b:         
                if piece.name == move[2]:
                    piece.set_position(x,y)
                    break
    def unmake_move(self,name):
        if name == "p1":
            self.pieces_w.pop()
        elif name == "p2":
            self.pieces_b.pop()
        for piece in self.pieces_w+self.pieces_b:
            if piece.name == name:
                piece.set_position(piece.previous_position[0],piece.previous_position[1])
                break
        
    def legal_moves(self,max_player):
        moves = []

        if max_player:
            for piece in self.pawns_w+self.pieces_w[:6]:
                for i in range(8):
                    for j in range(8):
                        if piece.check_move(i,j,self.pieces_w+self.pieces_b):
                            moves.append([i,j,piece.name])
        else:
            for piece in self.pawns_b+self.pieces_b[:6]:
                for i in range(8):
                    for j in range(8):
                        if piece.check_move(i,j,self.pieces_w+self.pieces_b):
                            moves.append([i,j,piece.name])
        return moves

    def get_AI_move(self,board,depth=1):
        self.depth = depth
        print(self.side_to_move)
        root = self.minmax(board, depth,max_player=0)
        print(root)
        # self.print_tree(self,root)

        return root,self.iter

    def minmax(self,board,depth=1,max_player=True,alpha=-10000, beta=10000,move=None):
        if board.victory or depth == 0:
            eva = self.eval(move,max_player)
            return eva,None
            
        if max_player: #maximize
                score = -100000
                moves = self.legal_moves(max_player)
                for move in moves:
                    board.make_move(move)
                    evaluation = self.minmax(board,depth-1,False,alpha=-10000,beta=10000,move=move)[0]
                    if evaluation > score:
                        score = evaluation
                    if evaluation >= score and depth==self.depth:
                        self.best_move = move

                    board.unmake_move(move[2])
                    # alpha = max(alpha, score)
                    # if alpha >= beta:
                    #     break  # Beta cutoff
                    self.iter+=1
        else:#minimaze
                score = 10000
                moves = self.legal_moves(max_player)
                for move in moves:
                    board.make_move(move)
                    evaluation = self.minmax(board,depth-1,True,alpha=-10000,beta=10000,move=move)[0]
                    if evaluation < score:
                        score = evaluation
                    if evaluation <= score and depth==self.depth:
                        self.best_move = move
                    board.unmake_move(move[2])
                    # alpha = max(alpha, score)
                    # if alpha >= beta:
                    #     break  # Beta cutoff
                    self.iter+=1

        return score,self.best_move

    def eval(self,move,max_player):
        score = 0
        for piece in self.pieces_w:
            if piece.name == "p1":
                score += 100
            if max_player:
                number_of_moves_w = len(self.legal_moves(max_player))
            else:
                number_of_moves_w = len(self.legal_moves(not max_player))
        for piece in self.pieces_b:
            if piece.name == "p2":
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
    root = board.get_AI_move(board,2)
    t2 = time.time()
    print(t2-t1)
    print(root)
    


