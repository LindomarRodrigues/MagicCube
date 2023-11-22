import os
import random
from io import BytesIO

import requests
from matplotlib import image as mpimg, pyplot as plt

COLORS = {
    'W': 'white',
    'Y': 'yellow',
    'R': 'red',
    'O': 'orange',
    'B': 'blue',
    'G': 'green'
}

FACES = {
    'U': 'up',
    'D': 'down',
    'L': 'left',
    'R': 'right',
    'F': 'front',
    'B': 'back'
}

FACES_COLORS = {
    'U': 'Y',
    'D': 'W',
    'L': 'O',
    'R': 'R',
    'F': 'B',
    'B': 'G'
}

FACES_COLORS_INV = {v: k for k, v in FACES_COLORS.items()}

FACES_CODES = {
    'U': 0,
    'R': 1,
    'F': 2,
    'D': 3,
    'L': 4,
    'B': 5
}

FACES_CODES_INV = {v: k for k, v in FACES_CODES.items()}

CORNERS_CODES = {
    'URF': 0,
    'UFL': 1,
    'ULB': 2,
    'UBR': 3,
    'DFR': 4,
    'DLF': 5,
    'DBL': 6,
    'DRB': 7
}

CORNERS_CODES_INV = {v: k for k, v in CORNERS_CODES.items()}

EDGES_CODES = {
    'UR': 0,
    'UF': 1,
    'UL': 2,
    'UB': 3,
    'DR': 4,
    'DF': 5,
    'DL': 6,
    'DB': 7,
    'FR': 8,
    'FL': 9,
    'BL': 10,
    'BR': 11
}

EDGES_CODES_INV = {v: k for k, v in EDGES_CODES.items()}


class Cube:
    VISUAL_CUBE_HOST = 'http://cube.rider.biz' if not 'VISUAL_CUBE_HOST' in os.environ else os.environ[
        'VISUAL_CUBE_HOST']
    if VISUAL_CUBE_HOST[-1] == '/':
        VISUAL_CUBE_HOST = VISUAL_CUBE_HOST[:-1]

    ALLOWED_MOVES = [
        'U', 'U\'', 'U2',
        'R', 'R\'', 'R2',
        'F', 'F\'', 'F2',
        'D', 'D\'', 'D2',
        'L', 'L\'', 'L2',
        'B', 'B\'', 'B2'
    ]

    OTHERS_ALLOWED_MOVES = [
        'M', 'M\'', 'M2',
        'E', 'E\'', 'E2',
        'S', 'S\'', 'S2',
        'X', 'X\'', 'X2',
        'Y', 'Y\'', 'Y2',
        'Z', 'Z\'', 'Z2'
    ]

    def __init__(self):
        self.cube = {
            'corners': {
                'URF': CORNERS_CODES['URF'],
                'UFL': CORNERS_CODES['UFL'],
                'ULB': CORNERS_CODES['ULB'],
                'UBR': CORNERS_CODES['UBR'],
                'DFR': CORNERS_CODES['DFR'],
                'DLF': CORNERS_CODES['DLF'],
                'DBL': CORNERS_CODES['DBL'],
                'DRB': CORNERS_CODES['DRB']
            },
            'corners_rotations': {
                'URF': 0,
                'UFL': 0,
                'ULB': 0,
                'UBR': 0,
                'DFR': 0,
                'DLF': 0,
                'DBL': 0,
                'DRB': 0
            },
            'edges': {
                'UR': EDGES_CODES['UR'],
                'UF': EDGES_CODES['UF'],
                'UL': EDGES_CODES['UL'],
                'UB': EDGES_CODES['UB'],
                'DR': EDGES_CODES['DR'],
                'DF': EDGES_CODES['DF'],
                'DL': EDGES_CODES['DL'],
                'DB': EDGES_CODES['DB'],
                'FR': EDGES_CODES['FR'],
                'FL': EDGES_CODES['FL'],
                'BL': EDGES_CODES['BL'],
                'BR': EDGES_CODES['BR']
            },
            'edges_rotations': {
                'UR': 0,
                'UF': 0,
                'UL': 0,
                'UB': 0,
                'DR': 0,
                'DF': 0,
                'DL': 0,
                'DB': 0,
                'FR': 0,
                'FL': 0,
                'BL': 0,
                'BR': 0
            },
            'faces': {
                'U': FACES_CODES['U'],
                'D': FACES_CODES['D'],
                'L': FACES_CODES['L'],
                'R': FACES_CODES['R'],
                'F': FACES_CODES['F'],
                'B': FACES_CODES['B']
            }
        }

    def get_relative_piece_position(self, piece='URF'):

        piece = ''.join([FACES_CODES_INV[self.cube['faces'][face]] for face in piece])

        if len(piece) == 2:
            if piece not in EDGES_CODES:
                piece = piece[::-1]

        return piece

    def get_relative_piece(self, piece='URF'):
        piece = self.get_relative_piece_position(piece)
        relative_piece = ''

        if len(piece) == 1:
            relative_piece = FACES_CODES_INV[self.cube['faces'][piece]]
        elif len(piece) == 2:
            relative_piece = EDGES_CODES_INV[self.cube['edges'][piece]]
        elif len(piece) == 3:
            relative_piece = CORNERS_CODES_INV[self.cube['corners'][piece]]

        return self.get_relative_piece_position(relative_piece)

    def get_piece(self, piece='URF'):
        if len(piece) == 1:
            return FACES_CODES_INV[self.cube['faces'][piece]]
        elif len(piece) == 2:
            return EDGES_CODES_INV[self.cube['edges'][piece]]
        elif len(piece) == 3:
            return CORNERS_CODES_INV[self.cube['corners'][piece]]

    def get_face_piece_color(self, face, piece, error=True):
        if not error:
            if face not in piece:
                return None

        if len(piece) == 1:
            return FACES_COLORS[FACES_CODES_INV[self.cube['faces'][piece]]]
        elif len(piece) == 2:
            piece_idx = piece.index(face)
            piece_idx = piece_idx + self.cube['edges_rotations'][piece]

            while piece_idx not in [0, 1]:
                if piece_idx > 1:
                    piece_idx = piece_idx - 2
                elif piece_idx < 0:
                    piece_idx = piece_idx + 2

            return FACES_COLORS[EDGES_CODES_INV[self.cube['edges'][piece]][piece_idx]]
        elif len(piece) == 3:
            piece_idx = piece.index(face)
            piece_idx = piece_idx + self.cube['corners_rotations'][piece]

            while piece_idx not in [0, 1, 2]:
                if piece_idx > 2:
                    piece_idx = piece_idx - 3
                elif piece_idx < 0:
                    piece_idx = piece_idx + 3

            return FACES_COLORS[CORNERS_CODES_INV[self.cube['corners'][piece]][piece_idx]]

    def normalize_rotations(self):
        for piece in self.cube['corners_rotations']:
            self.cube['corners_rotations'][piece] = self.cube['corners_rotations'][piece] % 3

        for piece in self.cube['edges_rotations']:
            self.cube['edges_rotations'][piece] = self.cube['edges_rotations'][piece] % 2

    def get_relative_piece_color(self, face, piece):
        # piece = self.get_piece(piece)

        return self.get_face_piece_color(face, piece)

    def search_piece(self, piece):
        piece = self.get_relative_piece_position(piece)

        if len(piece) == 1:
            for face in FACES:
                if self.get_piece(face) == piece:
                    return face
        elif len(piece) == 2:
            for edge in EDGES_CODES:
                if self.get_piece(edge) == piece:
                    return edge
        elif len(piece) == 3:
            for corner in CORNERS_CODES:
                if self.get_piece(corner) == piece:
                    return corner

    def search_piece_rotation(self, piece):
        piece = self.get_relative_piece_position(piece)

        if len(piece) == 1:
            return 0
        elif len(piece) == 2:
            return self.cube['edges_rotations'][piece]
        elif len(piece) == 3:
            return self.cube['corners_rotations'][piece]

    def get_face_of_color(self, color, piece):
        for face in piece:
            if self.get_face_piece_color(face, piece) == color:
                return face

    def pprint(self):
        face = 'B'
        for piece_idx, piece in enumerate([
            'DBL', 'DB', 'DRB',
            'BL', 'B', 'BR',
            'ULB', 'UB', 'UBR',

            'DBL', 'BL', 'ULB', 'ULB', 'UB', 'UBR', 'UBR', 'BR', 'DRB', 'DRB', 'DB', 'DBL',
            'DL', 'L', 'UL', 'UL', 'U', 'UR', 'UR', 'R', 'DR', 'DR', 'D', 'DL',
            'DLF', 'FL', 'UFL', 'UFL', 'UF', 'URF', 'URF', 'FR', 'DFR', 'DFR', 'DF', 'DLF',

            'UFL', 'UF', 'URF',
            'FL', 'F', 'FR',
            'DLF', 'DF', 'DFR', ]):
            if piece_idx in [0, 3, 6, 45, 48, 51]:
                print('\n' + ' ' * 4, end='')
                if piece_idx >= 45:
                    face = 'F'


            elif piece_idx in [9, 21, 33]:
                print('\n', end='')
                face = 'L'
            elif piece_idx in [12, 24, 36]:
                print(' ', end='')
                face = 'U'
            elif piece_idx in [15, 27, 39]:
                print(' ', end='')
                face = 'R'
            elif piece_idx in [18, 30, 42]:
                print(' ', end='')
                face = 'D'

            print(self.get_face_piece_color(face, piece), end='')
        print()

    def facelet_colors(self):
        facelet_colors = [
            self.get_face_piece_color('U', 'ULB'), self.get_face_piece_color('U', 'UB'),
            self.get_face_piece_color('U', 'UBR'),
            self.get_face_piece_color('U', 'UL'), self.get_face_piece_color('U', 'U'),
            self.get_face_piece_color('U', 'UR'),
            self.get_face_piece_color('U', 'UFL'), self.get_face_piece_color('U', 'UF'),
            self.get_face_piece_color('U', 'URF'),

            self.get_face_piece_color('R', 'URF'), self.get_face_piece_color('R', 'UR'),
            self.get_face_piece_color('R', 'UBR'),
            self.get_face_piece_color('R', 'FR'), self.get_face_piece_color('R', 'R'),
            self.get_face_piece_color('R', 'BR'),
            self.get_face_piece_color('R', 'DFR'), self.get_face_piece_color('R', 'DR'),
            self.get_face_piece_color('R', 'DRB'),

            self.get_face_piece_color('F', 'UFL'), self.get_face_piece_color('F', 'UF'),
            self.get_face_piece_color('F', 'URF'),
            self.get_face_piece_color('F', 'FL'), self.get_face_piece_color('F', 'F'),
            self.get_face_piece_color('F', 'FR'),
            self.get_face_piece_color('F', 'DLF'), self.get_face_piece_color('F', 'DF'),
            self.get_face_piece_color('F', 'DFR'),

            self.get_face_piece_color('D', 'DLF'), self.get_face_piece_color('D', 'DF'),
            self.get_face_piece_color('D', 'DFR'),
            self.get_face_piece_color('D', 'DL'), self.get_face_piece_color('D', 'D'),
            self.get_face_piece_color('D', 'DR'),
            self.get_face_piece_color('D', 'DBL'), self.get_face_piece_color('D', 'DB'),
            self.get_face_piece_color('D', 'DRB'),

            self.get_face_piece_color('L', 'ULB'), self.get_face_piece_color('L', 'UL'),
            self.get_face_piece_color('L', 'UFL'),
            self.get_face_piece_color('L', 'BL'), self.get_face_piece_color('L', 'L'),
            self.get_face_piece_color('L', 'FL'),
            self.get_face_piece_color('L', 'DBL'), self.get_face_piece_color('L', 'DL'),
            self.get_face_piece_color('L', 'DLF'),

            self.get_face_piece_color('B', 'UBR'), self.get_face_piece_color('B', 'UB'),
            self.get_face_piece_color('B', 'ULB'),
            self.get_face_piece_color('B', 'BR'), self.get_face_piece_color('B', 'B'),
            self.get_face_piece_color('B', 'BL'),
            self.get_face_piece_color('B', 'DRB'), self.get_face_piece_color('B', 'DB'),
            self.get_face_piece_color('B', 'DBL')

        ]
        return facelet_colors
    def facelet(self):
        facelet_colors = self.facelet_colors()

        facelet = [FACES_COLORS_INV[color] for color in facelet_colors]

        return facelet

    def move(self, move, direction='cw', quantity=1):
        faces_swap = []
        if move == 'U':
            corners_swap = ['URF', 'UBR', 'ULB', 'UFL']
            edges_swap = ['UL', 'UF', 'UR', 'UB']

            corners_swap_rotations = [0, 0, 0, 0]
            edges_swap_rotations = [0, 0, 0, 0]
        elif move == 'D':
            corners_swap = ['DLF', 'DBL', 'DRB', 'DFR']
            edges_swap = ['DL', 'DB', 'DR', 'DF']

            corners_swap_rotations = [0, 0, 0, 0]
            edges_swap_rotations = [0, 0, 0, 0]
        elif move == 'R':

            corners_swap = ['URF', 'DFR', 'DRB', 'UBR']
            edges_swap = ['UR', 'FR', 'DR', 'BR']

            corners_swap_rotations = [1, 2, 1, 2]
            edges_swap_rotations = [0, 0, 0, 0]

        elif move == 'L':
            corners_swap = ['UFL', 'ULB', 'DBL', 'DLF']
            edges_swap = ['UL', 'BL', 'DL', 'FL']

            corners_swap_rotations = [2, 1, 2, 1]
            edges_swap_rotations = [0, 0, 0, 0]

        elif move == 'F':
            corners_swap = ['UFL', 'DLF', 'DFR', 'URF']
            edges_swap = ['UF', 'FL', 'DF', 'FR']

            corners_swap_rotations = [1, 2, 1, 2]
            edges_swap_rotations = [1, 1, 1, 1]

        elif move == 'B':
            corners_swap = ['UBR', 'DRB', 'DBL', 'ULB']
            edges_swap = ['UB', 'BR', 'DB', 'BL']

            corners_swap_rotations = [1, 2, 1, 2]
            edges_swap_rotations = [1, 1, 1, 1]

        elif move == 'M':
            corners_swap = []
            edges_swap = ['UF', 'UB', 'DB', 'DF']
            faces_swap = ['U', 'B', 'D', 'F']

            corners_swap_rotations = []
            edges_swap_rotations = [1, 1, 1, 1]
        elif move == 'E':
            corners_swap = []
            edges_swap = ['FL', 'BL', 'BR', 'FR']
            faces_swap = ['F', 'L', 'B', 'R']

            corners_swap_rotations = []
            edges_swap_rotations = [1, 1, 1, 1]
        elif move == 'S':
            corners_swap = []
            edges_swap = ['UL', 'DL', 'DR', 'UR']

            faces_swap = ['L', 'D', 'R', 'U']

            corners_swap_rotations = []
            edges_swap_rotations = [1, 1, 1, 1]

        elif move in ['X', 'Y', 'Z']:
            for _ in range(quantity):
                self.rotate_cube('x' if move == 'X' else 'y' if move == 'Y' else 'z', direction)

            return

        if direction == 'ccw' or quantity == 3:
            edges_swap = edges_swap[::-1]
            corners_swap = corners_swap[::-1]

            edges_swap_rotations = edges_swap_rotations[::-1]
            corners_swap_rotations = corners_swap_rotations[::-1]

            faces_swap = faces_swap[::-1]

        if len(corners_swap) == 4:
            (self.cube['corners'][corners_swap[0]],
             self.cube['corners'][corners_swap[1]],
             self.cube['corners'][corners_swap[2]],
             self.cube['corners'][corners_swap[3]]) = (
                self.cube['corners'][corners_swap[1]],
                self.cube['corners'][corners_swap[2]],
                self.cube['corners'][corners_swap[3]],
                self.cube['corners'][corners_swap[0]])

            (self.cube['corners_rotations'][corners_swap[0]],
             self.cube['corners_rotations'][corners_swap[1]],
             self.cube['corners_rotations'][corners_swap[2]],
             self.cube['corners_rotations'][corners_swap[3]]) = (
                self.cube['corners_rotations'][corners_swap[1]] + corners_swap_rotations[0],
                self.cube['corners_rotations'][corners_swap[2]] + corners_swap_rotations[1],
                self.cube['corners_rotations'][corners_swap[3]] + corners_swap_rotations[2],
                self.cube['corners_rotations'][corners_swap[0]] + corners_swap_rotations[3])

        (self.cube['edges'][edges_swap[0]],
         self.cube['edges'][edges_swap[1]],
         self.cube['edges'][edges_swap[2]],
         self.cube['edges'][edges_swap[3]]) = (
            self.cube['edges'][edges_swap[1]],
            self.cube['edges'][edges_swap[2]],
            self.cube['edges'][edges_swap[3]],
            self.cube['edges'][edges_swap[0]])

        (self.cube['edges_rotations'][edges_swap[0]],
         self.cube['edges_rotations'][edges_swap[1]],
         self.cube['edges_rotations'][edges_swap[2]],
         self.cube['edges_rotations'][edges_swap[3]]) = (
            self.cube['edges_rotations'][edges_swap[1]] + edges_swap_rotations[0],
            self.cube['edges_rotations'][edges_swap[2]] + edges_swap_rotations[1],
            self.cube['edges_rotations'][edges_swap[3]] + edges_swap_rotations[2],
            self.cube['edges_rotations'][edges_swap[0]] + edges_swap_rotations[3])

        if len(faces_swap) == 4:
            (self.cube['faces'][faces_swap[0]],
             self.cube['faces'][faces_swap[1]],
             self.cube['faces'][faces_swap[2]],
             self.cube['faces'][faces_swap[3]]) = (
                self.cube['faces'][faces_swap[1]],
                self.cube['faces'][faces_swap[2]],
                self.cube['faces'][faces_swap[3]],
                self.cube['faces'][faces_swap[0]])

        if quantity == 2:
            self.move(move, direction, 1)

    def rotate_cube(self, ax='x', direction='cw'):
        if ax == 'x':
            self.move('R', direction)
            self.move('L', 'cw' if direction == 'ccw' else 'ccw')
            self.move('M', 'cw' if direction == 'ccw' else 'ccw')
        elif ax == 'y':
            self.move('U', direction)
            self.move('D', 'cw' if direction == 'ccw' else 'ccw')
            self.move('E', 'cw' if direction == 'ccw' else 'ccw')
        elif ax == 'z':
            self.move('F', direction)
            self.move('B', 'cw' if direction == 'ccw' else 'ccw')
            self.move('S', direction)

    def is_solved(self, cube_rotates=None):
        facelets = self.facelet_colors()

        for i in range(0, 54, 9):
            if facelets[i:i + 9] != [facelets[i]] * 9:
                return False

        return True

    def is_cross_solved(self):

        for edge in [edge for edge in EDGES_CODES if 'D' in edge]:
            for face in edge:
                if self.get_face_piece_color(face, edge) != self.get_face_piece_color(face, face):
                    return False

        return True

    def moves(self, moves=None):
        moves_ = ['F', 'F\'', 'F2', 'B', 'B\'', 'B2', 'R', 'R\'', 'R2', 'L', 'L\'', 'L2', 'U', 'U\'', 'U2', 'D', 'D\'',
                  'D2']

        if moves is None:
            moves = random.choices(moves_, k=100)
        elif type(moves) is str:
            moves = moves.split(' ')

        for move in moves:
            self.move(move[0],
                      'cw' if len(move) == 1 else 'ccw' if move[1] == '\'' else 'cw',
                      1 if len(move) == 1 else 2 if move[1] == '2' else 1)

    def visualcube_url(self):
        url = f"{self.VISUAL_CUBE_HOST}/visualcube.php?fmt=png&size=200&fc={''.join(self.facelet_colors()).lower()}"
        return url

    def visualcube_image(self):
        response = requests.get(self.visualcube_url())
        return mpimg.imread(BytesIO(response.content))

    def plot(self):
        img = self.visualcube_image()
        plt.imshow(img)
        plt.show()

    def white_to_bottom(self):
        if self.cube['faces']['U'] == FACES_CODES['D']:
            self.move('X', 'cw', 2)

        elif self.cube['faces']['F'] == FACES_CODES['D']:
            self.move('X', 'ccw', 1)
        elif self.cube['faces']['B'] == FACES_CODES['D']:
            self.move('X', 'cw', 1)

        elif self.cube['faces']['R'] == FACES_CODES['D']:
            self.move('Z', 'cw', 1)
        elif self.cube['faces']['L'] == FACES_CODES['D']:
            self.move('Z', 'ccw', 1)
        else:
            return

    def blue_to_front(self):

        if self.cube['faces']['R'] == FACES_CODES['F']:
            self.move('Y', 'cw', 1)
        elif self.cube['faces']['L'] == FACES_CODES['F']:
            self.move('Y', 'ccw', 1)
        elif self.cube['faces']['B'] == FACES_CODES['F']:
            self.move('Y', 'cw', 2)
        else:
            return
