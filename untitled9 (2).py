import numpy as np
import pulp
import pycuber as pc

c = pc.Cube()
print(c)

moves_mapping = ["B'", "B",
                 "F", "F'",
                 "U'", "U",
                 "D", "D'",
                 "L'", "L",
                 "R", "R'"]
c = pc.Cube()
# random scramle
alg = ' '.join(np.random.choice(moves_mapping, 10, replace=True))
fc = c.copy()
fc(alg)
print(alg)
print(c(alg))
cubes_idxs = np.zeros(shape=(6, 3, 3), dtype=int)
counter = 1
for i in range(3):
    for j in range(3):
        cubes_idxs[0, i, j] = counter
        cubes_idxs[5, i, j] = counter + 45
        counter += 1
for j in range(3):
    for k in range(4):
        cubes_idxs[1 + k, 0, j] = 10 + j + k * 3
        cubes_idxs[1 + k, 1, j] = 10 + j + k * 3 + 12
        cubes_idxs[1 + k, 2, j] = 10 + j + k * 3 + 24
faces = []
for f in range(6):
    faces.append([])
    for i in range(3):
        for j in range(3):
            faces[f] += [cubes_idxs[f, i, j]]

faces_letters = 'U L F R B D'.split()
colors = ['red', 'yellow', 'green', 'white', 'orange', 'blue']
init_pattern = []
for face_idx, face in enumerate(faces_letters):
    a = c.get_face(face)
    for i in range(3):
        for j in range(3):
            init_pattern += [(cubes_idxs[face_idx, i, j], colors.index(a[i][j].colour) + 1)]
# import ipdb; ipdb.set_trace()
G = [
    (1, 1, 18), (1, 2, 30), (1, 3, 42), (1, 10, 3), (1, 22, 2),
    (1, 34, 1), (1, 18, 54), (1, 30, 53), (1, 42, 52), (1, 52, 10), (1, 53, 22),
    (1, 54, 34), (1, 19, 43), (1, 20, 31), (1, 21, 19), (1, 31, 44), (1, 33, 20),
    (1, 43, 45), (1, 44, 33), (1, 45, 21),

    # (3,4,17), (3,5,29), (3,6,41), (3,11,6), (3,23,5), (3,35,4), (3,17,51), (3,29,50), (3,41,49),
    # (3,49,11), (3,50,23), (3,51,35),

    (3, 7, 16), (3, 8, 28), (3, 9, 40),
    (3, 12, 9), (3, 24, 8), (3, 36, 7), (3, 16, 48), (3, 28, 47), (3, 40, 46),
    (3, 46, 12), (3, 47, 24), (3, 48, 36), (3, 13, 15), (3, 14, 27), (3, 15, 39),
    (3, 25, 14), (3, 27, 38), (3, 37, 13), (3, 38, 25), (3, 39, 37),

    (5, 10, 13),
    (5, 11, 14), (5, 12, 15), (5, 13, 16), (5, 14, 17), (5, 15, 18), (5, 16, 19),
    (5, 17, 20), (5, 18, 21), (5, 19, 10), (5, 20, 11), (5, 21, 12), (5, 3, 1),
    (5, 6, 2), (5, 9, 3), (5, 2, 4), (5, 8, 6), (5, 1, 7), (5, 4, 8), (5, 7, 9),

    # (9,22,25), (9,23,26), (9,24,27), (9,25,28), (9,26,29), (9,27,30),
    # (9,28,31), (9,29,32), (9,30,33), (9,31,22), (9,32,23), (9,33,24),

    (7, 34, 37), (7, 35, 38), (7, 36, 39), (7, 37, 40), (7, 38, 41),
    (7, 39, 42), (7, 40, 43), (7, 41, 44), (7, 42, 45), (7, 43, 34),
    (7, 44, 35), (7, 45, 36), (7, 46, 48), (7, 47, 51), (7, 48, 54),
    (7, 49, 47), (7, 51, 53), (7, 52, 46), (7, 53, 49), (7, 54, 52),

    (9, 1, 45), (9, 4, 33), (9, 7, 21), (9, 13, 1), (9, 25, 4), (9, 37, 7),
    (9, 21, 52), (9, 33, 49), (9, 45, 46), (9, 46, 13), (9, 49, 25),
    (9, 52, 37), (9, 10, 34), (9, 11, 22), (9, 12, 10), (9, 22, 35),
    (9, 24, 11), (9, 34, 36), (9, 35, 24), (9, 36, 12),

    # (15,2,44), (15,5,32),
    # (15,8,20), (15,14,2), (15,26,5), (15,38,8), (15,20,53), (15,32,50),
    # (15,44,47), (15,47,14), (15,50,26), (15,53,38),

    (11, 3, 43), (11, 6, 31),
    (11, 9, 19), (11, 15, 3), (11, 27, 6), (11, 39, 9), (11, 19, 54), (11, 31, 51),
    (11, 43, 48), (11, 48, 15), (11, 51, 27), (11, 54, 39), (11, 16, 18),
    (11, 17, 30), (11, 18, 42), (11, 28, 17), (11, 30, 41), (11, 40, 16),
    (11, 41, 28), (11, 42, 40)
]

max_moves = 3
max_moves += 1
# Create a new model
model = pulp.LpProblem("Minimize_Moves", pulp.LpMinimize)

# Define the variables
y = pulp.LpVariable.dicts('y', ((i, t) for i in range(12) for t in range(max_moves)), cat='Binary')
x = pulp.LpVariable.dicts('x', ((i, t) for i in range(54) for t in range(max_moves)), lowBound=1, upBound=6,
                          cat='Integer')
moves_used = pulp.LpVariable('moves_used', cat='Continuous', upBound=max_moves)

# Objective: Minimize the number of used moves
model += moves_used

# Constraints
big_M = 1000  # Big-M value

for t in range(max_moves):
    model += moves_used >= pulp.lpSum((t + 1) * y[i, t] for i in range(12))

for t in range(max_moves - 1):
    for k, i, j in G:
        model += x[i - 1, t] - x[j - 1, t + 1] <= big_M * (1 - y[k - 1, t])
        model += x[j - 1, t + 1] - x[i - 1, t] <= big_M * (1 - y[k - 1, t])

        model += x[j - 1, t] - x[i - 1, t + 1] <= big_M * (1 - y[k + 1 - 1, t])
        model += x[i - 1, t + 1] - x[j - 1, t] <= big_M * (1 - y[k + 1 - 1, t])

        model += x[i - 1, t] - 6 * (y[k - 1, t] + y[k + 1 - 1, t] + pulp.lpSum(
            y[l - 1, t] + y[l + 1 - 1, t] for l, m, n in G if m == i and k != l)) <= x[i - 1, t + 1]
        model += x[i - 1, t + 1] <= x[i - 1, t] + 6 * (y[k - 1, t] + y[k + 1 - 1, t] + pulp.lpSum(
            y[l - 1, t] + y[l + 1 - 1, t] for l, m, n in G if m == i and k != l))

# Final state conditions - all cubes in every face must have the same colors
for f in range(6):
    for i in faces[f]:
        for j in faces[f]:
            if i > j:
                model += x[i - 1, max_moves - 1] == x[j - 1, max_moves - 1]

# Set initial cube configuration
for cidx, color in init_pattern:
    model += x[cidx - 1, 0] == color

# One move at the time
for t in range(max_moves):
    model += pulp.lpSum(y[i, t] for i in range(12)) <= 1

# Redundant constraints
for t in range(max_moves - 1):
    for k in range(6):
        model += y[2 * k + 1, t] + y[2 * k, t + 1] <= 1
        model += y[2 * k, t] + y[2 * k + 1, t + 1] + y[2 * k + 1, t] <= 1

# Solve the problem
# model.solve(pulp.PULP_CBC_CMD(mip=True))
model.solve()

# Output the results
print("Status:", pulp.LpStatus[model.status])
print("Objective value:", pulp.value(model.objective))

solution = []
for t in range(max_moves):
    for i in range(12):
        if pulp.value(y[(i, t)]) > 0.5:
            solution += [moves_mapping[i]]
solution_alg = ' '.join(solution)
print(solution_alg)

c1 = c.copy()
c1(solution_alg)
