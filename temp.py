import random
import time
from collections import deque
from heapq import heappush, heappop

def apply_permutation_in_place(array, permutation):
    temp_array = array[:]
    for i, perm_index in enumerate(permutation):
        array[i] = temp_array[perm_index]

def heuristic(array, target):
    # Manhattan distance heuristic
    return sum(abs(a - b) for a, b in zip(array, target))

def find_permutation_sequence(A, B, P):
    if A == B:
        return []

    # Priority queues for A* search
    open_start = [(heuristic(A, B), A[:], [])]  # (heuristic value, current array, sequence)
    open_end = [(heuristic(B, A), B[:], [])]
    visited_start = {tuple(A): []}
    visited_end = {tuple(B): []}

    while open_start and open_end:
        if len(open_start) <= len(open_end):
            _, current_array, sequence = heappop(open_start)
            for perm in P:
                new_array = current_array[:]
                apply_permutation_in_place(new_array, perm)
                new_tuple = tuple(new_array)

                if new_tuple in visited_end:
                    return sequence + [perm] + visited_end[new_tuple][::-1]

                if new_tuple not in visited_start:
                    new_sequence = sequence + [perm]
                    visited_start[new_tuple] = new_sequence
                    heappush(open_start, (heuristic(new_array, B), new_array, new_sequence))
        else:
            _, current_array, sequence = heappop(open_end)
            for perm in P:
                new_array = current_array[:]
                apply_permutation_in_place(new_array, perm)
                new_tuple = tuple(new_array)

                if new_tuple in visited_start:
                    return visited_start[new_tuple] + [perm] + sequence[::-1]

                if new_tuple not in visited_end:
                    new_sequence = sequence + [perm]
                    visited_end[new_tuple] = new_sequence
                    heappush(open_end, (heuristic(new_array, A), new_array, new_sequence))

    return None  # If no sequence found

# Example usage
# A = [random.randint(0, 1000) for _ in range(10)]
# B = random.sample(A, len(A))
# P = [random.sample(range(len(A)), len(A)) for _ in range(10)]
# start_time = time.time()
# sequence = find_permutation_sequence(A, B, P)
# print(len(sequence) if sequence else "No sequence found", time.time() - start_time)

import numpy as np


def find_global_permutation_index(A, B):
    # Convert lists of arrays into matrices
    A_matrix = np.array(A)
    B_matrix = np.array(B)

    # Flatten the matrices to treat the problem as finding permutation for 1D arrays
    A_flat = A_matrix.flatten()
    B_flat = B_matrix.flatten()

    # Initialize an empty list to store the permutation indices
    perm_index = np.zeros(len(A_flat), dtype=int)

    # Track the used indices in B
    used_indices = set()

    # Find the permutation index
    for i, elem in enumerate(A_flat):
        # Find the index of the first occurrence of elem in B_flat that has not been used
        for j in range(len(B_flat)):
            if B_flat[j] == elem and j not in used_indices:
                perm_index[i] = j
                used_indices.add(j)
                break

    # Reshape the permutation index to the original shape of A_matrix
    perm_index = perm_index.reshape(A_matrix.shape[0], A_matrix.shape[1])

    return perm_index[0]  # Return the permutation for the first array which should be applicable to all


# Example usage:
A = [np.array([0, 1, 0, 1]), np.array([1, 0, 1, 0])]
B = [np.array([1, 0, 1, 0]), np.array([0, 1, 0, 1])]

global_permutation_index = find_global_permutation_index(A, B)
print("Global permutation index:", global_permutation_index)

# Applying the same permutation index to all arrays in A to align them with B
A_permuted = [a[global_permutation_index] for a in A]

print("Permuted A arrays:")
for a_permuted in A_permuted:
    print(a_permuted)