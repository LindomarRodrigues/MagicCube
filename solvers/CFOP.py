from cube import FACES_CODES, Cube


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
        ALGORITHMS_EDGE_TO_TOP = {
            'FR': "U R U R' U2",
            'FL': "L' U' L U",
            'BL': "L U' L' U",
            'BR': "U R' U R U2"
        }

        ALGORITHMS_F2l_TOP_PIECES = {
            'UL': {
                'U': {
                    'U': "U2 R U R' U R U' R'",
                    'L': "U' R U' R2 F R F' R U' R'"
                },
                'R': {
                    'L': "U F' U' F U2 F' U F",
                    'U': "U' R U R' U R U R'"
                },
                'F': {
                    'U': "U' R U2 R' U' R U2 R'",
                    'L': "F' U' F"
                }

            },
            'UF': {
                'R': {
                    'U': "R U' R' U R U' R' U2 R U' R'",
                    'F': "F R' F' R"
                },
                'U': {
                    'F': "R' F R F' R U' R' U R U' R'",
                    'U': "U F R' F' R U R U R'"
                },
                'F': {
                    'F': "R U' R' U R' F R F' R U' R'",
                    'U': "R' D' R U' R' D R U R U' R'"
                }
            },
            'UB': {
                'F': {
                    'U': "U' R U R' U2 R U' R'",
                    'B': "U' R U' R' U F' U' F"
                },
                'U': {
                    'B': "F' L' U2 L F",
                    'U': "U R U2 R' U R U' R'"
                },
                'R': {
                    'B': "Y' U R' U2 R U2 R' U R Y",
                    'U': "R U R'"
                }
            },
            'UR': {
                'F': {
                    'R': "U' R U2 R' U F' U' F",
                    'U': "U R U' R'"
                },
                'U': {
                    'R': "F U R U' R' F' R U' R'",
                    'U': "R U2 R' U' R U R'"
                },
                'R': {
                    'U': "U' R U' R' U R U R'",
                    'R': "R U' R' U2 F' U' F"
                }
            },

        }

        for _ in range(4):
            dfr_corner = self.cube.search_piece('DFR')
            if 'U' not in dfr_corner:
                if dfr_corner == 'DFR':
                    self.moves += "R U R'".split(' ')
                    self.cube.moves("R U R'")
                elif dfr_corner == 'DLF':
                    self.moves += "L' U' L".split(' ')
                    self.cube.moves("L' U' L")
                elif dfr_corner == 'DBL':
                    self.moves += "L U2 L'".split(' ')
                    self.cube.moves("L U2 L'")
                elif dfr_corner == 'DRB':
                    self.moves += "R' U2 R U'".split(' ')
                    self.cube.moves("R' U2 R U'")

            while self.cube.search_piece('DFR') != 'URF':
                self.cube.moves("U")
                self.moves.append("U")

            fr_edge = self.cube.search_piece('FR')

            if 'U' not in fr_edge:
                self.moves += ALGORITHMS_EDGE_TO_TOP[fr_edge].split(' ')
                self.cube.moves(ALGORITHMS_EDGE_TO_TOP[fr_edge])

            dfr_corner = self.cube.search_piece('DFR')
            fr_edge = self.cube.search_piece('FR')

            down_face_color = self.cube.get_face_piece_color('D', 'D')

            for face in dfr_corner:
                if self.cube.get_relative_piece_color(face, dfr_corner) == down_face_color:
                    white_corner_face = face

            front_face_color = self.cube.get_face_piece_color('F', 'F')

            for face in fr_edge:
                if self.cube.get_relative_piece_color(face, fr_edge) == front_face_color:
                    white_edge_face = face


            self.moves += ALGORITHMS_F2l_TOP_PIECES[fr_edge][white_corner_face][white_edge_face].split(' ')
            self.cube.moves(ALGORITHMS_F2l_TOP_PIECES[fr_edge][white_corner_face][white_edge_face])

            self.moves.append("Y")
            self.cube.moves("Y")

    def solve_oll(self):
        ALGORITHMS_OLL = {
            "LBRLURLFR": ["R", "U", "B'", "X'", "R", "U", "X2", "R2", "X'", "U'", "R'", "F", "R", "F'"],
            "LBRLURFFF": ["R'", "F", "R", "F'", "U2", "R'", "F", "R", "Y'", "R2", "U2", "R"],
            "BBRLURLFU": ["Y", "M", "U", "X", "R'", "U2", "X'", "R", "U", "L'", "U", "L", "M'"],
            "LBULURFFR": ["R'", "U2", "X", "R'", "U", "R", "U'", "Y", "R'", "U'", "R'", "U", "R'", "F", "Z'"],
            "UBBLURLFU": ["R", "U", "R'", "U", "R'", "F", "R", "F'", "U2", "R'", "F", "R", "F'"],
            "UBULURUFU": ["M'", "U2", "M", "U2", "M'", "U", "M", "U2", "M'", "U2", "M"],
            "UBULURLFR": ["R'", "U2", "F", "R", "U", "R'", "U'", "Y'", "R2", "U2", "X'", "R", "U", "X"],
            "BBBLURUFU": ["F", "R", "U", "R'", "U", "Y'", "R'", "U2", "R'", "F", "R", "F'"],
            "BURLURFUR": ["R'", "U'", "Y", "L'", "U", "L'", "Y'", "L", "F", "L'", "F", "R"],
            "LURLURLUR": ["R", "U'", "Y", "R2", "D", "R'", "U2", "R", "D'", "R2", "Y'", "U", "R'"],
            "BBRUUUFFR": ["F", "U", "R", "U'", "R'", "U", "R", "U'", "R'", "F'"],
            "LBRUUULFR": ["L'", "B'", "L", "U'", "R'", "U", "R", "U'", "R'", "U", "R", "L'", "B", "L"],
            "BURUUUFUR": ["L", "U'", "R'", "U", "L'", "U", "R", "U", "R'", "U", "R"],
            "LURUUULUR": ["R", "U", "R'", "U", "R", "U'", "R'", "U", "R", "U2", "R'"],
            "LUBUUUFUU": ["L'", "U", "R", "U'", "L", "U", "R'"],
            "BURUUULUU": ["R'", "U2", "R", "U", "R'", "U", "R"],
            "UUBUUUUUF": ["R'", "F'", "L", "F", "R", "F'", "L'", "F"],
            "UUUUUUFUF": ["R2", "D", "R'", "U2", "R", "D'", "R'", "U2", "R'"],
            "UUBUUULUU": ["R'", "F'", "L'", "F", "R", "F'", "L", "F"],
            "UBUUURUUU": ["M'", "U'", "M", "U2", "M'", "U'", "M"],
            "UBUUUUUFU": ["L'", "R", "U", "R'", "U'", "L", "R'", "F", "R", "F'"],
            "BURUURUFF": ["L", "F", "R'", "F", "R", "F2", "L'"],
            "UURUURFFU": ["F", "R'", "F'", "R", "U", "R", "U'", "R'"],
            "LUBUURFFU": ["R'", "U'", "R", "Y'", "X'", "R", "U'", "R'", "F", "R", "U", "R'", "X"],
            "BUBUURUFU": ["U'", "R", "U2", "R'", "U'", "R", "U'", "R2", "Y'", "R'", "U'", "R", "U", "B"],
            "LUBUURLFF": ["F", "R", "U", "R'", "U'", "R", "U", "R'", "U'", "F'"],
            "BUBUURFFF": ["L", "F'", "L'", "F", "U2", "L2", "Y'", "L", "F", "L'", "F"],
            "BUBLUUUFU": ["U'", "R'", "U2", "R", "U", "R'", "U", "R2", "Y", "R", "U", "R'", "U'", "F'"],
            "LUULUUFFR": ["X", "L", "U2", "R'", "U'", "R", "U'", "X'", "L'"],
            "BUULUUUFR": ["R'", "U2", "X'", "R", "R", "U'", "R'", "U", "X", "R'", "U2", "R"],
            "BURLUUFFR": ["F'", "L'", "U'", "L", "U", "L'", "U'", "L", "U", "F"],
            "LUBLUULFF": ["R'", "F", "R'", "F'", "R2", "U2", "X'", "U'", "R", "U", "R'", "X"],
            "BUBLUUFFF": ["R'", "F", "R", "F'", "U2", "R2", "Y", "R'", "F'", "R", "F'"],
            "BBUUURLUF": ["R", "U", "R'", "Y", "R'", "F", "R", "U'", "R'", "F'", "R"],
            "UBBUURFUR": ["L'", "B'", "L", "U'", "R'", "U", "R", "L'", "B", "L"],
            "LBBUURFUU": ["U2", "X", "L", "R2", "U'", "R", "U'", "R'", "U2", "R", "U'", "M"],
            "UBUUURLUR": ["X'", "U'", "R", "U'", "R2", "F", "X", "R", "U", "R'", "U'", "R", "B2"],
            "LBBLUULUF": ["L", "U'", "Y'", "R'", "U2", "R'", "U", "R", "U'", "R", "U2", "R", "Y", "U'", "L'"],
            "BBRLUUUUF": ["U2", "X", "R'", "L2", "U", "L'", "U", "L", "U2", "L'", "U", "M"],
            "UBULUULUR": ["Y2", "F", "U", "R", "U'", "X'", "U", "R'", "D'", "R", "U'", "R'", "X"],
            "BBRLUULUU": ["X'", "L'", "U2", "R", "U", "R'", "U", "X", "L"],
            "UURLURUUR": ["R", "U", "X'", "R", "U'", "R'", "U", "X", "U'", "R'"],
            "LBRUUUUFU": ["R", "U", "R'", "U'", "X", "D'", "R'", "U", "R", "E'", "Z'"],
            "LBBUUUFFU": ["R'", "F", "R", "U", "R'", "F'", "R", "Y", "L", "U'", "L'"],
            "BBRUUUUFF": ["L", "F'", "L'", "U'", "L", "F", "L'", "Y'", "R'", "U", "R"],
            "BBRUUULFU": ["L'", "B'", "L", "R'", "U'", "R", "U", "L'", "B", "L"],
            "LBBUUUUFR": ["R", "B", "R'", "L", "U", "L'", "U'", "R", "B'", "R'"],
            "UURUURUFR": ["F", "U", "R", "U'", "R'", "F'"],
            "BUULUUFFU": ["R'", "Y", "U'", "L", "Y'", "U", "R", "U'", "R'", "F'", "R"],
            "UUBUURUFF": ["L", "Y'", "U", "R'", "Y", "U'", "L'", "U", "L", "F", "L'"],
            "LUULUULFU": ["F'", "U'", "L'", "U", "L", "F"],
            "LBUUUULFU": ["F", "R", "U", "R'", "U'", "F'"],
            "BBUUUUFFU": ["R", "U", "R'", "U'", "R'", "F", "R", "F'"],
            "LBULUUUUF": ["L", "U", "L'", "U", "L", "U'", "L'", "U'", "Y2", "R'", "F", "R", "F'"],
            "UBRUURFUU": ["R'", "U'", "R", "U'", "R'", "U", "R", "U", "Y", "F", "R'", "F'", "R"],
            "UBBUUULFU": ["R'", "F", "R", "U", "R'", "U'", "Y", "L'", "Y'", "U", "R"],
            "BBUUUUUFR": ["L", "F'", "L'", "U'", "L", "U", "Y'", "R", "Y", "U'", "L'"]
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
            'UFLURULBUBUULUBRUFURF': ['R2', 'Y', 'D', "R'", 'U', "R'", "U'", 'R', "Y'", "D'", 'R2', "Y'", "R'", 'U',
                                      'R'],
            'UBRUBUFLULUUFURFURULB': ['R', 'U', "R'", "Y'", 'R2', "Y'", "D'", 'R', "U'", "R'", 'U', "R'", 'Y', 'D',
                                      'R2'],
            'UBRUBULBUFUURUFLULURF': ['L', 'U2', "L'", 'U2', 'L', "F'", "L'", "U'", 'L', 'U', 'L', 'F', 'L2', 'U'],
            'UBRUBUFLUFUURURFULULB': ['R2', 'Y', 'D', "R'", 'U', "R'", "U'", 'R', "Y'", "D'", 'R2', "Y'", "R'", 'U',
                                      'R'],
            'URFURULBUFUUBUFLULUBR': ["R'", 'U2', "R'", 'Y', "U'", "R'", "F'", 'R2', "U'", "R'", 'U', "R'", 'F', 'R',
                                      "U'", 'F'],
            'ULBUBURFULUURUBRUFUFL': ["X'", 'R', "U'", 'R', 'D2', "R'", 'U', 'R', 'D2', 'R2', 'X'],
            'UBRULUFLUBUURURFUFULB': ['R2', "Y'", "D'", 'R', "U'", 'R', 'U', "R'", 'Y', 'D', 'R2', 'Y', 'R', "U'",
                                      "R'"],
            'UBRUFUFLULUURURFUBULB': ['R', 'U', "R'", "U'", "R'", 'F', 'R2', "U'", "R'", "U'", 'R', 'U', "R'", "F'"],
            'URFUFUBRULUUBULBURUFL': ['R2', 'Y', 'D', "R'", 'U', "R'", "U'", 'R', "Y'", "D'", 'R2', "Y'", "R'", 'U',
                                      'R'],
            'UFLULULBURUUBUBRUFURF': ['R', 'U', "R'", "F'", 'R', 'U', "R'", "U'", "R'", 'F', 'R2', "U'", "R'", "U'"],
            'ULBURURFUBUULUBRUFUFL': ['L', 'U2', "L'", 'U2', 'L', "F'", "L'", "U'", 'L', 'U', 'L', 'F', 'L2', 'U'],
            'UBRULURFUBUURULBUFUFL': ['R2', 'U', 'R', 'U', "R'", "U'", "R'", "U'", "R'", 'U', "R'"],
            'URFURUBRULUUBUFLUFULB': ["R'", 'U', "R'", 'Y', "U'", "R'", "F'", 'R2', "U'", "R'", 'U', "R'", 'F', 'R',
                                      'F'],
            'URFUFUBRUBUURULBULUFL': ['R', 'U', "R'", "F'", 'R', 'U', "R'", "U'", "R'", 'F', 'R2', "U'", "R'", "U'"],
            'UBRURUFLULUUBURFUFULB': ["R'", "U'", 'R', 'Y', 'R2', 'Y', 'D', "R'", 'U', 'R', "U'", 'R', "Y'", "D'",
                                      'R2'],
            'ULBUFURFUBUURUBRULUFL': ["R'", 'U2', 'R', 'U2', "R'", 'F', 'R', 'U', "R'", "U'", "R'", "F'", 'R2', "U'"],
            'ULBULUBRUBUUFUFLURURF': ['M2', 'U', 'M2', 'U', "M'", 'U2', 'M2', 'U2', "M'", 'U2'],
            'ULBUFURFURUUBUFLULUBR': ['R2', "Y'", "D'", 'R', "U'", 'R', 'U', "R'", 'Y', 'D', 'R2', 'Y', 'R', "U'",
                                      "R'"],
            'ULBUBURFURUULUFLUFUBR': ['R', 'U', "R'", "U'", "R'", 'F', 'R2', "U'", "R'", "U'", 'R', 'U', "R'", "F'"],
            'UFLUBURFULUURULBUFUBR': ["X'", 'R', "U'", "R'", 'D', 'R', 'U', "R'", "D'", 'R', 'U', "R'", 'D', 'R', "U'",
                                      "R'", "D'", 'X'],
            'ULBURURFULUUFUBRUBUFL': ["R'", 'U', "L'", 'U2', 'R', "U'", "R'", 'U2', 'R', 'L', "U'"],
            'URFUBUBRURUULUFLUFULB': ["R'", 'U', "L'", 'U2', 'R', "U'", 'L', "R'", 'U', "L'", 'U2', 'R', "U'", 'L',
                                      "U'"],
            'ULBUBUBRUFUULUFLURURF': ['R2', 'U', 'R', 'U', "R'", "U'", "R'", "U'", "R'", 'U', "R'"],
            'UFLUFULBUBUURUBRULURF': ['R', 'U', "R'", "Y'", 'R2', "Y'", "D'", 'R', "U'", "R'", 'U', "R'", 'Y', 'D',
                                      'R2'],
            'ULBULURFURUUFUFLUBUBR': ['R2', 'Y', 'D', "R'", 'U', "R'", "U'", 'R', "Y'", "D'", 'R2', "Y'", "R'", 'U',
                                      'R'],
            'UFLULURFUFUURULBUBUBR': ["R'", 'U', "R'", 'Y', "U'", "R'", "F'", 'R2', "U'", "R'", 'U', "R'", 'F', 'R',
                                      'F'],
            'UFLULUBRURUUBURFUFULB': ["R'", 'U2', 'R', 'U2', "R'", 'F', 'R', 'U', "R'", "U'", "R'", "F'", 'R2', "U'"],
            'URFUFUFLURUUBULBULUBR': ["R'", 'U', "L'", 'U2', 'R', "U'", "R'", 'U2', 'R', 'L', "U'"],
            'URFUBULBULUURUFLUFUBR': ['X', "R'", 'U', "R'", 'D2', 'R', "U'", "R'", 'D2', 'R2', "X'"],
            'ULBUFUFLURUUBUBRULURF': ['F', 'R', "U'", "R'", "U'", 'R', 'U', "R'", "F'", 'R', 'U', "R'", "U'", "R'", 'F',
                                      'R', "F'"],
            'ULBUBUBRURUULURFUFUFL': ["R'", 'U2', "R'", 'Y', "U'", "R'", "F'", 'R2', "U'", "R'", 'U', "R'", 'F', 'R',
                                      "U'", 'F'],
            'UBRUFUFLURUULULBUBURF': ['X', "R'", 'U', "R'", 'D2', 'R', "U'", "R'", 'D2', 'R2', "X'"],
            'URFURUFLUBUUFULBULUBR': ["X'", 'R', "U'", 'R', 'D2', "R'", 'U', 'R', 'D2', 'R2', 'X'],

            'UBRURUFLUFUULURFUBULB': ['R', 'U', "R'", "F'", 'R', 'U', "R'", "U'", "R'", 'F', 'R2', "U'", "R'", "U'"],

            'ULBUBUFLURUULUBRUFURF': ['L', "U'", 'R', 'U2', "L'", 'U', "R'", 'L', "U'", 'R', 'U2', "L'", 'U', "R'",
                                      'U'],
            'UFLUFUBRURUULURFUBULB': ["X'", 'R', "U'", 'R', 'D2', "R'", 'U', 'R', 'D2', 'R2', 'X'],
            'URFUBUFLULUURUBRUFULB': ['M2', 'U', 'M2', 'U2', 'M2', 'U', 'M2'],
            'UFLUFURFULUURUBRUBULB': ["R'", 'U2', "R'", 'Y', "U'", "R'", "F'", 'R2', "U'", "R'", 'U', "R'", 'F', 'R',
                                      "U'", 'F'],
            'UFLULURFUFUUBUBRURULB': ['X', "R'", 'U', "R'", 'D2', 'R', "U'", "R'", 'D2', 'R2', "X'"],
            'UBRUFURFUBUULULBURUFL': ['R', "U'", 'R', 'U', 'R', 'U', 'R', "U'", "R'", "U'", 'R2'],

            'UFLURULBULUUFUBRUBURF': ['R2', "Y'", "D'", 'R', "U'", 'R', 'U', "R'", 'Y', 'D', 'R2', 'Y', 'R', "U'",
                                      "R'"],
            'UFLUBUBRUFUULURFURULB': ["R'", 'U', "L'", 'U2', 'R', "U'", "R'", 'U2', 'R', 'L', "U'"],
            'URFULUFLUFUURUBRUBULB': ['R', "U'", 'R', 'U', 'R', 'U', 'R', "U'", "R'", "U'", 'R2'],
            'UBRUBULBURUUFURFULUFL': ["R'", 'U', "R'", 'Y', "U'", "R'", "F'", 'R2', "U'", "R'", 'U', "R'", 'F', 'R',
                                      'F'],
            'URFULUBRUBUUFULBURUFL': ['R', 'U', "R'", "U'", "R'", 'F', 'R2', "U'", "R'", "U'", 'R', 'U', "R'", "F'"],
            'ULBULUFLUFUUBUBRURURF': ["X'", 'R', "U'", "R'", 'D', 'R', 'U', "R'", "D'", 'R', 'U', "R'", 'D', 'R', "U'",
                                      "R'", "D'", 'X'],
            'URFURUFLUFUULULBUBUBR': ["R'", 'U2', 'R', 'U2', "R'", 'F', 'R', 'U', "R'", "U'", "R'", "F'", 'R2', "U'"],
            'URFULUBRUFUURULBUBUFL': ["R'", "U'", 'R', 'Y', 'R2', 'Y', 'D', "R'", 'U', 'R', "U'", 'R', "Y'", "D'",
                                      'R2'],
            'URFULUFLURUUFULBUBUBR': ['L', 'U2', "L'", 'U2', 'L', "F'", "L'", "U'", 'L', 'U', 'L', 'F', 'L2', 'U'],
            'UBRULULBUBUURUFLUFURF': ["R'", 'U', "L'", 'U2', 'R', "U'", "R'", 'U2', 'R', 'L', "U'"],
            'UFLURURFUFUUBULBULUBR': ["R'", 'U', "L'", 'U2', 'R', "U'", 'L', "R'", 'U', "L'", 'U2', 'R', "U'", 'L',
                                      "U'"],
            'ULBUFUFLULUURUBRUBURF': ["R'", 'U', "L'", 'U2', 'R', "U'", 'L', "R'", 'U', "L'", 'U2', 'R', "U'", 'L',
                                      "U'"],
            'URFURUFLUFUUBUBRULULB': ['M2', 'U', 'M2', 'U', "M'", 'U2', 'M2', 'U2', "M'", 'U2'],
            'UFLURULBUBUUFURFULUBR': ['M2', 'U', 'M2', 'U2', 'M2', 'U', 'M2'],
            'URFULUBRUBUURUFLUFULB': ['F', 'R', "U'", "R'", "U'", 'R', 'U', "R'", "F'", 'R', 'U', "R'", "U'", "R'", 'F',
                                      'R', "F'"],
            'UBRURULBULUUFURFUBUFL': ['F', 'R', "U'", "R'", "U'", 'R', 'U', "R'", "F'", 'R', 'U', "R'", "U'", "R'", 'F',
                                      'R', "F'"],
            'UFLUFUBRULUUBURFURULB': ['L', 'U2', "L'", 'U2', 'L', "F'", "L'", "U'", 'L', 'U', 'L', 'F', 'L2', 'U'],

            'UFLURULBUFUUBUBRULURF': ['R', 'U', "R'", "U'", "R'", 'F', 'R2', "U'", "R'", "U'", 'R', 'U', "R'", "F'"],
            'UBRUBULBULUUFUFLURURF': ["R'", 'U2', 'R', 'U2', "R'", 'F', 'R', 'U', "R'", "U'", "R'", "F'", 'R2', "U'"],
            'UBRULULBUFUUBUFLURURF': ["X'", 'R', "U'", 'R', 'D2', "R'", 'U', 'R', 'D2', 'R2', 'X'],
            'ULBURUBRUBUUFURFULUFL': ['X', "R'", 'U', "R'", 'D2', 'R', "U'", "R'", 'D2', 'R2', "X'"],
            'UFLUBULBURUULURFUFUBR': ['M2', 'U', 'M2', 'U', "M'", 'U2', 'M2', 'U2', "M'", 'U2'],
            'UFLUBURFUFUULULBURUBR': ['F', 'R', "U'", "R'", "U'", 'R', 'U', "R'", "F'", 'R', 'U', "R'", "U'", "R'", 'F',
                                      'R', "F'"],
            'ULBUBUBRURUUFUFLULURF': ['R', "U'", 'R', 'U', 'R', 'U', 'R', "U'", "R'", "U'", 'R2'],

            'URFUBUBRUFUULULBURUFL': ['R2', "Y'", "D'", 'R', "U'", 'R', 'U', "R'", 'Y', 'D', 'R2', 'Y', 'R', "U'",
                                      "R'"],
            'ULBUFURFUBUULUFLURUBR': ["R'", "U'", 'R', 'Y', 'R2', 'Y', 'D', "R'", 'U', 'R', "U'", 'R', "Y'", "D'",
                                      'R2'],
            'UFLUBULBURUUFUBRULURF': ["R'", "U'", 'R', 'Y', 'R2', 'Y', 'D', "R'", 'U', 'R', "U'", 'R', "Y'", "D'",
                                      'R2'],
            'URFUFUBRULUURUFLUBULB': ['L', "U'", 'R', 'U2', "L'", 'U', "R'", 'L', "U'", 'R', 'U2', "L'", 'U', "R'",
                                      'U'],
            'URFULUBRURUUBULBUFUFL': ['R', 'U', "R'", "Y'", 'R2', "Y'", "D'", 'R', "U'", "R'", 'U', "R'", 'Y', 'D',
                                      'R2'],
            'UFLURULBULUUBURFUFUBR': ['R', "U'", 'R', 'U', 'R', 'U', 'R', "U'", "R'", "U'", 'R2'],
            'URFURUBRUBUUFUFLULULB': ["X'", 'R', "U'", "R'", 'D', 'R', 'U', "R'", "D'", 'R', 'U', "R'", 'D', 'R', "U'",
                                      "R'", "D'", 'X'],
            'ULBUBURFULUUFUFLURUBR': ['R', 'U', "R'", "F'", 'R', 'U', "R'", "U'", "R'", 'F', 'R2', "U'", "R'", "U'"],
            'UBRULUFLUBUUFULBURURF': ["R'", 'U2', "R'", 'Y', "U'", "R'", "F'", 'R2', "U'", "R'", 'U', "R'", 'F', 'R',
                                      "U'", 'F'],
            'ULBURURFUFUULUFLUBUBR': ['R', 'U', "R'", "Y'", 'R2', "Y'", "D'", 'R', "U'", "R'", 'U', "R'", 'Y', 'D',
                                      'R2'],
            'UBRULURFUFUUBULBURUFL': ['M2', 'U', 'M2', 'U2', 'M2', 'U', 'M2'],
            'UFLULURFUBUUFULBURUBR': ['L', "U'", 'R', 'U2', "L'", 'U', "R'", 'L', "U'", 'R', 'U2', "L'", 'U', "R'",
                                      'U'],
            'URFURUFLULUUFUBRUBULB': ['R2', 'U', 'R', 'U', "R'", "U'", "R'", "U'", "R'", 'U', "R'"],
            'ULBUFUFLUBUULUBRURURF': ["R'", 'U', "R'", 'Y', "U'", "R'", "F'", 'R2', "U'", "R'", 'U', "R'", 'F', 'R',
                                      'F'],
            'UFLUFULBURUUBURFULUBR': ['R2', 'U', 'R', 'U', "R'", "U'", "R'", "U'", "R'", 'U', "R'"],

            'UBRUFULBURUULURFUBUFL': ["X'", 'R', "U'", "R'", 'D', 'R', 'U', "R'", "D'", 'R', 'U', "R'", 'D', 'R', "U'",
                                      "R'", "D'", 'X'],
            'UBRURULBUFUUBURFULUFL': ['L', "U'", 'R', 'U2', "L'", 'U', "R'", 'L', "U'", 'R', 'U2', "L'", 'U', "R'",
                                      'U'],
            'ULBUFUBRURUULUFLUBURF': ['M2', 'U', 'M2', 'U2', 'M2', 'U', 'M2'],
            'UBRUFURFULUURULBUBUFL': ['M2', 'U', 'M2', 'U', "M'", 'U2', 'M2', 'U2', "M'", 'U2'],
            'UBRULULBUBUUFURFURUFL': ["R'", 'U', "L'", 'U2', 'R', "U'", 'L', "R'", 'U', "L'", 'U2', 'R', "U'", 'L',
                                      "U'"],
            'UBRURURFUBUUFULBULUFL': []

        }
        for _ in range(4):
            orientation = ''.join([
                self.cube.search_piece('ULB'),
                self.cube.search_piece('UB'),
                self.cube.search_piece('UBR'),

                self.cube.search_piece('UL'),
                self.cube.search_piece('U'),
                self.cube.search_piece('UR'),

                self.cube.search_piece('UFL'),
                self.cube.search_piece('UF'),
                self.cube.search_piece('URF'),

            ])

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
