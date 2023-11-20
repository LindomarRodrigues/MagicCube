# MagicCube

Python 3 implementation of a (3x3x3) Rubik's Cube utility.

![3x3x3 Rubik's Cube](cube.png)

## TODO (Open to contributions)

- [ ] CFOP is not Optimal, need to reimplement F2L and refactor PLL 
- [ ] Refactor `Cube` class to be more easy to understand
- [ ] Replace VisualCube with a custom implementation of a 3D cube visualization
- [ ] Add more solvers
- [ ] Add support for other cube sizes (2x2x2, 4x4x4, 5x5x5, etc.)
- [ ] Add support for other cube types (Pyraminx, Megaminx, etc.)

## Installation

Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/LindomarRodrigues/MagicCube.git
cd rubiks-cube
```

Install the required packages:

```bash
pip install -r requirements.txt
```

## Usage

To use the utility, import the `Cube` class from the `cube` module:

```python
from cube import Cube
```

Create a new instance of the `Cube` class:

```python
cube = Cube()
```

Print or plot the cube:

```python
cube.pprint()

# or

cube.plot()
```

Perform a sequence of moves:

```python
cube.move("R U R' U'")
```

Solver the cube using Layer by Layer (LBL) method:

```python
from solvers.layer_by_layer import LayerByLayerSolver

solver = LayerByLayerSolver(cube)
solver.solve()

print(solver.moves)
```

Or using the Fridrich(CFOP) method:

```python
from solvers.CFOP import CfopSolver

solver = CfopSolver(cube)
solver.solve()

print(solver.moves)
```

Optimize the sequence of moves:

```python
from solvers.optimizer import optimize_moves

print(len(moves))
moves = optimize_moves(moves)
print(len(moves))
```

## Misc

To use a custom [VisualCube](https://github.com/Cride5/visualcube) server, set the `VISUAL_CUBE_HOST` environment
variable:

```bash
export VISUAL_CUBE_HOST="http://localhost:80"
```









