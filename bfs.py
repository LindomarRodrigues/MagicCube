import itertools
import pickle
from collections import deque

import numpy as np

from cube import Cube

moves_matrix = pickle.load(open('moves_matrix.pkl', 'rb'))

cube = Cube()

original_cube = cube.to_array_faces()

cube.moves()
cube.normalize_rotations()

scrumbled_cube = cube.to_array_faces()

from numpy.linalg import norm


def find_closest_move(solution_matrix, moves_combinations, moves_matrix, combined_matrix):
    closest_moves = None
    min_distance = float('inf')

    for moves in moves_combinations:
        for move in moves:
            combined_matrix = combined_matrix @ moves_matrix[move]
        distance = norm(solution_matrix - combined_matrix)
        if distance < min_distance:
            print(distance)
            min_distance = distance
            closest_moves = moves

    return closest_moves


def apply_moves(cube, original_cube, moves_matrix, num_moves_per_iteration):
    solution_moves = []
    moves_combinations = list(itertools.product(moves_matrix.keys(), repeat=num_moves_per_iteration))
    combined_matrix = np.eye(moves_matrix['U'].shape[1])

    while True:
        solution_matrix = np.linalg.lstsq([cube], [original_cube], rcond=None)[0]

        moves = find_closest_move(solution_matrix, moves_combinations, moves_matrix, combined_matrix)
        for move in moves:
            cube = (cube @ moves_matrix[move]).round()
            combined_matrix = combined_matrix @ moves_matrix[move]
        solution_moves.append(moves)

        # import ipdb;
        # ipdb.set_trace()

    return solution_moves


# Assuming cube, original_cube, and moves_matrix are defined as in your code
# num_moves_per_iteration = 5  # Set the number of moves per iteration
# solution_moves = apply_moves(scrumbled_cube, original_cube, moves_matrix, num_moves_per_iteration)
# print("Solution moves:", solution_moves)
# import ipdb;
#
# ipdb.set_trace()
visited = []
moves = []
queue = deque([scrumbled_cube])

while queue:
    state = queue.popleft()
    # visited.add(tuple(state))
    if len(visited) % 1000 == 0:
        print(len(visited))
    # if tuple(state) in visited:
    #     continue
    for move in moves_matrix:
        move_matrix = moves_matrix[move]
        new_cube = (state @ move_matrix).round()

        if tuple(new_cube) not in visited:
            queue.append(new_cube)
            visited.append(tuple(new_cube))
            moves.append(move)

            if np.all(new_cube == original_cube):
                print('Found')
                # visited.index(tuple(new_cube))
                import ipdb;

                ipdb.set_trace()

# for move in moves_matrix:
#     move_matrix = moves_matrix[move]
#     new_cube = (scrumbled_cube @ move_matrix).round()
#
#
#     import ipdb; ipdb.set_trace()
