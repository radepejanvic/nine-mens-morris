from hashmap import LinearHashMap


class Board(object):
    def __init__(self, move=None):
        self.board = [["*", None, None, "*", None, None, "*"],
                       [None, "*", None, "*", None, "*", None],
                       [None, None, "*", "*", "*", None, None],
                       ["*", "*", "*", None, "*", "*", "*"],
                       [None, None, "*", "*", "*", None, None],
                       [None, "*", None, "*", None, "*", None],
                       ["*", None, None, "*", None, None, "*"]]

        self.black_pawns = {}  # LinearHashMap()
        self.white_pawns = {}  # LinearHashMap()
        self.empty_fields = self.getEmptyFields()
        ('[(0, 0), (0, 3), (0, 6), (1, 1), (1, 3), (1, 5),\n'
         '                        (2, 2), (2, 3), (2, 4), (3, 0), (3, 1), (3, 2),\n'
         '                        (3, 4), (3, 5), (3, 6), (4, 2), (4, 3), (4, 4),\n'
         '                        (5, 1), (5, 3), (5, 5), (6, 0), (6, 3), (6, 6)]')
        self.whites = 9
        self.blacks = 9
        self.placed_whites = 0
        self.placed_blacks = 0

        self.last_move = move
        
        self.doubles = []
        self.horizontal = []
        self.vertical = []

    def get_value(self, i, j):
        return self.board[i][j]

    def set_value(self, i, j, value):
        self.board[i][j] = value
        if value == "W":
            self.white_pawns[(i, j)] = value
            self.whites -= 1
            self.placed_whites += 1
            self.last_move = (i, j)
        else:
            self.black_pawns[(i, j)] = value
            self.blacks -= 1
            self.placed_blacks += 1
            self.last_move = (i, j)
        self.empty_fields.remove((i, j))

    def is_empty(self, i, j):
        if self.board[i][j] != "*":
            return False
        return True

    def is_piece_there(self, i, j, value):
        if self.board[i][j] == "*" or self.board[i][j] != value:
            return False
        else:
            return True

    def get_moves_phase_2(self, value):
        moves = []
        if value == "W":
            pawns = self.white_pawns
        else:
            pawns = self.black_pawns
        for xy in pawns:
            for move in adjacent_fields[xy]:
                if self.board[move[0]][move[1]] == "*" and move not in moves:
                    moves.append(move)
        return moves

    # ova funkcija sluzi za izbacivanje protivnicke figurice kao i za pomeranje figurice,
    # tj kad se izabere nova lokacija setuje se nova vrednost tamo a stara se brise pomocu ove
    def remove_piece(self, i, j, value):
        self.board[i][j] = "*"
        if value == "W":
            del self.white_pawns[(i, j)]
            self.placed_whites -= 1
        else:
            del self.black_pawns[(i, j)]
            self.placed_blacks -= 1

        if self.is_morris(i, j, value) == 2:
            self.doubles.remove((i, j))
            self.horizontal.remove(i)
            self.horizontal.remove(j)
        elif self.is_morris(i, j, value) == 1:
            if i in self.horizontal:
                self.horizontal.remove(i)
            elif j in self.vertical:
                self.vertical.remove(j)
        self.empty_fields.append((i, j))

    def is_blocked(self, i, j):
        for xy in adjacent_fields[(i, j)]:
            if self.board[xy[0]][xy[1]] == "*":
                return False
        return True

    def get_free_adj(self, i, j):
        free_frields = []
        for adj in adjacent_fields[(i, j)]:
            if self.is_empty(adj[0], adj[1]):
                free_frields.append(adj)
        return free_frields

    def getNumberOfBlockedPawns(self, value):
        counter = 0
        if value == "W":
            pawns = self.white_pawns
        else:
            pawns = self.black_pawns
        for xy in pawns:
            if self.is_blocked(xy[0], xy[1]):
                counter += 1
        return counter

    # if every player places every pawn, list of each players unplayed pawns gets empty
    """mozda cak nepotrebno"""
    def is_phase_one(self):
        if self.whites <= 0 and self.blacks <= 0:
            return False
        return True

    # poziva se tek u drugoj fazi
    def is_end(self):
        if not self.is_phase_one():
            if self.placed_whites < 3 or self.getNumberOfBlockedPawns("W") == len(self.black_pawns):
                return True, "B", 1
            elif self.placed_blacks < 3 or self.getNumberOfBlockedPawns("B") == len(self.white_pawns):
                return True, "W", -1
            else:
                return False, None, 0
        return False, None, 0

    def win(self):
        win, player, outcome = self.is_end()
        return outcome

    # compares each positions value in a single row, based on the function atribute, same for the vertical morris
    def is_horizontal_morris(self, i, value):
        if i in [0, 6] and self.board[i][0] == self.board[i][3] == self.board[i][6] == value:
            return True
        elif i in [1, 5] and self.board[i][1] == self.board[i][3] == self.board[i][5] == value:
            return True
        elif i in [2, 4] and self.board[i][2] == self.board[i][3] == self.board[i][4] == value:
            return True
        elif i == 3 and self.board[i][0] == self.board[i][1] == self.board[i][2] == value or self.board[i][4] == \
                self.board[i][5] == self.board[i][6] == value:
            return True
        return False

    def is_vertical_morris(self, j, value):
        if j in [0, 6] and self.board[0][j] == self.board[3][j] == self.board[6][j] == value:
            return True
        elif j in [1, 5] and self.board[1][j] == self.board[3][j] == self.board[5][j] == value:
            return True
        elif j in [2, 4] and self.board[2][j] == self.board[3][j] == self.board[4][j] == value:
            return True
        elif j == 3 and self.board[0][j] == self.board[1][j] == self.board[2][j] == value or self.board[4][j] == \
                self.board[5][j] == self.board[6][j] == value:
            return True
        return False

    def is_morris(self, i, j, value):
        """double morris, single morris, no morris"""
        if self.is_horizontal_morris(i, value) and self.is_vertical_morris(j, value):
            return 2
        elif self.is_horizontal_morris(i, value) or self.is_vertical_morris(j, value):
            return 1
        return 0

    def getNumberOfDoubleMorrises(self, value):
        counter = 0
        self.doubles = []
        if value == "W":
            pawns = self.white_pawns
        else:
            pawns = self.black_pawns
        for xy in pawns:
            if self.is_morris(xy[0], xy[1], value) == 2:
                self.doubles.append(xy)
                counter += 1
        return counter, self.doubles
        # returnuj i listu duplih mica

    def getNumberOfMorrises(self, value):
        counter = 0
        self.vertical = []
        self.horizontal = []
        if value == "W":
            pawns = self.white_pawns
        else:
            pawns = self.black_pawns

        for xy in pawns:
            # horizontalne
            if xy[0] == 3 and xy[1] < 3 and -3 not in self.horizontal and self.is_horizontal_morris(xy[0], value):
                self.horizontal.append(-3)
                counter += 1
            elif xy[0] == 3 and xy[1] > 3 and 3 not in self.horizontal and self.is_horizontal_morris(xy[0], value):
                self.horizontal.append(3)
                counter += 1
            elif xy[0] != 3 and xy[0] not in self.horizontal and self.is_horizontal_morris(xy[0], value):
                self.horizontal.append(xy[0])
                counter += 1
            # vertikalne
            if xy[1] == 3 and xy[0] < 3 and -3 not in self.vertical and self.is_vertical_morris(xy[1], value):
                self.vertical.append(-3)
                counter += 1
            elif xy[1] == 3 and xy[0] > 3 and 3 not in self.vertical and self.is_vertical_morris(xy[1], value):
                self.vertical.append(3)
                counter += 1
            elif xy[1] != 3 and xy[1] not in self.vertical and self.is_vertical_morris(xy[1], value):
                self.vertical.append(xy[1])
                counter += 1
        return counter, self.horizontal, self.vertical

    def getNumberOfDoubles(self, value):
        counter = 0
        i_axis = []
        j_axis = []
        i_op = []
        j_op = []
        if value == "W":
            pawns = self.white_pawns
            opponent = self.black_pawns
        else:
            pawns = self.black_pawns
            opponent = self.white_pawns

        for op in opponent:
            if op[0] == 3 and op[1] < 3:
                if -3 not in i_op:
                    i_op.append(-3)
            elif op[0] == 3 and op[1] > 3:
                if 3 not in i_op:
                    i_op.append(3)
            elif op[0] != 3:
                if op[0] not in i_op:
                    i_op.append(op[0])

            if op[1] == 3 and op[0] < 3:
                if -3 not in j_op:
                    j_op.append(-3)
            elif op[1] == 3 and op[0] > 3:
                if 3 not in j_op:
                    j_op.append(3)
            elif op[1] != 3:
                if op[0] not in j_op:
                    j_op.append(op[1])

        for xy in pawns:
            # horizontal
            if xy[0] == 3 and xy[1] < 3 and -3 not in self.horizontal and -3 not in i_op:
                if -3 in i_axis:
                    counter += 1
                else:
                    i_axis.append(-3)
            elif xy[0] == 3 and xy[1] > 3 and 3 not in self.horizontal and 3 not in i_op:
                if 3 in i_axis:
                    counter += 1
                else:
                    i_axis.append(3)
            elif xy[0] != 3 and xy[0] not in self.horizontal and xy[0] not in i_op:
                if xy[0] in i_axis:
                    counter += 1
                else:
                    i_axis.append(xy[0])
            # vertical
            if xy[1] == 3 and xy[0] < 3 and -3 not in self.vertical and -3 not in j_op:
                if -3 in j_axis:
                    counter += 1
                else:
                    j_axis.append(-3)
            elif xy[1] == 3 and xy[0] > 3 and 3 not in self.vertical and 3 not in j_op:
                if 3 in j_axis:
                    counter += 1
                else:
                    j_axis.append(3)
            elif xy[1] != 3 and xy[1] not in self.vertical and xy[1] not in j_op:
                if xy[1] in j_axis:
                    counter += 1
                else:
                    j_axis.append(xy[1])
        return counter, i_axis, j_axis

    def getNumberOfGuaranteedMorris(self, value):
        counter = 0
        for tup in potential_morris:
            if self.board[tup[0][0]][tup[0][1]] == self.board[tup[1][0]][tup[1][1]] == self.board[tup[2][0]][tup[2][1]] == value \
                    and self.board[tup[3][0]][tup[3][1]] == self.board[tup[4][0]][tup[4][1]] == "*":
                counter += 1
        return counter

    def getEmptyFields(self):
        self.empty_fields = []
        for i in range(24):
            if self.is_empty(fields[i][0], fields[i][1]):
                self.empty_fields.append(fields[i])
        return self.empty_fields

    def evaluate(self, i, j):
        if self.get_value(i, j) == "B":
            val = "B"
            num = 18
            num2 = 14
        else:
            val = "W"
            num = -18
            num2 = -14
        if self.is_phase_one():
            result = num * self.is_morris(i, j, val) + \
                26 * (self.getNumberOfMorrises("B")[0] - self.getNumberOfMorrises("W")[0]) + \
                1 * (self.getNumberOfBlockedPawns("B") - self.getNumberOfBlockedPawns("W")) + \
                9 * (self.placed_blacks - self.placed_blacks) + \
                10 * (self.getNumberOfDoubles("B")[0] - self.getNumberOfDoubles("W")[0]) + \
                7 * (self.getNumberOfGuaranteedMorris("B") - self.getNumberOfGuaranteedMorris("W"))
        else:
            result = num2 * self.is_morris(i, j, val) + \
                43 * (self.getNumberOfMorrises("B")[0] - self.getNumberOfMorrises("W")[0]) + \
                10 * (self.getNumberOfBlockedPawns("B") - self.getNumberOfBlockedPawns("W")) + \
                11 * (self.placed_blacks - self.placed_blacks) + \
                8 * (self.getNumberOfDoubles("B")[0] - self.getNumberOfDoubles("W")[0]) + \
                1086 * self.is_end()[2]
        return result

    def __str__(self):
        ret = "\n   "
        for x_osa in range(7):
            ret += str(x_osa) + "    "
        ret += "\n"

        y_osa = 0
        for i in range(len(self.board)):
            if i != 0:
                ret += "\n"
            if i in [0, 6]:
                if i == 6:
                    ret += "   |              |              |\n"
                ret += str(y_osa) + "  "
                ret += self.board[i][0] + 14 * "-" + self.board[i][3] + 14 * "-" + self.board[i][6]
                if i == 0:
                    ret += "\n   |              |              |"
            elif i in [1, 5]:
                if i == 5:
                    ret += "   |    |         |         |    |\n"
                ret += str(y_osa) + "  "
                ret += "|    " + self.board[i][1] + 9 * "-" + self.board[i][3] + 9 * "-" + self.board[i][5] + "    |"
                if i == 1:
                    ret += "\n   |    |         |         |    |"
            elif i in [2, 4]:
                ret += str(y_osa) + "  "
                ret += 2 * "|    " + self.board[i][2] + "----" + self.board[i][3] + "----" + self.board[i][
                    4] + 2 * "    |"
            else:
                ret += "   |    |    |         |    |    |\n"
                ret += str(y_osa) + "  "
                ret += self.board[i][0] + "----" + self.board[i][1] + "----" + self.board[i][2] + 9 * " " + \
                       self.board[i][4] + "----" + self.board[i][5] + "----" + self.board[i][6]
                ret += "\n   |    |    |         |    |    |"
            y_osa += 1
        return ret

# Evaluation function for Phase 1 = 18 * (1) + 26 * (2) + 1 * (3) + 9 * (4) + 10 * (5) + 7 * (6)
#
# Evaluation function for Phase 2 = 14 * (1) + 43 * (2) + 10 * (3) + 11 * (4) + 8 * (7) + 1086 * (8)
potential_morris = \
    (((3, 0), (0, 0), (0, 3), (0, 6), (6, 0)),
      ((3, 0), (6, 0), (6, 3), (0, 0), (6, 6)),
      ((0, 3), (0, 6), (3, 6), (0, 0), (6, 6)),
      ((6, 3), (6, 6), (3, 6), (6, 0), (0, 6)),
      ((3, 1), (1, 1), (1, 3), (1, 5), (5, 1)),
      ((1, 3), (1, 5), (3, 5), (1, 1), (5, 5)),
	  ((3, 1), (5, 1), (5, 3), (1, 1), (5, 5)),
      ((5, 3), (5, 5), (3, 5), (5, 1), (1, 5)),
      ((3, 2), (2, 2), (2, 3), (4, 2), (2, 4)),
      ((2, 3), (2, 4), (3, 4), (2, 2), (4, 4)),
      ((3, 2), (4, 2), (4, 3), (2, 2), (4, 4)),
      ((4, 3), (4, 4), (3, 4), (4, 2), (2, 4)),
      ((0, 0), (0, 3), (1, 3), (2, 3), (0, 6)),
      ((0, 6), (0, 3), (1, 3), (0, 0), (2, 3)),
      ((6, 0), (6, 3), (5, 3), (4, 3), (6, 6)),
      ((6, 6), (6, 3), (5, 3), (4, 3), (6, 0)),
      ((0, 0), (3, 0), (3, 1), (3, 2), (6, 0)),
      ((6, 0), (3, 0), (3, 1), (3, 2), (0, 0)),
      ((0, 6), (3, 5), (3, 6), (3, 4), (6, 6)),
      ((3, 5), (3, 6), (6, 6), (3, 4), (0, 6)),
      ((1, 1), (1, 3), (2, 3), (1, 5), (0, 3)),
      ((1, 1), (1, 3), (0, 3), (2, 3), (1, 5)),
      ((1, 3), (1, 5), (2, 3), (1, 1), (0, 3)),
      ((1, 5), (1, 3), (0, 3), (2, 3), (1, 1)),
      ((6, 3), (5, 3), (5, 1), (5, 5), (4, 3)),
      ((5, 1), (5, 3), (4, 3), (6, 3), (5, 5)),
      ((5, 5), (5, 3), (6, 3), (4, 3), (5, 1)),
      ((5, 5), (5, 3), (4, 3), (5, 1), (6, 3)),
      ((1, 1), (3, 1), (3, 2), (3, 0), (5, 1)),
      ((1, 1), (3, 0), (3, 1), (3, 2), (5, 1)),
      ((5, 1), (3, 1), (3, 2), (3, 0), (1, 1)),
      ((5, 1), (3, 1), (3, 0), (3, 2), (1, 1)),
      ((1, 5), (3, 4), (3, 5), (3, 6), (5, 5)),
      ((1, 5), (3, 5), (3, 6), (3, 4), (5, 5)),
      ((5, 5), (3, 5), (3, 6), (3, 4), (1, 5)),
      ((5, 5), (3, 5), (3, 4), (1, 5), (3, 6)),
      ((2, 2), (2, 3), (1, 3), (0, 3), (2, 4)),
      ((2, 4), (2, 3), (1, 3), (0, 3), (2, 2)),
      ((2, 2), (3, 2), (3, 1), (3, 0), (4, 2)),
      ((4, 2), (3, 2), (3, 1), (2, 2), (3, 0)),
      ((4, 2), (4, 3), (5, 3), (4, 4), (6, 3)),
      ((4, 3), (4, 4), (5, 3), (4, 2), (6, 3)),
      ((4, 4), (3, 4), (3, 5), (2, 4), (3, 6)),
      ((2, 4), (3, 4), (3, 5), (3, 6), (4, 4)))

adjacent_fields = LinearHashMap()
adjacent_fields[(0, 0)] = [(0, 3), (3, 0)]
adjacent_fields[(0, 3)] = [(0, 0), (0, 6), (1, 3)]
adjacent_fields[(0, 6)] = [(0, 3), (3, 6)]
adjacent_fields[(1, 1)] = [(1, 3), (3, 1)]
adjacent_fields[(1, 3)] = [(0, 3), (1, 1), (1, 5), (2, 3)]
adjacent_fields[(1, 5)] = [(1, 3), (3, 5)]
adjacent_fields[(2, 2)] = [(2, 3), (3, 2)]
adjacent_fields[(2, 3)] = [(1, 3), (2, 2), (2, 4)]
adjacent_fields[(2, 4)] = [(2, 3), (3, 4)]
adjacent_fields[(3, 0)] = [(0, 0), (3, 1), (6, 0)]
adjacent_fields[(3, 1)] = [(1, 1), (3, 0), (3, 2), (5, 1)]
adjacent_fields[(3, 2)] = [(2, 2), (3, 1), (4, 2)]
adjacent_fields[(3, 4)] = [(2, 4), (3, 5), (4, 4)]
adjacent_fields[(3, 5)] = [(1, 5), (3, 4), (3, 6), (5, 5)]
adjacent_fields[(3, 6)] = [(0, 6), (3, 5), (6, 6)]
adjacent_fields[(4, 2)] = [(3, 2), (4, 3)]
adjacent_fields[(4, 3)] = [(4, 2), (4, 4), (5, 3)]
adjacent_fields[(4, 4)] = [(3, 4), (4, 3)]
adjacent_fields[(5, 1)] = [(3, 1), (5, 3)]
adjacent_fields[(5, 3)] = [(4, 3), (5, 1), (5, 5), (6, 3)]
adjacent_fields[(5, 5)] = [(3, 5), (5, 3)]
adjacent_fields[(6, 0)] = [(3, 0), (6, 3)]
adjacent_fields[(6, 3)] = [(5, 3), (6, 0), (6, 6)]
adjacent_fields[(6, 6)] = [(3, 6), (6, 3)]

fields = LinearHashMap()
fields[0] = (0, 0)
fields[1] = (0, 3)
fields[2] = (0, 6)
fields[3] = (1, 1)
fields[4] = (1, 3)
fields[5] = (1, 5)
fields[6] = (2, 2)
fields[7] = (2, 3)
fields[8] = (2, 4)
fields[9] = (3, 0)
fields[10] = (3, 1)
fields[11] = (3, 2)
fields[12] = (3, 4)
fields[13] = (3, 5)
fields[14] = (3, 6)
fields[15] = (4, 2)
fields[16] = (4, 3)
fields[17] = (4, 4)
fields[18] = (5, 1)
fields[19] = (5, 3)
fields[20] = (5, 5)
fields[21] = (6, 0)
fields[22] = (6, 3)
fields[23] = (6, 6)

# mills = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (9, 10, 11), (12, 13, 14), (15, 16, 17)
# (18, 19, 20), (21, 22, 23), (0, 9, 21), ()]

# is_move_valid -> set_position
# is_my_pawn -> is_empty -> move_piece

"""Odavde"""
# board = Board()
# board.set_value(0, 0, "W")
# board.set_value(1, 1, "B")
# print(board.evaluate(1, 1))
# board.set_value(0, 3, "W")
# board.set_value(1, 3, "B")
#
# board.set_value(0, 6, "W")
# board.remove_piece(1, 1, "B")
#
# board.set_value(1, 5, "B")
# board.set_value(5, 5, "W")
#
# board.set_value(1, 1, "B")
# board.remove_piece(5, 5, "W")
# board.remove_piece(1, 1, "B")
#
#
# print(board)
# print(board.whites)
# print(board.blacks)
# print(board.placed_whites)
# print(board.placed_blacks)
#
# print(board.is_end())
#
# print(board.getNumberOfDoubleMorrises("B"))
# print(board.getNumberOfMorrises("B"))
# print(board.getNumberOfDoubles("B"))
# print(board.get_free_adj(5, 5))
# print(board.evaluate(1, 1))
"""Dovde"""


#
# board2 = Board()
# board2.set_value(5, 1, "B")
# board2.set_value(5, 3, "B")
# board2.set_value(5, 5, "B")

# board.is_end()
# win, winner, outcome = board.is_end()
# print(board.is_end())


# board.set_value(0, 0, "W")
# board.set_value(0, 3, "W")
# board.set_value(3, 0, "W")
#
# board.set_value(6, 6, "W")
# board.set_value(3, 6, "W")
# board.set_value(6, 3, "W")
#


# # redosled pozivanja funkcija za proveru stanja na tabli
# # obavezno je da prvo ide dupli morris pa obican i onda potencijalni morris(dupla polja)
# print(board.getNumberOfGuaranteedMorris("W"))
# print(board.getNumberOfDoubleMorrises("W"))
# print(board.getNumberOfMorrises("W"))
# print(board.getNumberOfDoubles("W"))
# print(board.getEmptyFields())
# print(board.get_moves_phase_2("W"))
# print(board.evaluate(5, 5))



# print(board2)
# print(board2.getNumberOfGuaranteedMorris("W"))
# print(board2.getNumberOfDoubleMorrises("W"))
# print(board2.getNumberOfMorrises("B"))
# print(board2.getNumberOfDoubles("W"))
# print(board2.getEmptyFields())
# print(board2.get_moves_phase_2("W"))
# print(board.evaluate(5, 5))
# print(board2.evaluate(board2.last_move[0], board2.last_move[1]))

# print(board.getNumberOfBlockedPawns("W"))
# print(board.getNumberOfBlockedPawns("B"))


