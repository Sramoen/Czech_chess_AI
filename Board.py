from chessboard import Rook,Bishop,Knight,Pawn
import copy
import time

# class Board_nodes:
#     def __init__(self,board):
#         self.board = board
#         self.children = []
#         self.recursive_call_count = 0

#     def print_tree(self,node, depth=0):
#         self.recursive_call_count += 1
#         if node is None:
#             return
#         pieces = node.board.pieces_w+node.board.pieces_b
#         # for piece in pieces:
#         #     print(piece.position)
#         # print("--------------------")
#         for child in node.children:
#             self.print_tree(child, depth + 1)
#     def print_rec(self):
#         print(self.recursive_call_count) 

class Board:
    def __init__(self):
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
        self.pawns_w = [Pawn([-1,-1],1,"p1")]
        self.pawns_b = [Pawn([-1,-1],0,"p2")]

    def make_move(self,move):
        x = move[0]
        y = move[1]
        if move[2] == "p1":
                self.pieces_w.append(Pawn([x,y],1,"p1"))
        elif move[2] == "p2":    
                self.pieces_b.append(Pawn([x,y],0,"p2"))
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

    def copy(self,move):
        # Create a new instance of ChessBoard
        new_board = Board()
        
        # Copy primitive attributes
        new_board.side_to_move = self.side_to_move
        new_board.victory = self.victory
        new_board.square = self.square

        # Deep copy lists containing objects
        new_board.pieces_w = copy.deepcopy(self.pieces_w)
        new_board.pieces_b =  copy.deepcopy(self.pieces_w)
        new_board.pawns_w = self.pawns_w
        new_board.pawns_b = self.pawns_b
        self.make_move(move)
        return new_board
        
    def legal_moves(self,max_player):
        moves = []

        if max_player:
            for piece in self.pieces_w+self.pawns_w:
                for i in range(8):
                    for j in range(8):
                        if piece.check_move(i,j,self.pieces_w+self.pieces_b):
                            moves.append([i,j,piece.name])
        else:
            for piece in self.pieces_b+self.pawns_b:
                for i in range(8):
                    for j in range(8):
                        if piece.check_move(i,j,self.pieces_w+self.pieces_b):
                            moves.append([i,j,piece.name])
        return moves

    def generate_moves(self,max_player):
        legal_moves = self.legal_moves(max_player)
        return legal_moves
            # # print(depth)
            # for move in legal_moves:
            #     # print(node.board)
            #     child_board = node.board.copy(move)
            #     child_node = Board_nodes(child_board)
            #     node.children.append(child_node)
                # self.generate_moves(child_node, depth - 1)


    def get_AI_move(self,board,depth=1):
        root = self.minmax(board, depth)

        # self.print_tree(self,root)

        return root

    def minmax(self,board,depth=1,max_player=True,best_score=None):
        if board.victory or depth == 0:
            eva = self.eval()
            return eva,None
            
        if max_player: #maximize
                score = -100000
                moves = self.generate_moves(max_player)
                for move in moves:
                    board.make_move(move)
                    evaluation = self.minmax(board,depth-1,False)[0]
                    if evaluation >= score:
                        score = evaluation
                        self.best_move = move

                    board.unmake_move(move[2])
        else:#minimaze
                score = 10000
                moves = self.generate_moves(max_player)
                for move in moves:
                    board.make_move(move)
                    evaluation = self.minmax(board,depth-1,True)[0]
                    if evaluation < score:
                        score = evaluation


                    board.unmake_move(move[2])
        return score,self.best_move

    def eval(self):
        score = 0
        for piece in self.pieces_w:
            if piece.name == "p1":
                score += 100
        for piece in self.pieces_b:
            if piece.name == "p2":
                score -= 100
        return score


if __name__ == "__main__":
    board = Board()
    t1 = time.time()
    root = board.get_AI_move(board,2)
    t2 = time.time()
    print(t2-t1)
    print(root)
    


