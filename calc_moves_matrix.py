import pickle
from copy import deepcopy

import numpy as np
from scipy.optimize import minimize
from tqdm import tqdm

from cube import Cube, CORNERS_CODES, EDGES_CODES


cubes_array = []
unormalized_cubes_array = []
normalized_cubes_array = []
after_moves_cubes_array = {
    move: [] for move in Cube.ALLOWED_MOVES
}
for _ in tqdm(range(10000)):
    cube = Cube()
    cube.moves()
    cube.normalize_rotations()
    cubes_array.append(cube.to_array_faces())


    for move in Cube.ALLOWED_MOVES:
        cube_ = deepcopy(cube)
        cube_.moves(move)

        cube_.normalize_rotations()
        after_moves_cubes_array[move].append(cube_.to_array_faces())
cubes_array = np.array(cubes_array)
moves_matrix = {}
# moves_matrix['normalize'] = np.ones(40) * np.inf
# moves_matrix['normalize'][len(CORNERS_CODES):2 * len(CORNERS_CODES)] = 3
# moves_matrix['normalize'][2 * len(CORNERS_CODES) + len(EDGES_CODES):] = 2
# # moves_matrix[]
#
# # for move in Cube.ALLOWED_MOVES:

for move in Cube.ALLOWED_MOVES:
    u_cubes_array = np.array(after_moves_cubes_array[move])
    moves_matrix[move] = np.linalg.lstsq(cubes_array, u_cubes_array,
                                         rcond=None
                                         )[0].round().astype(np.uint8)
    B_pred = cubes_array @ moves_matrix[move]
    mse = np.mean(np.abs(cubes_array - B_pred) ** 2)
    print(move)
    print(f"MSE: {mse}")
    print(f"MSE: {np.mean(np.abs(u_cubes_array - B_pred.round()) ** 2)}")
    # import ipdb; ipdb.set_trace()
pickle.dump(moves_matrix, open('moves_matrix.pkl', 'wb'))
