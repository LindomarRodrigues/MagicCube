from cube import Cube, FACES_CODES, EDGES_CODES_INV


class LayerByLayerSolver:
    def __init__(self, cube: Cube):
        self.cube = cube
        self.moves = []

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

    def cross(self):
        for edge in ['UR', 'UF', 'UL', 'UB']:
            if 'D' not in EDGES_CODES_INV[self.cube.cube['edges'][edge]]:
                continue
            if self.cube.get_face_piece_color('U', edge) == 'W':

                if edge[1] == 'R':
                    r_color = self.cube.get_face_piece_color('R', edge)

                    if r_color == 'R':
                        self.cube.move('R', 'cw', 2)
                        self.moves.append('R2')
                        return self.cross()
                    elif r_color == 'B':
                        self.cube.move('U', 'cw', 1)
                        self.moves.append('U')
                        self.cube.move('F', 'cw', 2)
                        self.moves.append('F2')
                        return self.cross()
                    elif r_color == 'O':
                        self.cube.move('U', 'cw', 2)
                        self.moves.append('U2')
                        self.cube.move('L', 'cw', 2)
                        self.moves.append('L2')
                        return self.cross()
                    elif r_color == 'G':
                        self.cube.move('U', 'ccw', 1)
                        self.moves.append('U\'')
                        self.cube.move('B', 'cw', 2)
                        self.moves.append('B2')
                        return self.cross()

                elif edge[1] == 'F':
                    self.cube.move('U', 'ccw', 1)
                    self.moves.append('U\'')
                    return self.cross()
                elif edge[1] == 'L':
                    self.cube.move('U', 'cw', 2)
                    self.moves.append('U2')
                    return self.cross()
                elif edge[1] == 'B':
                    self.cube.move('U', 'cw', 1)
                    self.moves.append('U')
                    return self.cross()
            elif self.cube.get_face_piece_color(edge[1], edge) == 'W':
                if edge[1] == 'R':
                    self.cube.move('U', 'cw', 1)
                    self.moves.append("U")
                elif edge[1] == 'L':
                    self.cube.move('U', 'ccw', 1)
                    self.moves.append("U'")
                elif edge[1] == 'B':
                    self.cube.move('U', 'cw', 2)
                    self.moves.append("U2")

                self.cube.moves("F R U R' U' F'")
                self.moves += "F R U R' U' F'".split(' ')
                return self.cross()

        for edge in ['FR', 'FL', 'BL', 'BR']:
            if 'D' not in EDGES_CODES_INV[self.cube.cube['edges'][edge]]:
                continue

            moves = [edge[1] if (self.cube.get_face_piece_color(edge[0], edge) == 'W') else edge[0],
                     'U']
            moves.append(moves[0])

            if (edge == 'FR' and moves[0] == 'R') or (edge == 'FL' and moves[0] == 'F') or (
                    edge == 'BL' and moves[0] == 'L') or (edge == 'BR' and moves[0] == 'B'):
                moves[2] += '\''
            else:
                moves[0] += '\''

            self.cube.moves(' '.join(moves))
            self.moves += moves
            return self.cross()

        for edge in ['DR', 'DF', 'DL', 'DB']:
            if ('D' not in EDGES_CODES_INV[self.cube.cube['edges'][edge]] or
                    self.cube.get_face_piece_color('D', edge) == 'W'):
                continue

            moves = [edge[1]]
            self.cube.moves(' '.join(moves))
            self.moves += moves

            return self.cross()

    def first_layer(self):

        for _ in range(4):
            moves = []
            dfr = self.cube.get_relative_piece_position('DFR')

            if self.cube.get_piece('DFR') == dfr and self.cube.get_relative_piece_color('D', 'DFR') == 'W':
                moves += ["Y"]
                self.cube.moves("Y")
                self.moves += moves
                continue
            elif self.cube.get_piece('DFR') == dfr:
                moves += "R U R' U'".split(' ')
                self.cube.moves("R U R' U'")
            elif self.cube.get_piece('UFL') == dfr:
                moves += ["U'"]
                self.cube.moves("U'")
            if self.cube.get_piece('ULB') == dfr:
                moves += ["U2"]
                self.cube.moves("U2")
            elif self.cube.get_piece('UBR') == dfr:
                moves += ["U"]
                self.cube.moves("U")
            elif self.cube.get_piece('DLF') == dfr:
                moves += ["L'", "U'", "L"]
                self.cube.moves("L' U' L")
            elif self.cube.get_piece('DBL') == dfr:
                moves += ["L", "U2", "L'"]
                self.cube.moves("L U2 L'")
            elif self.cube.get_piece('DRB') == dfr:
                moves += ["R'", "U2", "R", "U'"]
                self.cube.moves("R' U2 R U'")
            elif self.cube.get_piece('URF') == dfr:
                pass

            if self.cube.get_relative_piece_color('R', 'URF') == 'W':
                moves += ["R", "U", "R'"]
                self.cube.moves("R U R'")
            elif self.cube.get_relative_piece_color('F', 'URF') == 'W':

                moves += ["F'", "U'", "F"]
                self.cube.moves("F' U' F")
            elif self.cube.get_relative_piece_color('U', 'URF') == 'W':
                moves += ["R", "U2", "R'", "U'", "R", "U", "R'"]
                self.cube.moves("R U2 R' U' R U R'")
            # self.cube.plotar_cubo()
            moves += ["Y"]
            self.cube.moves("Y")
            self.moves += moves

    def second_layer(self):
        for _ in range(4):
            moves = []
            fr_piece = self.cube.search_piece('FR')
            if fr_piece == 'FR' and self.cube.get_relative_piece_color('F', 'FR') != self.cube.get_face_piece_color('F',
                                                                                                                    'F'):
                moves += "U R U' R' U' F' U F".split(' ')
                self.cube.moves("U R U' R' U' F' U F")
            elif fr_piece == 'FL':
                moves += "U' L' U L U F U' F'".split(' ')
                self.cube.moves("U' L' U L U F U' F'")
            elif fr_piece == 'BL':
                moves += "U L U' L' U' B' U B".split(' ')
                self.cube.moves("U L U' L' U' B' U B")
            elif fr_piece == 'BR':
                moves += "U' R' U R U B U' B'".split(' ')
                self.cube.moves("U' R' U R U B U' B'")
            fr_piece = self.cube.search_piece('FR')
            if fr_piece != 'FR':
                if fr_piece == 'UL':
                    moves += ["U'"]
                    self.cube.moves("U'")
                elif fr_piece == 'UB':
                    moves += ["U2"]
                    self.cube.moves("U2")
                elif fr_piece == 'UR':
                    moves += ["U"]
                    self.cube.moves("U")

                if self.cube.get_face_piece_color('U', 'UF') == self.cube.get_face_piece_color('F', 'F'):
                    moves += "U2 F' U F U R U' R'".split(' ')
                    self.cube.moves("U2 F' U F U R U' R'")
                elif self.cube.get_face_piece_color('U', 'UF') == self.cube.get_face_piece_color('R', 'R'):
                    moves += "U R U' R' U' F' U F".split(' ')
                    self.cube.moves("U R U' R' U' F' U F")

            moves += ["Y"]
            self.cube.moves("Y")
            self.moves += moves

    def yellow_cross(self):
        yellow_cross_corrects = 0
        yellow_cross = []
        for edge in ['UF', 'UR', 'UB', 'UL']:
            if self.cube.get_face_piece_color('U', edge) == 'Y':
                yellow_cross_corrects += 1
                yellow_cross.append(edge)

        if yellow_cross_corrects == 0:
            self.cube.moves("F R U R' U' F'")
            self.moves += "F R U R' U' F'".split(' ')
            return self.yellow_cross()
        elif yellow_cross_corrects == 2:
            if yellow_cross == ['UF', 'UB']:
                self.cube.moves("U")
                self.moves += "U".split(' ')
                return self.yellow_cross()
            elif yellow_cross == ['UR', 'UL']:
                self.cube.moves("F R U R' U' F'")
                self.moves += "F R U R' U' F'".split(' ')
            elif yellow_cross == ['UF', 'UR']:
                self.cube.moves("U2")
                self.moves += "U2".split(' ')
                return self.yellow_cross()
            elif yellow_cross == ['UF', 'UL']:
                self.cube.moves("U")
                self.moves += "U".split(' ')
                return self.yellow_cross()
            elif yellow_cross == ['UR', 'UB']:
                self.cube.moves("U'")
                self.moves += "U'".split(' ')
                return self.yellow_cross()
            elif yellow_cross == ['UB', 'UL']:
                self.cube.moves("F R U R' U' F'")
                self.moves += "F R U R' U' F'".split(' ')
                return self.yellow_cross()

    def yellow_face(self):
        yellow_face_corrects = 0
        yellow_face = []
        for corner in ['URF', 'UBR', 'ULB', 'UFL']:
            if self.cube.get_face_piece_color('U', corner) == 'Y':
                yellow_face_corrects += 1
                yellow_face.append(corner)

        if yellow_face_corrects == 0:
            while self.cube.get_face_piece_color('F', 'URF') != 'Y':
                self.cube.moves("U")
                self.moves += "U".split(' ')

            if self.cube.get_face_piece_color('B', 'ULB') == 'Y':
                self.cube.moves("U")
                self.moves += "U".split(' ')

        elif yellow_face_corrects == 1:
            while self.cube.get_face_piece_color('U', 'UFL') != 'Y':
                self.cube.moves("U")
                self.moves += "U".split(' ')

        elif yellow_face_corrects == 2:
            if yellow_face == ['URF', 'ULB'] or yellow_face == ['UBR', 'UFL']:
                while self.cube.get_face_piece_color('F', 'UFL') != 'Y':
                    self.cube.moves("U")
                    self.moves += "U".split(' ')
            else:
                while (self.cube.get_face_piece_color('U', 'UBR') != 'Y'
                       or self.cube.get_face_piece_color('F', 'UFL') != 'Y'):
                    self.cube.moves("U")
                    self.moves += "U".split(' ')
        if yellow_face_corrects != 4:
            self.cube.moves("R U R' U R U2 R'")
            self.moves += "R U R' U R U2 R'".split(' ')
            return self.yellow_face()

    def yellow_corners(self):
        for _ in range(4):
            if self.cube.get_face_piece_color('F', 'URF') == self.cube.get_face_piece_color('F', 'UFL'):
                break
            else:
                self.cube.moves("U")
                self.moves += "U".split(' ')

        corners_pair_corrects = 0
        for _ in range(4):
            if self.cube.get_face_piece_color('F', 'URF') == self.cube.get_face_piece_color('F', 'UFL'):
                corners_pair_corrects += 1
            self.cube.moves("U")
            self.moves += "U".split(' ')

        if corners_pair_corrects == 4:
            while self.cube.get_face_piece_color('F', 'URF') != self.cube.get_face_piece_color('F', 'F'):
                self.cube.moves("U")
                self.moves += "U".split(' ')
        else:
            self.cube.moves("R B' R F2 R' B R F2 R2")
            self.moves += "R B' R F2 R' B R F2 R2".split(' ')
            return self.yellow_corners()

    def last_layer_orientation(self):
        # self.blue_to_front()

        if self.cube.is_solved():
            return

        for _ in range(4):
            if self.cube.get_face_piece_color('B', 'UB') == self.cube.get_face_piece_color('B', 'UBR'):
                if self.cube.get_face_piece_color('R', 'UR') == self.cube.get_face_piece_color('F', 'F'):
                    self.cube.moves("F2 U L R' F2 L' R U F2")
                    self.moves += "F2 U L R' F2 L' R U F2".split(' ')
                else:
                    self.cube.moves("F2 U' L R' F2 L' R U' F2")
                    self.moves += "F2 U' L R' F2 L' R U' F2".split(' ')

                self.blue_to_front()
                return
            else:
                self.cube.moves("Y")
                self.moves += "Y".split(' ')

        self.cube.moves("F2 U' L R' F2 L' R U' F2")
        self.moves += "F2 U' L R' F2 L' R U' F2".split(' ')

        return self.last_layer_orientation()

    def solve(self):
        # 0. Orient white to bottom
        self.white_to_bottom()

        # 0. Orient blue to front
        self.blue_to_front()

        # 1. White cross
        self.cross()

        # 2. First layer
        self.first_layer()

        # 3. Second layer
        self.second_layer()

        # 4. Yellow cross
        self.yellow_cross()

        # 5. Yellow face
        self.yellow_face()

        # 6. Yellow corners
        self.yellow_corners()

        # 7. Last layer orientation
        self.last_layer_orientation()

        # self.cube.plotar_cubo()
        #
        # print(self.moves)
        # self.cube.move('X', 'cw', 2)
        # self.cube.plotar_cubo()
        # self.cube.move('Y', 'cw', 1)
        # self.cube.plotar_cubo()
        # self.cube.move('Y', 'cw', 1)
        # self.cube.plotar_cubo()
        # self.cube.move('Y', 'cw', 1)
        # self.cube.plotar_cubo()
