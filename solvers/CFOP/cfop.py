from cube import FACES_CODES, Cube
from solvers.CFOP.cfop_db import F2lDb

ALGORITHMS_F2L = {f2l_db.case: f2l_db.alg for f2l_db in F2lDb.select()}


class CfopSolver:
    def __init__(self, cube: Cube):
        self.cube = cube
        self.moves = []

    def solve(self):
        self.white_to_bottom()

        self.blue_to_front()

        self.solve_cross()
        self.solve_f2l()
        self.solve_oll()
        self.solve_pll()

        self.white_to_bottom()
        self.blue_to_front()

    def solve_cross(self):
        for _ in range(4):
            df_edge = self.cube.search_piece('DF')

            if (df_edge == 'DF'
                    and self.cube.get_relative_piece_color('D', 'DF') == self.cube.get_face_piece_color('D',
                                                                                                        'D')):
                ...
            elif df_edge == 'DF':
                self.moves += "F D' L D".split(' ')
                self.cube.moves("F D' L D")
            elif df_edge == 'UB':
                if self.cube.get_relative_piece_color('U', df_edge) == self.cube.get_face_piece_color('D', 'D'):
                    self.moves += "U2 F2".split(' ')
                    self.cube.moves("U2 F2")
                else:
                    self.moves += "U R' F R".split(' ')
                    self.cube.moves("U R' F R")
            elif df_edge == 'UL':
                if self.cube.get_relative_piece_color('U', df_edge) == self.cube.get_face_piece_color('D', 'D'):
                    self.moves += "U' F2".split(' ')
                    self.cube.moves("U' F2")
                else:
                    self.moves += "L F' L'".split(' ')
                    self.cube.moves("L F' L'")
            elif df_edge == 'BL':
                if self.cube.get_relative_piece_color('L', df_edge) == self.cube.get_face_piece_color('D', 'D'):
                    self.moves += "D2 B D2".split(' ')
                    self.cube.moves("D2 B D2")
                else:
                    self.moves += "D' L' D".split(' ')
                    self.cube.moves("D' L' D")
            elif df_edge == 'FL':
                if self.cube.get_relative_piece_color('F', df_edge) == self.cube.get_face_piece_color('D', 'D'):
                    self.moves += "D' L D".split(' ')
                    self.cube.moves("D' L D")
                else:
                    self.moves += "F'".split(' ')
                    self.cube.moves("F'")
            elif df_edge == 'DR':
                if self.cube.get_relative_piece_color('R', df_edge) == self.cube.get_face_piece_color('D', 'D'):
                    self.moves += "R F".split(' ')
                    self.cube.moves("R F")
                else:
                    self.moves += "R D R' D'".split(' ')
                    self.cube.moves("R D R' D'")
            elif df_edge == 'FR':
                if self.cube.get_relative_piece_color('F', df_edge) == self.cube.get_face_piece_color('D', 'D'):
                    self.moves += "D R' D'".split(' ')
                    self.cube.moves("D R' D'")
                else:
                    self.moves += "F".split(' ')
                    self.cube.moves("F")
            elif df_edge == 'DL':
                if self.cube.get_relative_piece_color('L', df_edge) == self.cube.get_face_piece_color('D', 'D'):
                    self.moves += "L' F'".split(' ')
                    self.cube.moves("L' F'")
                else:
                    self.moves += "L' D' L D".split(' ')
                    self.cube.moves("L' D' L D")
            elif df_edge == 'UR':
                if self.cube.get_relative_piece_color('U', df_edge) == self.cube.get_face_piece_color('D', 'D'):
                    self.moves += "U F2".split(' ')
                    self.cube.moves("U F2")
                else:
                    self.moves += "R' F R".split(' ')
                    self.cube.moves("R' F R")
            elif df_edge == 'UF':
                if self.cube.get_relative_piece_color('U', df_edge) == self.cube.get_face_piece_color('D', 'D'):
                    self.moves += "F2".split(' ')
                    self.cube.moves("F2")
                else:
                    self.moves += "U' R' F R".split(' ')
                    self.cube.moves("U' R' F R")
            elif df_edge == 'DB':
                if self.cube.get_relative_piece_color('D', df_edge) == self.cube.get_face_piece_color('D', 'D'):
                    self.moves += "B2 U2 F2".split(' ')
                    self.cube.moves("B2 U2 F2")
                else:
                    self.moves += "B2 U R' F R".split(' ')
                    self.cube.moves("B2 U R' F R")
            elif df_edge == 'BR':
                if self.cube.get_relative_piece_color('R', df_edge) == self.cube.get_face_piece_color('D', 'D'):
                    self.moves += "R2 F R2".split(' ')
                    self.cube.moves("R2 F R2")
                else:
                    self.moves += "D R D'".split(' ')
                    self.cube.moves("D R D'")

            self.moves.append("Y")
            self.cube.moves("Y")

    def solve_f2l(self):
        for _ in range(4):
            dfr_corner = self.cube.search_piece('DFR')
            fr_edge = self.cube.search_piece('FR')
            white_corner_face = self.cube.get_face_of_color(self.cube.get_face_piece_color('D', 'D'), dfr_corner)
            white_edge_face = self.cube.get_face_of_color(self.cube.get_face_piece_color('F', 'F'), fr_edge)

            case = (dfr_corner[dfr_corner.index(white_corner_face):] +
                    dfr_corner[:dfr_corner.index(white_corner_face)] +
                    fr_edge[fr_edge.index(white_edge_face):] +
                    fr_edge[:fr_edge.index(white_edge_face)])

            alg = ALGORITHMS_F2L[case]
            if alg != '':
                self.moves += alg.split(' ')
                self.cube.moves(alg)

            self.moves.append("Y")
            self.cube.moves("Y")

    def solve_oll(self):
        ALGORITHMS_OLL = {
            "LBRLURLFR": ['R', 'U', "B'", 'R', 'B', 'R2', "U'", "R'", 'F', 'R', "F'"],
            "LBRLURFFF": ['R', "B'", "R'", 'U2', 'F', 'R', "B'", 'R', 'B2', 'R2', "F'"],
            "BBRLURLFU": ["F'", 'B', 'L', "B'", 'U2', 'B', 'L', "F'", 'L', 'F2', "B'"],
            "LBULURFFR": ["R'", 'U2', "R'", 'F', 'R', "F'", "U'", "F'", "U'", 'F', "U'", 'R'],
            "UBBLURLFU": ['R', 'U', 'B', "U'", "B'", 'U', "R'", "U'", "R'", 'F', 'R', "F'"],
            "UBULURUFU": ['R', "L'", 'F2', 'R2', 'D2', 'R2', "B'", "R'", 'L', 'D2', 'L2', 'F2', 'L2'],
            "UBULURLFR": ["R'", 'U2', 'F', 'R', 'U', "R'", "U'", 'F2', 'U2', 'F', 'R'],
            "BBBLURUFU": ['F', 'R', 'U', "R'", 'U', "F'", 'U2', "F'", 'L', 'F', "L'"],
            "BURLURFUR": ['R', 'U', "R'", 'U', 'R', "U'", 'B', "U'", "B'", "R'"],
            "LURLURLUR": ['R', "U'", 'B2', 'D', "B'", 'U2', 'B', "D'", 'B2', 'U', "R'"],
            "BBRUUUFFR": ["F", "U", "R", "U'", "R'", "U", "R", "U'", "R'", "F'"],
            "LBRUUULFR": ["L'", "B'", "L", "U'", "R'", "U", "R", "U'", "R'", "U", "R", "L'", "B", "L"],
            "BURUUUFUR": ["L", "U'", "R'", "U", "L'", "U", "R", "U", "R'", "U", "R"],
            "LURUUULUR": ["R", "U", "R'", "U", "R", "U'", "R'", "U", "R", "U2", "R'"],
            "LUBUUUFUU": ["L'", "U", "R", "U'", "L", "U", "R'"],
            "BURUUULUU": ["R'", "U2", "R", "U", "R'", "U", "R"],
            "UUBUUUUUF": ["R'", "F'", "L", "F", "R", "F'", "L'", "F"],
            "UUUUUUFUF": ["R2", "D", "R'", "U2", "R", "D'", "R'", "U2", "R'"],
            "UUBUUULUU": ["R'", "F'", "L'", "F", "R", "F'", "L", "F"],
            "UBUUURUUU": ['B', 'R', 'D2', 'F2', 'U2', 'L', 'F2', 'D2', 'B'],
            "UBUUUUUFU": ["L'", "R", "U", "R'", "U'", "L", "R'", "F", "R", "F'"],
            "BURUURUFF": ["L", "F", "R'", "F", "R", "F2", "L'"],
            "UURUURFFU": ["F", "R'", "F'", "R", "U", "R", "U'", "R'"],
            "LUBUURFFU": ["R'", "U'", 'R', 'F', "R'", "F'", 'U', 'F', 'R', "F'"],
            "BUBUURUFU": ['F', 'U2', "F'", "U'", 'F', "U'", 'F2', "L'", "U'", 'L', 'U', 'F', "U'"],
            "LUBUURLFF": ["F", "R", "U", "R'", "U'", "R", "U", "R'", "U'", "F'"],
            "BUBUURFFF": ['L', "F'", "L'", 'F', 'U2', 'L2', 'B', 'L', "B'", 'L'],
            "BUBLUUUFU": ["F'", 'U2', 'F', 'U', "F'", 'U', 'F2', 'R', 'U', "R'", "U'", "F'", "U'"],
            "LUULUUFFR": ['L', 'F2', "R'", "F'", 'R', "F'", "L'"],
            "BUULUUUFR": ["R'", 'U2', 'R2', "B'", "R'", 'B', "R'", 'U2', 'R'],
            "BURLUUFFR": ["F'", "L'", "U'", "L", "U", "L'", "U'", "L", "U", "F"],
            "LUBLUULFF": ["R'", 'F', "R'", "F'", 'R2', 'U2', "B'", 'R', 'B', "R'"],
            "BUBLUUFFF": ["R'", 'F', 'R', "F'", 'U2', 'R2', "B'", "R'", 'B', "R'"],
            "BBUUURLUF": ['R', 'U', "R'", "B'", 'R', 'B', "U'", "B'", "R'", 'B'],
            "UBBUURFUR": ["L'", "B'", "L", "U'", "R'", "U", "R", "L'", "B", "L"],
            "LBBUURFUU": ['R', 'L2', "B'", 'L', "B'", "L'", 'B2', 'L', "B'", "R'", 'L', 'U2'],
            "UBUUURLUR": ["B'", 'R', "B'", 'R2', 'U', 'R', 'U', "R'", "U'", 'R', 'B2'],
            "LBBLUULUF": ['L', "U'", "F'", 'U2', "F'", 'U', 'F', "U'", 'F', 'U2', 'F', "U'", "L'"],
            "BBRLUUUUF": ['R2', "L'", 'B', "R'", 'B', 'R', 'B2', "R'", 'B', "R'", 'L', 'U2'],
            "UBULUULUR": ['B', 'U', 'L', "U'", 'F', "L'", "B'", 'L', "F'", "L'"],
            "BBRLUULUU": ["L'", 'B2', 'R', 'B', "R'", 'B', 'L'],
            "UURLURUUR": ['R', 'U', 'R', "B'", "R'", 'B', "U'", "R'"],
            "LBRUUUUFU": ['R', 'U', "R'", "U'", "B'", "R'", 'F', 'R', "F'", 'B'],
            "LBBUUUFFU": ["R'", 'F', 'R', 'U', "R'", "F'", 'R', 'F', "U'", "F'"],
            "BBRUUUUFF": ['L', "F'", "L'", "U'", 'L', 'F', "L'", "F'", 'U', 'F'],
            "BBRUUULFU": ["L'", "B'", "L", "R'", "U'", "R", "U", "L'", "B", "L"],
            "LBBUUUUFR": ["R", "B", "R'", "L", "U", "L'", "U'", "R", "B'", "R'"],
            "UURUURUFR": ["F", "U", "R", "U'", "R'", "F'"],
            "BUULUUFFU": ["R'", "U'", 'F', 'U', 'R', "U'", "R'", "F'", 'R'],
            "UUBUURUFF": ["R'", 'L', "U'", "F'", 'U', 'F', 'R', 'U', "L'"],
            "LUULUULFU": ["F'", "U'", "L'", "U", "L", "F"],
            "LBUUUULFU": ["F", "R", "U", "R'", "U'", "F'"],
            "BBUUUUFFU": ["R", "U", "R'", "U'", "R'", "F", "R", "F'"],
            "LBULUUUUF": ['B', "U'", "L'", 'B', 'L', 'D', "F'", 'L', 'F', "D'", 'B2'],
            "UBRUURFUU": ["B'", 'U', 'R', "B'", "R'", "D'", 'F', "R'", "F'", 'D', 'B2'],
            "UBBUUULFU": ["R'", 'U', 'L', 'F', 'U', "F'", "U'", 'R', "L'"],
            "BBUUUUUFR": ['L', "U'", "R'", "F'", "U'", 'F', 'U', 'R', "L'"],

        }

        for _ in range(4):
            orientation = ''.join([
                self.cube.get_face_of_color('Y', 'ULB')
                , self.cube.get_face_of_color('Y', 'UB')
                , self.cube.get_face_of_color('Y', 'UBR'),

                self.cube.get_face_of_color('Y', 'UL'),
                self.cube.get_face_of_color('Y', 'U'),
                self.cube.get_face_of_color('Y', 'UR'),

                self.cube.get_face_of_color('Y', 'UFL'),
                self.cube.get_face_of_color('Y', 'UF'),
                self.cube.get_face_of_color('Y', 'URF'),

            ])

            if orientation in ALGORITHMS_OLL:
                self.moves += ALGORITHMS_OLL[orientation]
                self.cube.moves(' '.join(ALGORITHMS_OLL[orientation]))

                return

            self.moves.append('U')
            self.cube.moves('U')

    def solve_pll(self):
        ALGORITHMS_PLL = {
            '010343101434': ['R2', 'F2', 'B2', 'L2', 'D', 'R2', 'F2', 'B2', 'L2'],
            '012121660206': ["R'", 'L', 'F2', 'R', "L'", 'B2', 'U', 'L2', "U'", 'R2', 'U', 'F2', 'R2', 'D', 'L2'],
            '012323100231': ['R', 'L', 'U2', "R'", "L'", 'U', 'F2', 'U', 'B2', "U'", 'B2', 'D', 'L2', "D'", 'F2'],
            '002340233424': ['F2', "U'", 'F2', 'D', 'R2', 'B2', 'U', 'B2', "D'", 'R2'],
            '012101620266': ['R', 'B', "R'", 'F2', 'R', "B'", 'R', 'D2', 'B2', "D'", 'B2', "D'", 'R2', 'F2'],
            '012141400224': ['R2', 'B2', "D'", 'F2', 'D', 'B2', "D'", 'F2', 'D', 'R2'],
            '011300666133': ['F2', 'R', 'U', "R'", 'F2', 'L', "D'", 'L', 'D', 'L2'],
            '000343474737': ['R', 'L', 'U2', 'R', 'L', 'U', 'B2', 'L2', 'F2', 'U', 'F2', 'R2', 'L2', 'F2', 'D'],
            '012100626261': ['F', 'U', "F'", 'L2', 'B', "D'", 'B', 'D2', 'R2', "U'", 'L2', 'F2', 'U', 'R2', "D'"],
            '002330223999': ['F2', "U'", 'F2', 'D', 'F2', "D'", 'L2', 'U', 'L2', 'F2'],
            '012140221404': ['R', "L'", 'D2', 'R', "L'", 'U', 'F2', "U'", 'F2', 'D', 'F2', 'R2', 'D', 'L2'],
            '010101676767': ['R', 'F2', 'R2', 'L2', 'B2', 'R', 'L2', 'U', 'R2', 'L2', 'D', 'R2', 'L2'],
            '012331200123': ["R'", "U'", 'R', 'F2', "R'", 'U', 'R', 'U', 'F2', "U'", 'F2', "U'", 'F2'],
            '011335150503': ["R'", 'U', "R'", "U'", 'R', "D'", "R'", 'D', "R'", 'B2', "U'", 'B2', 'U', 'R2'],
            '010301663136': ['R', "D'", 'R', 'F2', "L'", 'U', 'L', "U'", 'R2', 'U2', 'R2', 'F2', 'D', 'R2'],
            '011344100433': ['R', 'U', "R'", 'B2', 'R', "U'", 'R', 'L2', "D'", 'F2', 'D', 'R2', 'L2', 'B2', 'U', 'B2'],
            '010303666131': ['F2', "U'", 'R2', 'B2', 'L2', 'D', 'L2', 'B2', 'R2', 'U2', 'F2'],
            '010305133551': ['F', "R'", 'F', 'L2', "F'", 'R', 'F', 'L2', 'F2'],
            '012120201999': ['R', "U'", 'R', 'F2', "R'", 'U', 'R', 'L2', 'D', 'R2', 'L2', 'U', 'L2', 'B2', 'L2'],
            '002335220553': ['R', 'L', 'F2', 'D2', "R'", 'L', 'D', 'B2', 'L2', 'U2', 'L2', 'D', 'L2', 'F2', 'U2', 'F2'],
            '012321230103': ['R', 'U2', 'R2', 'D', 'R2', 'U2', 'R', 'B2', 'U', 'R2', 'U', 'R2', 'U2', 'B2', "D'", 'R2'],
            '000333666999': [],

        }

        self.blue_to_front()
        self.white_to_bottom()

        for _ in range(4):
            orientation = ''.join([

                self.cube.get_face_piece_color('L', 'ULB'),
                self.cube.get_face_piece_color('L', 'UL'),
                self.cube.get_face_piece_color('L', 'UFL'),

                self.cube.get_face_piece_color('F', 'UFL'),
                self.cube.get_face_piece_color('F', 'UF'),
                self.cube.get_face_piece_color('F', 'URF'),

                self.cube.get_face_piece_color('R', 'URF'),
                self.cube.get_face_piece_color('R', 'UR'),
                self.cube.get_face_piece_color('R', 'UBR'),

                self.cube.get_face_piece_color('B', 'UBR'),
                self.cube.get_face_piece_color('B', 'UB'),
                self.cube.get_face_piece_color('B', 'ULB'),

            ])
            orientation = ''.join([str(orientation.index(color)) for color in orientation])
            if orientation in ALGORITHMS_PLL:
                self.moves += ALGORITHMS_PLL[orientation]
                self.cube.moves(ALGORITHMS_PLL[orientation])

                while self.cube.get_face_piece_color('F', 'UF') != self.cube.get_face_piece_color('F', 'F'):
                    self.moves.append('U')
                    self.cube.moves('U')

                return

            self.moves.append('U')
            self.cube.moves('U')

    def white_to_bottom(self):
        if self.cube.cube['faces']['U'] == FACES_CODES['D']:
            self.cube.move('X', 'cw', 2)
            self.moves.append('x2')

        elif self.cube.cube['faces']['F'] == FACES_CODES['D']:
            self.cube.move('X', 'ccw', 1)
            self.moves.append('x\'')
        elif self.cube.cube['faces']['B'] == FACES_CODES['D']:
            self.cube.move('X', 'cw', 1)
            self.moves.append('x')

        elif self.cube.cube['faces']['R'] == FACES_CODES['D']:
            self.cube.move('Z', 'cw', 1)
            self.moves.append('z')
        elif self.cube.cube['faces']['L'] == FACES_CODES['D']:
            self.cube.move('Z', 'ccw', 1)
            self.moves.append('z\'')
        else:
            return

    def blue_to_front(self):

        if self.cube.cube['faces']['R'] == FACES_CODES['F']:
            self.cube.move('Y', 'cw', 1)
            self.moves.append('y')
        elif self.cube.cube['faces']['L'] == FACES_CODES['F']:
            self.cube.move('Y', 'ccw', 1)
            self.moves.append('y\'')
        elif self.cube.cube['faces']['B'] == FACES_CODES['F']:
            self.cube.move('Y', 'cw', 2)
            self.moves.append('y2')
        else:
            return
