import numpy as np
import time
from gui import root, create_board, button

nums = np.arange(1, 9)
blank_tile = 0      # placeholder
nums = np.append(nums, blank_tile) 
goal = np.arange(1, 9)
goal = np.append(goal, blank_tile)
steps = []          # for GUI

def is_solvable(arr):
    inv_count = 0
    for i in range(9):
        for j in range(i + 1, 9):
            if arr[j] != blank_tile and arr[i] != blank_tile and arr[i] > arr[j]:       # ignoring empty tile (None)
                inv_count += 1

    return inv_count % 2 == 0       # condition to be solvable: even number of inversions (inversion = values in reverse order)

def shape_board(board):
    return board.reshape((3, 3))

def generate_start():
    while True:
        np.random.shuffle(nums)
        if is_solvable(nums):
            return nums

def left(board):
    new_state = np.copy(board)
    index = np.argwhere(board == blank_tile)[0]
    if  index not in [2, 5, 8]:     # otherwise already rightmost
        temp = new_state[index + 1]
        new_state[index + 1] = new_state[index]
        new_state[index] = temp
        return new_state
    else:
        return None                 # can't move

def right(board):
    new_state = np.copy(board)
    index = np.argwhere(board == blank_tile)[0]
    if  index not in [0, 3, 6]:     # otherwise already leftmost
        temp = new_state[index - 1]
        new_state[index - 1] = new_state[index]
        new_state[index] = temp
        return new_state
    else:
        return None                 # can't move

def up(board):
    new_state = np.copy(board)
    index = np.argwhere(board == blank_tile)[0]
    if  index not in [6, 7, 8]:     # otherwise already lowermost
        temp = new_state[index + 3]
        new_state[index + 3] = new_state[index]
        new_state[index] = temp
        return new_state
    else:
        return None                 # can't move 

def down(board):
    new_state = np.copy(board)
    index = np.argwhere(board == blank_tile)[0]
    if  index not in [0, 1, 2]:     # otherwise already uppermost
        temp = new_state[index - 3]
        new_state[index - 3] = new_state[index]
        new_state[index] = temp
        return new_state
    else:
        return None                 # can't move

def dist(b1, b2):
    d = 0
    b1, b2 = shape_board(b1), shape_board(b2)
    for i in range (9):
        [r1, c1] = np.argwhere(b1 == i)[0]
        [r2, c2] = np.argwhere(b2 == i)[0]
        d += abs(r1 - r2) + abs(c1 - c2)
    return d

class Node:
    def __init__(self, board, direction, parent) -> None:
        self.board = board
        self.direction = direction
        self.parent = parent
        self.h = None   # basis for greedy's decision, Manhattan distance as heuristic

def greedy(board):
    parent = Node(board=board, direction=None, parent=None)
    visited = []
    fringe = []
    moves = []
    current_node = parent
    visited.append(current_node)

    while not np.array_equal(current_node.board, goal):
        directions = [
            Node(board=up(current_node.board), direction="up", parent=current_node),
            Node(board=left(current_node.board), direction="left", parent=current_node),
            Node(board=right(current_node.board), direction="right", parent=current_node),
            Node(board=down(current_node.board), direction="down", parent=current_node)
        ]
        for node in directions:
            if node.board is not None and not any(np.array_equal(node.board, board) for board in visited):  # only add new possible moves
                fringe.append(node)
                visited.append(node.board)

        for node in fringe:     
            node.h = dist(node.board, goal)     # heuristic for each board to goal state

        # use lambda function instead of separate func declaration
        fringe.sort(key=lambda x: x.h)      # property of fringe: ordered queue
        if len(fringe) > 0: 
            current_node = fringe.pop(0)        # default = -1, pop first

    result = current_node.board

    while current_node.parent is not None:
        moves.insert(0, current_node.direction)
        steps.insert(0, shape_board(current_node.board))
        current_node = current_node.parent

    return moves, result

if __name__ == "__main__":
    b = generate_start() 
    start = time.time()   
    moves, board = greedy(b)
    end = time.time()
    print("Start:")
    print(shape_board(b))
    print()
    print("Moves:")
    print(moves)
    print()
    print("Result:")
    print(shape_board(board))
    print()
    print(f"Number of moves: {len(moves)}, processing time: {end - start}")

    # call GUI
    create_board(shape_board(b))
    button(steps)       # shows solution on button click
    root.mainloop()

