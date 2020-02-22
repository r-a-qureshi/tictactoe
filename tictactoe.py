import numpy as np
import random
from copy import deepcopy

class InvalidMoveError(Exception):
    pass
class OccupiedSpaceError(InvalidMoveError):
    pass
class IncorrectMarkError(Exception):
    pass

class Board():
    def __init__(self,dim=3):
        self.dim=dim
        self.gameboard = np.tile('_',[dim,dim])
    def place_move(self,mark:str,loc:tuple):
        if loc not in self.remaining_moves():
            raise InvalidMoveError('Move is not possible')
        if mark not in ['X','O']:
            raise IncorrectMarkError('Mark must be X or O')
        if self.gameboard[loc[0],loc[1]] == '_':
            self.gameboard[loc[0],loc[1]] = mark
        else:
            raise OccupiedSpaceError(
                f'Selected space already contains {self.gameboard[loc[0],loc[1]]}'
            )
    def remaining_moves(self):
        return(
            tuple(zip(*np.where(self.gameboard=='_')))
        )
    def winning(self,mark):
        board = self.gameboard==mark
        win_states = np.hstack(
            [
                np.all(board,axis=0),
                np.all(board,axis=1),
                np.all(np.diag(board)),
                np.all(np.diag(np.fliplr(board)))
            ]
        )
        return(np.any(win_states))
    def is_end_state(self):
        if self.winning('X'):
            return(True,'X','X wins!')
        elif self.winning('O'):
            return(True,'O','O wins!')
        elif np.any(self.gameboard == '_') == False:
            return(True,'Draw!','Draw!')
        else:
            return(False,'','')
    def reset(self):
        self.gameboard = np.tile('_',[self.dim,self.dim])
    def __repr__(self):
        return('\n'.join(['Tic Tac Toe Board',self.gameboard.__repr__()]))

class Player():
    def __init__(self,mark,ttt_board):
        self.mark=mark
        self.ttt_board = ttt_board

class RandomPlayer(Player):
    def get_move(self):
        print(f'Random player ({self.mark}) move')
        return(random.choice(self.ttt_board.remaining_moves()))

class HumanPlayer(Player):
    def get_move(self):
        player_move = (-1,-1)
        self.failed = False
        while player_move not in self.ttt_board.remaining_moves():
            if self.failed:
                print('Invalid Move')
            player_move = input(f'Place {self.mark} where? X,Y\n')
            player_move = tuple([int(i) for i in player_move.split(',')])
            self.failed = True
        return(player_move)

class MiniMaxPlayer(Player):
    def get_move(self):
        board = deepcopy(self.ttt_board)
        print(f'CPU player ({self.mark}) move')
        if np.all(self.ttt_board.gameboard == '_'):
            # optimal first move is the corners, hardcode this to save
            # time searching all possible tic tac toe games
            if self.ttt_board.dim == 3:
                return(random.choice([(0,0),(0,2),(2,0),(2,2)]))
            else:
                return((0,0))
        else:
            return(minimax(board,self.mark,self.mark)[0])

def minimax(board,player,max_player,depth=0,move=None):
    other_player = {'X':'O','O':'X'}
    game_over,winner,_ =  board.is_end_state()
    if game_over:
        if winner == max_player:
            return((move,10-depth))
        elif winner != 'Draw!':
            # min player
            return((move,-10+depth))
        else:
            # tie game
            return((move,0))
    if player == max_player:
        best_score = -1000
        min_or_max = max
    else:
        best_score = 1000
        min_or_max = min
    
    for move in board.remaining_moves():
        board_ = deepcopy(board)
        board_.place_move(player,move)
        _,score = minimax(
            board_,
            other_player[player],
            max_player,
            depth+1,
            move,
        ) 
        if min_or_max([score,best_score]) == score:
            best_score = score
            best_move = move
    return(best_move,best_score)


def play_game(board_,X_player,O_player):
    turns = 0
    print(board_.gameboard)
    while board_.is_end_state()[0] == False:
        board_.place_move('X',X_player.get_move())
        print(board_.gameboard)
        
        if board_.is_end_state()[0]==True:
            print(board_.is_end_state()[2])
            turns += 1
            break

        board_.place_move('O',O_player.get_move())
        print(board_.gameboard)

        if board_.is_end_state()[0]==True:
            print(board_.is_end_state()[2])
            turns += 1
            break

        turns += 1
    return(*board_.is_end_state()[1:],turns)