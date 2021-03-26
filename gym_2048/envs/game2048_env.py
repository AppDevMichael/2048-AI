"""
File: 2048_env.py
Project: envs
Created Date: Thursday, 25th March 2021 6:25:48 pm
-----
Author(s): Michael O'Connell
-----
Last Modified By: Michael O'Connell
Date Modified: Thursday, 25th March 2021 6:30 pm
"""
from random import randrange, choice
from pprint import pprint
import numpy as np
import gym


class Game2048Env(gym.Env):
    metadata = {"render.modes": ["human"]}

    
    board_size = 4
    def __init__(self):
        self.board = np.zeros((self.board_size, self.board_size), dtype="int")
        # np.random.randint(15, size=(board_size, board_size))
        self.score = 0
        self.random_add(self.board)
        np.set_printoptions(formatter={"int": lambda x: "{:6d} ".format(x)})

    def step(self, action):
        if self.is_gameover(self.board) == False:
            self.board = self.game(self.board, action)
            self.board = self.random_add(self.board)

    def reset(self):
        self.board = np.zeros((self.board_size, self.board_size), dtype="int")
        # np.random.randint(15, size=(board_size, board_size))
        self.random_add(self.board)

    def render(self, mode="human"):
        print(np.array(self.board))
        print("Score: ", self.score)
        ...

    def close(self):
        ...


    def game(self, board, input):
        input_char = input

        if self.possible_move(input_char, board) == False:
            return board #input_char = input("Move: ")
        board = self.move(input_char, board)
        return board

    def is_gameover(self, board):
        return not any(self.possible_move(move, board) for move in [0, 1, 2, 3])

    def random_add(self, board):
        if np.any(board == 0):
            zeroElements = np.argwhere(board == 0)
            pos = zeroElements[np.random.choice(zeroElements.shape[0], 1, replace=False), :]
            board[pos[0][0]][pos[0][1]] = 2
        return np.array(board)

    def move(self, direction, b):
        def move_row_left(row):

            def gravity_left(row):
                new_row = [i for i in row if i != 0]
                new_row += [0 for i in range(self.board_size - len(new_row))]
                return new_row

            def merge(row):
                for i in range(self.board_size - 2):
                    if row[i] == row[i + 1]:
                        row[i] *= 2
                        row[i + 1] = 0
                        self.score += row[i]
                return row

            out = gravity_left(merge(gravity_left(row))) if np.any(row) else row
            return out

        def up(b):
            return transpose(left(transpose(b)))

        def down(b):
            return transpose(right(transpose(b)))

        def left(b):
            return [move_row_left(row) for row in b]

        def right(b):
            return invert(left(invert(b)))

        moves = {
            0: up,
            "w": up,
            "W": up,
            1: left,
            "a": left,
            "A": left,
            2: down,
            "s": down,
            "S": down,
            3: right,
            "d": right,
            "D": right,
        }

        if direction in moves:

            return np.array(moves[direction](b))
        else:
            return b

    def possible_move(self, direction, b):
        def row_is_left_movable(row):
            def change(i):
                if row[i] == 0 and row[i + 1] != 0:  # Move
                    return True
                if row[i] != 0 and row[i + 1] == row[i]:  # Merge
                    return True
                return False

            return any(change(i) for i in range(len(row) - 1))

        def left(grid):
            return any(row_is_left_movable(row) for row in grid)

        def right(grid):
            return left(invert(grid))

        def up(grid):
            return left(transpose(grid))

        def down(grid):
            return right(transpose(grid))

        moves = {
            0: up,
            "w": up,
            "W": up,
            1: left,
            "a": left,
            "A": left,
            2: down,
            "s": down,
            "S": down,
            3: right,
            "d": right,
            "D": right,
        }

        if direction in moves:
            return moves[direction](b)
        else:
            return False

def transpose(field):
    return [list(row) for row in zip(*field)]

def invert(field):
    return [row[::-1] for row in field]
