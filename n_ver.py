import pickle

import pulp

from cube import Cube

cube = Cube()
solved_cube = cube.to_array_faces()

moves = cube.moves(k=4)

cube.normalize_rotations()

init_pattern = cube.to_array_faces()
print(solved_cube)
print(init_pattern)

cube.plot()

# moves_matrix = pickle.load(open('moves_matrix.pkl', 'rb'))
# index_cube = [i for i in range(len(init_pattern))]
# G = [index_cube @ moves_matrix[move] for move in Cube.ALLOWED_MOVES]
perm_matrix = pickle.load(open('perm_matrix.pkl', 'rb'))
G = [perm_matrix[move] for move in Cube.ALLOWED_MOVES]
import ipdb;

ipdb.set_trace()
max_moves = 4
max_moves += 1
model = pulp.LpProblem("Minimize_Moves", pulp.LpMinimize)

y = pulp.LpVariable.dicts('y', ((i, t) for i in range(len(Cube.ALLOWED_MOVES)) for t in range(max_moves)),
                          cat='Binary')
x = pulp.LpVariable.dicts('x', ((i, t) for i in range(len(init_pattern)) for t in range(max_moves)),
                          lowBound=0,
                          upBound=5,
                          cat='Integer')
moves_used = pulp.LpVariable('moves_used', cat='Continuous', upBound=max_moves)
import ipdb;

ipdb.set_trace()

model += moves_used

big_M = 10000  # Big-M value

for t in range(max_moves):
    model += moves_used >= pulp.lpSum((t + 1) * y[i, t] for i in range(len(Cube.ALLOWED_MOVES)))

for t in range(max_moves - 1):
    for k, move in enumerate(G):
        for i in range(len(move)):
            model += x[i, t] - x[move[i], t + 1] <= big_M * (1 - y[k, t])
            model += x[move[i], t + 1] - x[i, t] <= big_M * (1 - y[k, t])
            model += x[i, t] - 5 * (y[k, t] + pulp.lpSum(y[l, t] for l in range(len(Cube.ALLOWED_MOVES)) if l != k)) <= \
                     x[i, t + 1]
            model += x[i, t + 1] <= x[i, t] + 5 * (
                        y[k, t] + pulp.lpSum(y[l, t] for l in range(len(Cube.ALLOWED_MOVES)) if l != k))

for i in range(0, len(init_pattern), 8):
    for i_ in range(i + 1, i + 8):
        model += x[i, max_moves - 1] == x[i_, max_moves - 1]

for i in range(len(init_pattern)):
    model += x[i, 0] == init_pattern[i]

for t in range(max_moves):
    model += pulp.lpSum(y[i, t] for i in range(len(cube.ALLOWED_MOVES))) <= 1

for t in range(max_moves - 1):
    for k in range(0, len(Cube.ALLOWED_MOVES), 3):
        model += y[k, t] + y[k + 1, t + 1] <= 1
        model += y[k + 1, t] + y[k, t + 1] + y[k, t] <= 1

        model += y[k, t] + y[k + 2, t + 1] <= 1
        model += y[k + 2, t] + y[k, t + 1] + y[k, t] <= 1

        model += y[k + 1, t] + y[k + 2, t + 1] <= 1
        model += y[k + 2, t] + y[k + 1, t + 1] + y[k + 1, t] <= 1

model.solve(pulp.PULP_CBC_CMD(mip=True))

print("Status:", pulp.LpStatus[model.status])
print("Objective value:", pulp.value(model.objective))

solution = []
for t in range(max_moves):
    for i in range(len(Cube.ALLOWED_MOVES)):
        if pulp.value(y[(i, t)]) > 0.5:
            solution += [Cube.ALLOWED_MOVES[i]]
solution_alg = ' '.join(solution)
print(solution_alg, moves)
[x[i, max_moves - 1].value() for i in range(len(init_pattern))]
import ipdb;

ipdb.set_trace()
#
# c1 = c.copy()
# c1(solution_alg)
