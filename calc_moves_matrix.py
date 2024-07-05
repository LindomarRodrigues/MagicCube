import pickle
from copy import deepcopy

import numpy as np
from tqdm import tqdm

from cube import Cube

cubes_array = []
unormalized_cubes_array = []
normalized_cubes_array = []
after_moves_cubes_array = {
    move: [] for move in Cube.ALLOWED_MOVES
}
for _ in tqdm(range(1000)):
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
perm_matrix = {}


# moves_matrix['normalize'] = np.ones(40) * np.inf
# moves_matrix['normalize'][len(CORNERS_CODES):2 * len(CORNERS_CODES)] = 3
# moves_matrix['normalize'][2 * len(CORNERS_CODES) + len(EDGES_CODES):] = 2
# # moves_matrix[]
#
# # for move in Cube.ALLOWED_MOVES:
def find_global_permutation_index(A, B):
    A = np.array(A)
    B = np.array(B)

    permutation_indices = [[] for _ in range(A.shape[1])]


    for i in range(A.shape[1]):
        for k in range(A.shape[0]):
            a = A[k]
            b = B[k]
            indices = list(np.where(b == a[i])[0])
            if k == 0:
                permutation_indices[i] = indices

            for indice in permutation_indices[i]:
                if indice not in indices:
                    permutation_indices[i].remove(indice)
            if len(permutation_indices[i]) == 0:
                import ipdb; ipdb.set_trace()
    return [indices[0] for indices in permutation_indices]

for move in tqdm(Cube.ALLOWED_MOVES):
    u_cubes_array = np.array(after_moves_cubes_array[move])
    global_permutation_index = find_global_permutation_index(cubes_array, u_cubes_array)
    # import ipdb; ipdb.set_trace()
    perm_matrix[move] = global_permutation_index

    moves_matrix[move] = np.linalg.lstsq(cubes_array, u_cubes_array,
                                         rcond=1e-10
                                         )[0].round().astype(int)
    B_pred = cubes_array @ moves_matrix[move]
    mse = np.mean(np.abs(cubes_array - B_pred) ** 2)
    print(move)
    print(f"MSE: {mse}")
    print(f"MSE: {np.mean(np.abs(u_cubes_array - B_pred.round()) ** 2)}")
    # import ipdb; ipdb.set_trace()
pickle.dump(moves_matrix, open('moves_matrix.pkl', 'wb'))
pickle.dump(perm_matrix, open('perm_matrix.pkl', 'wb'))
