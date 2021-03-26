"""
File: game.py
Project: 2048
Created Date: Thursday, 25th March 2021 10:56:26 am
-----
Author(s): Michael O'Connell
-----
Last Modified By: Michael O'Connell
Date Modified: Thursday, 25th March 2021 10:56 am
"""

from random import randrange, choice
from pprint import pprint
import numpy as np
import sys

register(
    id='Copy-v0',
    entry_point='gym.envs.algorithmic:CopyEnv',
    max_episode_steps=200,
    reward_threshold=25.0,
)

score = 0
board_size = 4

class 
def game(board):
    global score
    print(np.array(board))
    input_char = input("Move: ")

    while possible_move(input_char, board) == False:
        input_char = input("Move: ")
    board = move(input_char, board)
    print("Score: ", score)
    return board


def setup():
    board = np.zeros(
        (board_size, board_size), dtype="int"
    )  # np.random.randint(15, size=(board_size, board_size))
    random_add(board)
    np.set_printoptions(formatter={"int": lambda x: "{:6d} ".format(x)})
    while is_gameover(board) == False:
        board = game(board)
        board = random_add(board)


def is_gameover(board):
    return not any(possible_move(move, board) for move in ["w", "a", "s", "d"])


def random_add(board):
    if np.any(board == 0):
        zeroElements = np.argwhere(board == 0)
        pos = zeroElements[np.random.choice(zeroElements.shape[0], 1, replace=False), :]
        board[pos[0][0]][pos[0][1]] = 2
    return np.array(board)


def move(direction, b):
    def move_row_left(row):
        global score

        def gravity_left(row):
            new_row = [i for i in row if i != 0]
            new_row += [0 for i in range(board_size - len(new_row))]
            return new_row

        def merge(row):
            global score
            for i in range(board_size - 2):
                if row[i] == row[i + 1]:
                    row[i] *= 2
                    row[i + 1] = 0
                    score += row[i]
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
        "w": up,
        "W": up,
        "a": left,
        "A": left,
        "s": down,
        "S": down,
        "d": right,
        "D": right,
    }

    if direction in moves:

        return np.array(moves[direction](b))
    else:
        return b


def possible_move(direction, b):
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
        "w": up,
        "W": up,
        "a": left,
        "A": left,
        "s": down,
        "S": down,
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


setup()
