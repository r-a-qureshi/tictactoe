import numpy as np
import random
from copy import deepcopy
import pandas as pd

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
        self.is_end_state()
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

class Player():
    def __init__(self,mark,ttt_board):
        self.mark=mark
        self.ttt_board = ttt_board

class RandomPlayer(Player):
    def get_move(self):
        print('Random Player Turn')
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

    
def scoring(board_,depth,player):
    result = board_.is_end_state()
    depth = 0
    if result[1] == player:
        score = 10 - depth
    elif result[1] != 'Draw!':
        score = -10 + depth
    else:
        score = 0
    return(score,player)

def minimax(board_,depth,player,max_player):
    board_ = deepcopy(board_)
    reverse_player = {'X':'O','O':'X'}
    if board_.is_end_state()[0]:
        score,_ = scoring(board_,depth,max_player)
        return(score,None)
    move_list = board_.remaining_moves()
    scores = []
    best_move = (-1,-1)
    if player == max_player:
        best_value = -1000
        for move in move_list:
            board_.place_move(player,move)
            value,_ = minimax(board_,depth+1,reverse_player[player],max_player)
            scores.append(value)
            # if value > best_value:
            best_value = max(scores)
            best_move = move_list[np.argmax(scores)]
        if depth == 0:
            print(list(zip(move_list,scores))) 
        return(best_value,best_move)
    else:
        best_value = 1000
        for move in move_list:
            board_.place_move(player,move)
            value,_ = minimax(board_,depth+1,reverse_player[player],max_player)
            scores.append(value)
            # if value < best_value:
            #     best_value = value
            #     best_move = move
            best_value = min(scores)
            best_move = move_list[np.argmin(scores)]
        if depth == 0:
            print(list(zip(move_list,scores))) 
        return(best_value,best_move)

class MiniMaxPlayer(Player):
    def get_move(self):
        if self.mark == 'X':
            player_dict = {'X':True,'O':False}
        else:
            player_dict = {'O':True,'X':False}
        return(minimax(self.ttt_board,0,self.mark,self.mark)[1])

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

if __name__ == '__main__':
    ttt = Board()
    # score, move = minimax(ttt,0,'X')
    # print(score,move)
    X_player = MiniMaxPlayer('X',ttt)
    O_player = MiniMaxPlayer('O',ttt)
    # ttt.place_move('O',(0,2))
    # ttt.place_move('O',(2,0))
    # ttt.place_move('X',(0,0))
    # minimax(ttt,0,'X')
    play_game(ttt,X_player,O_player)