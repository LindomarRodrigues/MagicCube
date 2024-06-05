from copy import deepcopy

import numpy as np
from tqdm import tqdm

from cube import Cube, CORNERS_CODES, EDGES_CODES
from solvers.CFOP.cfop import CfopSolver
from solvers.layer_by_layer import LayerByLayerSolver
from solvers.optimizer import optimize_moves

cube = Cube()
cube.normalize_rotations()

orig_cube_array = np.array([
    *[cube.cube['corners'][corner_code] for corner_code in CORNERS_CODES],
    *[cube.cube['corners_rotations'][corner_code] for corner_code in CORNERS_CODES],
    *[cube.cube['edges'][edge_code] for edge_code in EDGES_CODES],
    *[cube.cube['edges_rotations'][edge_code] for edge_code in EDGES_CODES],
])
cubes_array = []
u_cubes_array = []
after_moves_cubes_array = {
    move: [] for move in Cube.ALLOWED_MOVES
}
for _ in tqdm(range(1000)):
    cube = Cube()
    cube.moves()
    cube.normalize_rotations()

    cube_array = [
        *[cube.cube['corners'][corner_code] for corner_code in CORNERS_CODES],
        *[cube.cube['corners_rotations'][corner_code] for corner_code in CORNERS_CODES],
        *[cube.cube['edges'][edge_code] for edge_code in EDGES_CODES],
        *[cube.cube['edges_rotations'][edge_code] for edge_code in EDGES_CODES],
    ]
    cubes_array.append(cube_array)

    for move in Cube.ALLOWED_MOVES:
        cube_ = deepcopy(cube)
        cube_.moves(move)
        # cube_.normalize_rotations()
        after_moves_cubes_array[move].append([
            *[cube_.cube['corners'][corner_code] for corner_code in CORNERS_CODES],
            *[cube_.cube['corners_rotations'][corner_code] for corner_code in CORNERS_CODES],
            *[cube_.cube['edges'][edge_code] for edge_code in EDGES_CODES],
            *[cube_.cube['edges_rotations'][edge_code] for edge_code in EDGES_CODES],
        ])

cubes_array = np.array(cubes_array)
moves_matrix = {}
for move in Cube.ALLOWED_MOVES:
    u_cubes_array = after_moves_cubes_array[move]
    moves_matrix[move] = np.linalg.lstsq(cubes_array, u_cubes_array, rcond=None)[0]

    B_pred = (cubes_array @ moves_matrix[move])

    # Calculate the Mean Squared Error (MSE)
    mse = np.mean(np.abs(u_cubes_array - B_pred) ** 2)
    print(move)
    print(f"MSE: {mse}")
import ipdb; ipdb.set_trace()

u_cubes_array = np.array(u_cubes_array)

# x is the matrix that multiplied by the original cube array gives the cube array after the U move
x, residuals, rank, ss = np.linalg.lstsq(cubes_array, u_cubes_array, rcond=None)

# Predict b values using the found x
B_pred = (cubes_array @ x.round(0))

# Calculate the Mean Squared Error (MSE)
mse = np.mean(np.abs(u_cubes_array - B_pred) ** 2)
print(f"MSE: {mse}")
import ipdb;

ipdb.set_trace()
solver = LayerByLayerSolver(cube)
solver.solve()

moves = optimize_moves(solver.moves)

print("Layer by layer:")
print(f"Quantity of moves: {len(solver.moves)}")
print(f"Quantity of optimized moves: {len(moves)}")

print(f"Movements: {' '.join(moves)}")

cube = Cube()
cube.moves("B U' B2 L2 D2 R2 D' L2 U2 B2 U R' F' L R' D F2 U' R'")

solver = CfopSolver(cube)
solver.solve()

moves = optimize_moves(solver.moves)

print("\nCFOP: ")
print(f"Quantity of moves: {len(solver.moves)}")
print(f"Quantity of optimized moves: {len(moves)}")

print(f"Movements: {' '.join(moves)}")
