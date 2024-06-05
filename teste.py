import numpy as np

from cube import Cube, CORNERS_CODES, EDGES_CODES

cube = Cube()
import numpy as np

# Define the permutation arrays for a U move
# Assume CORNERS_CODES = ['URF', 'UFL', 'ULB', 'UBR', 'DFR', 'DLF', 'DBL', 'DRB']
# Assume EDGES_CODES = ['UR', 'UF', 'UL', 'UB', 'FR', 'FL', 'BL', 'BR', 'DF', 'DR', 'DB', 'DL']

# Define permutation arrays for corners and edges affected by U move
corner_permutation = [3, 0, 1, 2, 4, 5, 6, 7]  # New positions for corners
edge_permutation = [3, 0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11]  # New positions for edges

# Full permutation array combining corners and edges
full_permutation = corner_permutation + [i + 8 for i in corner_permutation] + edge_permutation + [i + 12 for i in edge_permutation]

# Convert the cube array to a numpy array
cube_array = np.array([
    *[cube.cube['corners'][corner_code] for corner_code in CORNERS_CODES],
    *[cube.cube['corners_rotations'][corner_code] for corner_code in CORNERS_CODES],
    *[cube.cube['edges'][edge_code] for edge_code in EDGES_CODES],
    *[cube.cube['edges_rotations'][edge_code] for edge_code in EDGES_CODES],
])

# Apply the permutation using numpy indexing
new_cube_array = cube_array[full_permutation]

# Convert the resulting array back to the cube dictionary format if needed
new_cube = {
    'corners': {corner_code: new_cube_array[i] for i, corner_code in enumerate(CORNERS_CODES)},
    'corners_rotations': {corner_code: new_cube_array[8 + i] for i, corner_code in enumerate(CORNERS_CODES)},
    'edges': {edge_code: new_cube_array[16 + i] for i, edge_code in enumerate(EDGES_CODES)},
    'edges_rotations': {edge_code: new_cube_array[28 + i] for i, edge_code in enumerate(EDGES_CODES)},
}


import ipdb; ipdb.set_trace()