import pickle
import pulp
from cube import Cube

# Initialize the cube and get the initial and solved states
cube = Cube()
solved_cube = cube.to_array_faces()
moves = cube.moves(k=5)
cube.normalize_rotations()
init_pattern = cube.to_array_faces()

# Load the permutation matrix
perm_matrix = pickle.load(open('perm_matrix.pkl', 'rb'))
G = [perm_matrix[move] for move in Cube.ALLOWED_MOVES]

# Define the maximum number of moves
max_moves = 6

# Create the optimization model
model = pulp.LpProblem("Minimize_Moves", pulp.LpMinimize)

# Define the variables
y = pulp.LpVariable.dicts('y', ((i, t) for i in range(len(Cube.ALLOWED_MOVES)) for t in range(max_moves)), cat='Binary')
x = pulp.LpVariable.dicts('x', ((i, t) for i in range(len(init_pattern)) for t in range(max_moves)), lowBound=0, upBound=5, cat='Integer')
moves_used = pulp.LpVariable('moves_used', cat='Integer', lowBound=0, upBound=max_moves)

# Objective: Minimize the number of used moves
model += moves_used

# Constraints
big_M = 10000

# Constraint to track the number of moves used
for t in range(max_moves):
    model += moves_used >= t + 1 - (max_moves - 1) * (1 - pulp.lpSum(y[i, t] for i in range(len(Cube.ALLOWED_MOVES))))

# Transition constraints between consecutive states
for t in range(max_moves - 1):
    for k, move in enumerate(G):
        for i in range(len(move)):
            model += x[i, t] - x[move[i], t + 1] <= big_M * (1 - y[k, t])
            model += x[move[i], t + 1] - x[i, t] <= big_M * (1 - y[k, t])
            model += x[i, t] - 5 * (1 - y[k, t]) <= x[i, t + 1]
            model += x[i, t + 1] <= x[i, t] + 5 * (1 - y[k, t])

# Final state conditions
for i in range(0, len(init_pattern), 8):
    model += pulp.lpSum(x[i, max_moves - 1] == x[i_ , max_moves - 1] for i_ in range(i + 1, i + 8)) == 8

for i in range(len(init_pattern)):
    model += x[i, 0] == init_pattern[i]

# Ensure only one move per time step
for t in range(max_moves):
    model += pulp.lpSum(y[i, t] for i in range(len(Cube.ALLOWED_MOVES))) <= 1

# Redundant constraints to avoid conflicting moves
for t in range(max_moves - 1):
    for k in range(0, len(Cube.ALLOWED_MOVES), 3):
        model += y[k, t] + y[k + 1, t + 1] <= 1
        model += y[k + 1, t] + y[k, t + 1] <= 1
        model += y[k, t] + y[k + 2, t + 1] <= 1
        model += y[k + 2, t] + y[k, t + 1] <= 1
        model += y[k + 1, t] + y[k + 2, t + 1] <= 1
        model += y[k + 2, t] + y[k + 1, t + 1] <= 1

# Solve the problem
model.solve(pulp.PULP_CBC_CMD(mip=True))

# Output the results
print("Status:", pulp.LpStatus[model.status])
print("Objective value:", pulp.value(model.objective))

solution = []
for t in range(max_moves):
    for i in range(len(Cube.ALLOWED_MOVES)):
        if pulp.value(y[(i, t)]) > 0.5:
            solution.append(Cube.ALLOWED_MOVES[i])

solution_alg = ' '.join(solution)
print(solution_alg, moves)
final_state = [x[i, max_moves - 1].value() for i in range(len(init_pattern))]
print("Final State:", final_state)
