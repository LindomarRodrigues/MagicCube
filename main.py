from cube import Cube
from solvers.layer_by_layer import LayerByLayerSolver
from solvers.CFOP import CfopSolver
from solvers.optimizer import optimize_moves

cube = Cube()
cube.moves("B U' B2 L2 D2 R2 D' L2 U2 B2 U R' F' L R' D F2 U' R'")

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

