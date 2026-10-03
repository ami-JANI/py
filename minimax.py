# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 21:59:13 2026

@author: janir
"""

import math
import copy

def player(state):
    x_count = 0
    o_count = 0
    for row in state:
        for cell in row:
            if cell == 'X':
                x_count += 1
            elif cell == 'O':
                o_count += 1
    if x_count == o_count:
        return 'X'
    else:
        return 'O'

def display(state):
    for row in state:
        print(" | ".join(row))
    print("-" * 9)

def actions(state):
    moves = []
    for i in range(3):
        for j in range(3):
            if state[i][j] == ' ':
                moves.append((i, j))
    return moves

def result(state, action):
    i, j = action
    new_state = copy.deepcopy(state)
    new_state[i][j] = player(state)
    return new_state


def terminal(state):
    lines = []
    for row in state:
        lines.append(row)
    for j in range(3):
        column = []
        for i in range(3):
            column.append(state[i][j])
        lines.append(column)
    lines.append([state[0][0], state[1][1], state[2][2]])
    lines.append([state[0][2], state[1][1], state[2][0]])
    
    for line in lines:
        if line == ['X', 'X', 'X'] or line == ['O', 'O', 'O']:
            return True

    for row in state:
        for cell in row:
            if cell == ' ':
                return False

    return True


def utility(state):
    lines = []
    for row in state:
        lines.append(row)
    for j in range(3):
        column = []
        for i in range(3):
            column.append(state[i][j])
        lines.append(column)
    lines.append([state[0][0], state[1][1], state[2][2]])
    lines.append([state[0][2], state[1][1], state[2][0]])

    for line in lines:
        if line == ['X', 'X', 'X']:
            return 1
        if line == ['O', 'O', 'O']:
            return -1
    return 0


def max_value(state):
    if terminal(state):
        return utility(state)

    value = -math.inf

    for action in actions(state):
        new_state = result(state, action)
        eval_value = min_value(new_state)

        if eval_value > value:
            value = eval_value

    return value


def min_value(state):
    if terminal(state):
        return utility(state)

    value = math.inf

    for action in actions(state):
        new_state = result(state, action)
        eval_value = max_value(new_state)

        if eval_value < value:
            value = eval_value

    return value


def minimax(state):
    best_action = None

    if player(state) == 'X':
        best_value = -math.inf

        for action in actions(state):
            new_state = result(state, action)
            value = min_value(new_state)

            if value > best_value:
                best_value = value
                best_action = action

    else:
        best_value = math.inf

        for action in actions(state):
            new_state = result(state, action)
            value = max_value(new_state)

            if value < best_value:
                best_value = value
                best_action = action

    return best_action


def play():
    state = [
        [' ', ' ', ' '],
        [' ', ' ', ' '],
        [' ', ' ', ' ']
    ]

    print("Welcome to Tic-Tac-Toe! You are O, AI is X.")
    display(state)

    while not terminal(state):
        if player(state) == 'O':
            position = input("Enter row and col: ").split()
            row = int(position[0])
            col = int(position[1])
            action = (row, col)
            if action not in actions(state):
                print("Invalid move! Try again.")
                continue
            # action = minimax(state)
            state = result(state, action)
        else:
            action = minimax(state)
            print(f"AI plays: {action}")
            state = result(state, action)

        display(state)

    score = utility(state)

    if score == 1:
        print("X wins!")
    elif score == -1:
        print("O wins!")
    else:
        print("It's a draw!")

play()