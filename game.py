from test import Board
from copy import deepcopy
import time

MIN = -1000000
MAX = 1000000


class Game(object):
    __slots__ = ["current_state", "player_turn"]

    def __init__(self, player_turn="W"):
        self.current_state = None
        self.player_turn = player_turn
        self.initialize_game()

    def initialize_game(self):
        self.current_state = Board()
        self.player_turn = "W"

    # def min_max_og(self, depth, alfa, beta, maxplayer):
    #     win, winner, outcome = self.current_state.is_end()
    #     #last_move = (A, B)
    #
    #     minval = [MIN, 0]
    #     maxval = [MAX, 0]
    #
    #     # end of recursion
    #     if depth == 0 or win is True:
    #         return self.current_state.evaluate(self.current_state.last_move[0], self.current_state.last_move[1], outcome)
    #
    #     # max player
    #     if maxplayer:
    #         max_eval = MIN
    #         for position in self.current_state.getEmptyFields():
    #             new = deepcopy(self)
    #             new.current_state.set_value(position[0], position[1], "B")
    #             morris = new.current_state.is_morris(position[0], position[1], "B")
    #             if morris != 0:
    #                 for white in new.current_state.white_pawns:
    #                     if white.is_morris == 0:
    #                         new.current_state.remove_piece(white[0], white[1], "W")
    #                         remval = new.current_state.evaluate(white[0], white[1])
    #                         new.current_state.set_value(white[0], white[1], "W")
    #                         if remval > minval[0]:
    #                             minval = [remval, white]
    #                     if minval[1] != 0:
    #                         new.current_state.remove_piece(minval[1][0], minval[1][1], "W")
    #             maxplayer = False
    #             evaluation = new.min_max(depth-1, alfa, beta, maxplayer)
    #             if evaluation > max_eval:
    #                 max_eval = evaluation
    #             if evaluation > alfa:
    #                 alfa = evaluation
    #             if beta <= alfa:
    #                 break
    #             return max_eval
    #
    #     else:
    #         min_eval = MAX
    #         for position in self.current_state.getEmptyFields():
    #             new = deepcopy(self)
    #             new.current_state.set_value(position[0], position[1], "W")
    #             morris = new.current_state.is_morris(position[0], position[1], "W")
    #             if morris != 0:
    #                 for white in new.current_state.white_pawns:
    #                     if white.is_morris == 0:
    #                         new.current_state.remove_piece(white[0], white[1], "B")
    #                         remval = new.current_state.evaluate(white[0], white[1])
    #                         new.current_state.set_value(white[0], white[1], "B")
    #                         if remval < maxval[0]:
    #                             maxval = [remval, white]
    #                     if maxval[1] != 0:
    #                         new.current_state.remove_piece(maxval[1][0], maxval[1][1], "W")
    #             maxplayer = True
    #             evaluation = new.min_max(depth - 1, alfa, beta, maxplayer)
    #             if evaluation < min_eval:
    #                 min_eval = evaluation
    #             if evaluation > beta:
    #                 beta = evaluation
    #             if beta <= alfa:
    #                 break
    #             return min_eval

    def min_max(self, depth, alpha, beta, maxplayer):
        global move_set
        win, winner, outcome = self.current_state.is_end()

        if depth == 0 or win is True:
            return self.current_state.evaluate(self.current_state.last_move[0], self.current_state.last_move[1])

        # maximazing player
        if maxplayer:
            max_eval = MIN
            if self.current_state.is_phase_one():
                setups = self.every_move_1()
            else:
                setups = self.every_move_2()
            for move in setups:
                if move[0].current_state.is_morris(move[1][0], move[1][1], "B"):
                    # morris_eval[0] -> najbolji Game() za maksimajzera
                    # morris_eval[1] -> minimajzerov najbolji pijun

                    #removed = (move[0].eval_best_morris()[0], move[0].eval_best_morris()[1])
                    # evaluation = removed[0].min_max(depth - 1, alpha, beta, False)
                    removed = move[0].eval_best_morris()[1]
                    move[0].current_state.remove_piece(removed[0], removed[1], "W")
                    evaluation = move[0].min_max(depth - 1, alpha, beta, False)
                else:
                    evaluation = move[0].min_max(depth - 1, alpha, beta, False)

                if max_eval < evaluation:
                    max_eval = evaluation
                    move_set[0] = move[1]
                    # if not move[0].current_state.is_phase_one():
                    #     move_set[1] = move[2]

                # max_eval = max(max_eval, evaluation)
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break
            return max_eval

        # minimazing player
        else:
            min_eval = MAX
            if self.current_state.is_phase_one():
                setups = self.every_move_1()
            else:
                setups = self.every_move_2()
            for move in setups:
                if move[0].current_state.is_morris(move[1][0], move[1][1], "W"):
                    # morris_eval[2] -> najgori Game() za maksimajzera
                    # morris_eval[3] -> maksimajzerov najbolji pijun

                    # next_move = (move[0].eval_best_morris()[2], move[0].eval_best_morris()[3])
                    # evaluation = next_move[0].min_max(depth - 1, alpha, beta, True)
                    removed = move[0].eval_best_morris()[3]
                    move[0].current_state.remove_piece(removed[0], removed[1], "B")
                    evaluation = move[0].min_max(depth - 1, alpha, beta, True)
                else:
                    evaluation = move[0].min_max(depth - 1, alpha, beta, True)

                if min_eval > evaluation:
                    min_eval = evaluation
                    move_set[0] = move[1]

                # min_eval = min(min_eval, evaluation)
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break
            return min_eval

    # returnuje listu n-torki (Game(), pozicija)...
    def every_move_1(self):
        setups = []
        moves = self.current_state.getEmptyFields()
        if self.player_turn == "W":
            player = "W"
            opponent = "B"
        else:
            player = "B"
            opponent = "W"
        for position in moves:
            board = deepcopy(self)
            # board = Game()
            # board.current_state = deepcopy(self.current_state)

            board.current_state.set_value(position[0], position[1], player)
            board.player_turn = opponent
            setups.append((board, position))
        return setups

    # returnuje listu n-torki (Game(), pocetna pozicija, krajnja pozicija)
    def every_move_2(self):
        setups = []
        movable = []
        if self.player_turn == "W":
            player = "W"
            pawns = self.current_state.white_pawns
            opponent = "B"
        else:
            player = "B"
            pawns = self.current_state.black_pawns
            opponent = "W"
        for start in pawns:
            if not self.current_state.is_blocked(start[0], start[1]):
                movable.append(start)
        # start -> pijun kog je moguce pomeriti
        # movable -> lista startova
        # end -> prazna pozicija na koju pijun biva prebacen
        # dobio listu pijuna koji se mogu pomeriti
        for start in movable:
            for end in self.current_state.get_free_adj(start[0], start[1]):
                board = deepcopy(self)
                # board = Game()
                # board.current_state = deepcopy(self.current_state)

                board.current_state.remove_piece(start[0], start[1], player)
                board.current_state.set_value(end[0], end[1], player)
                board.player_turn = opponent
                setups.append((board, end, start))
        return setups

        # iteriraj kroz sve moguce poteze i dodaj ponmeranje svakog pijuna posle toga

    # returnuje n-torku (max_tabla, max_uklonjen, min_tabla, min_uklonjena)
    def eval_best_morris(self):
        setups = [0, 0, 0, 0]
        # SETUPS = (MAX_TABLE, MAX_EVAL, MIN_TABLE, MIN_EVAL)
        # ulazni parametar igraca je protivnik igraca koji je sklopio micu
        # tj player -> opponent; opponent -> player -> OBRNUTI SU TAKO DA TREBA OBRNUTI SVE *face palm*
        removable = []
        max_eval = MIN
        min_eval = MAX
        if self.player_turn == "W":
            op_pawns = self.current_state.white_pawns
            opponent = "W"
        else:
            op_pawns = self.current_state.black_pawns
            opponent = "B"
        for op in op_pawns:
            if self.current_state.is_morris(op[0], op[1], opponent) == 0:
                removable.append(op)
        for op in removable:
            board = deepcopy(self)
            # board = Game()
            # board.current_state = deepcopy(self.current_state)

            board.current_state.remove_piece(op[0], op[1], opponent)
            removal_eval = board.current_state.evaluate(op[0], op[1])
            if removal_eval > max_eval:
                max_eval = removal_eval
                setups[0] = board
                setups[1] = op
            if removal_eval < min_eval:
                min_eval = removal_eval
                setups[2] = board
                setups[3] = op
            # obrati paznju ovde da promenis player turn samo nez jos kako,
            # posto se ovde ulazi sa trenutnim igracem koji je sastavio micu,
            # tako da bi trebalo da se prebaci na kraju ovoga na sledeceg
        return setups

    def play(self):
        phase = 1
        while True:

            win, winner, outcome = self.current_state.is_end()
            if self.current_state.last_move is not None:
                print(self.current_state.evaluate(self.current_state.last_move[0], self.current_state.last_move[1]))
            print(self.current_state.is_end())

            if win is True:
                if winner == "W":
                    print("Pobednik je beli igrac")
                else:
                    print("PObednik je crni igrac")
                break
            if phase == 1 and self.current_state.is_phase_one():
                print("----- FAZA 1 -----")
                self.phase_1_play()
            else:
                phase = 2
                print("----- FAZA 2 -----")
                self.phase_2_play()

    def phase_1_play(self):
        player = self.player_turn
        if player == "W":
            opponent = "B"
            pawns = self.current_state.black_pawns
        else:
            opponent = "W"
            pawns = self.current_state.white_pawns

        print(self.current_state)
        print(player + " -> IGRAC NA POTEZU")
        print(self.current_state.getEmptyFields())
        i = int(input("Izaberite i koordinatu >> "))
        j = int(input("Izaberite j koordinatu >> "))
        while True:
            if not self.current_state.is_empty(i, j):
                print("Neispravne koordinate, ponovite unos")
                i = int(input("Izaberite i koordinatu >> "))
                j = int(input("Izaberite j koordinatu >> "))
            else:
                break
        self.current_state.set_value(i, j, player)

        removable = []
        for xy in pawns:
            if self.current_state.is_morris(xy[0], xy[1], opponent) == 0:
                removable.append((xy[0], xy[1]))
        if self.current_state.is_morris(i, j, player) == 2:
            for i in range(2):
                if len(removable) == 0:
                    print("Ne postoje pijuni koje mozete da sklonite")
                else:
                    print("Izaberite protivnickog pijuna kog zelite da sklonite")
                    print(removable)
                    i = int(input("Izaberite i koordinatu >> "))
                    j = int(input("Izaberite j koordinatu >> "))
                    while True:
                        if (i, j) not in removable:
                            print("Neispravne koordinate, ponovite unos")
                            i = int(input("Izaberite i koordinatu >> "))
                            j = int(input("Izaberite j koordinatu >> "))
                        else:
                            break
                    self.current_state.remove_piece(i, j, opponent)

        elif self.current_state.is_morris(i, j, player) == 1:
            if len(removable) == 0:
                print("Ne postoje pijuni koje mozete da sklonite")
            else:
                print("Izaberite protivnickog pijuna kog zelite da sklonite")
                print(removable)
                i = int(input("Izaberite i koordinatu >> "))
                j = int(input("Izaberite j koordinatu >> "))
                while True:
                    if (i, j) not in removable:
                        print("Neispravne koordinate, ponovite unos")
                        i = int(input("Izaberite i koordinatu >> "))
                        j = int(input("Izaberite j koordinatu >> "))
                    else:
                        break
                self.current_state.remove_piece(i, j, opponent)
        self.player_turn = opponent

    def phase_2_play(self):
        player = self.player_turn
        if player == "W":
            opponent = "B"
            pawns = self.current_state.black_pawns
            pl_pawns = self.current_state.white_pawns
        else:
            opponent = "W"
            pawns = self.current_state.white_pawns
            pl_pawns = self.current_state.black_pawns

        print(self.current_state)
        print(player + " -> IGRAC NA POTEZU")
        movable = []
        for xy in pl_pawns:
            if not self.current_state.is_blocked(xy[0], xy[1]):
                movable.append(xy)
        print("Izaberi pijuna kog zelite da pomerite")
        print(movable)
        i = int(input("Izaberite i koordinatu >> "))
        j = int(input("Izaberite j koordinatu >> "))
        while True:
            if (i, j) not in movable:
                print("Neispravne koordinate, ponovite unos")
                i = int(input("Izaberite i koordinatu >> "))
                j = int(input("Izaberite j koordinatu >> "))
            else:
                break

        self.current_state.remove_piece(i, j, player)

        print("Izaberite gde zelite da pomerite pijuna")
        print(self.current_state.get_free_adj(i, j))
        adj_i = int(input("Izaberite i koordinatu >> "))
        adj_j = int(input("Izaberite j koordinatu >> "))
        while True:
            if (adj_i, adj_j) not in self.current_state.get_free_adj(i, j):
                print("Neispravne koordinate, ponovite unos")
                i = int(input("Izaberite i koordinatu >> "))
                j = int(input("Izaberite j koordinatu >> "))
            else:
                break

        self.current_state.set_value(adj_i, adj_j, player)

        removable = []
        for xy in pawns:
            if self.current_state.is_morris(xy[0], xy[1], opponent) == 0:
                removable.append(xy)
        if self.current_state.is_morris(adj_i, adj_j, player) == 2:
            for i in range(2):
                if len(removable) == 0:
                    print("Ne postoje pijuni koje mozete da sklonite")
                else:
                    print("Izaberite protivnickog pijuna kog zelite da sklonite")
                    print(removable)
                    i = int(input("Izaberite i koordinatu >> "))
                    j = int(input("Izaberite j koordinatu >> "))
                    while True:
                        if (i, j) not in removable:
                            print("Neispravne koordinate, ponovite unos")
                            i = int(input("Izaberite i koordinatu >> "))
                            j = int(input("Izaberite j koordinatu >> "))
                        else:
                            break
                    self.current_state.remove_piece(i, j, opponent)

        elif self.current_state.is_morris(adj_i, adj_j, player) == 1:
            if len(removable) == 0:
                print("Ne postoje pijuni koje mozete da sklonite")
            else:
                print(removable)
                print("Izaberite protivnickog pijuna kog zelite da sklonite")
                i = int(input("Izaberite i koordinatu >> "))
                j = int(input("Izaberite j koordinatu >> "))
                while True:
                    if (i, j) not in removable:
                        print("Neispravne koordinate, ponovite unos")
                        i = int(input("Izaberite i koordinatu >> "))
                        j = int(input("Izaberite j koordinatu >> "))
                    else:
                        break
                self.current_state.remove_piece(i, j, opponent)
        self.player_turn = opponent

    def pijuni(self):
        print("\n crni -> ", end=" ")
        for i in self.current_state.black_pawns:
            print(i, end=" ")
        print("\n beli -> ", end=" ")
        for i in self.current_state.white_pawns:
            print(i, end=" ")
        print()

    def min_max_2(self, depth, alpha, beta, maxplayer):
        global move_set
        global move_set_2
        win, winner, outcome = self.current_state.is_end()

        if depth == 0 or win is True:
            return self.current_state.evaluate(self.current_state.last_move[0], self.current_state.last_move[1])

        # maximazing player
        if maxplayer:
            max_eval = MIN
            if self.current_state.is_phase_one():
                setups = self.every_move_1()
            else:
                setups = self.every_move_2()
            for move in setups:
                if move[0].current_state.is_morris(move[1][0], move[1][1], "B"):
                    # morris_eval[0] -> najbolji Game() za maksimajzera
                    # morris_eval[1] -> minimajzerov najbolji pijun

                    #removed = (move[0].eval_best_morris()[0], move[0].eval_best_morris()[1])
                    # evaluation = removed[0].min_max(depth - 1, alpha, beta, False)
                    removed = move[0].eval_best_morris()[1]
                    move[0].current_state.remove_piece(removed[0], removed[1], "W")
                    evaluation = move[0].min_max(depth - 1, alpha, beta, False)
                else:
                    evaluation = move[0].min_max(depth - 1, alpha, beta, False)

                # if move[0].current_state.is_phase_one():
                if move[0].current_state.blacks >= 0:
                    if max_eval < evaluation:
                        max_eval = evaluation
                        move_set[0] = move[1]
                else:
                    if max_eval < evaluation:
                        max_eval = evaluation
                        move_set_2 = move
                        # move_set[0] = move[1]
                        # move_set[1] = move[2]
                        # try:
                        #     move_set[1] = move[2]
                        # except IndexError:
                        #     print()
                # if max_eval < evaluation:
                #     max_eval = evaluation
                #     move_set[0] = move[1]
                #     if not move[0].current_state.is_phase_one():
                #         move_set[0] = move[1]
                #         move_set[1] = move[2]

                    # if not move[0].current_state.is_phase_one():
                    #     move_set[1] = move[2]

                # max_eval = max(max_eval, evaluation)
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break
            return max_eval

        # minimazing player
        else:
            min_eval = MAX
            if self.current_state.is_phase_one():
                setups = self.every_move_1()
            else:
                setups = self.every_move_2()
            for move in setups:
                if move[0].current_state.is_morris(move[1][0], move[1][1], "W"):
                    # morris_eval[2] -> najgori Game() za maksimajzera
                    # morris_eval[3] -> maksimajzerov najbolji pijun

                    # next_move = (move[0].eval_best_morris()[2], move[0].eval_best_morris()[3])
                    # evaluation = next_move[0].min_max(depth - 1, alpha, beta, True)
                    removed = move[0].eval_best_morris()[3]
                    move[0].current_state.remove_piece(removed[0], removed[1], "B")
                    evaluation = move[0].min_max(depth - 1, alpha, beta, True)
                else:
                    evaluation = move[0].min_max(depth - 1, alpha, beta, True)

                # if move[0].current_state.is_phase_one():
                if move[0].current_state.whites >= 0:
                    if min_eval > evaluation:
                        min_eval = evaluation
                        # move_set[0] = move[1]
                else:
                    if min_eval > evaluation:
                        min_eval = evaluation
                        move_set_2 = move
                        # move_set[0] = move[1]
                        # move_set[1] = move[2]


                        # move_set[0] = move[1]
                        # try:
                        #     move_set[1] = move[2]
                        # except IndexError:
                        #     print()


                # if min_eval > evaluation:
                #     min_eval = evaluation
                #     move_set[0] = move[1]
                #     if not move[0].current_state.is_phase_one():
                #         move_set[0] = move[1]
                #         move_set[1] = move[2]

                # min_eval = min(min_eval, evaluation)
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break
            return min_eval

    def play_AI(self):
        phase = 1
        while True:
            self.pijuni()
            win, winner, outcome = self.current_state.is_end()
            # if self.current_state.last_move is not None:
            #     print(self.current_state.evaluate(self.current_state.last_move[0], self.current_state.last_move[1]))
            # print(self.current_state.is_end())

            if win is True:
                if winner == "W":
                    print("POBEDILI STE !!!")
                else:
                    print("IZGUBILI SET OD KOMPJUTERA :(")
                break

            if self.player_turn == "W":
                if phase == 1 and self.current_state.is_phase_one():
                    print("----- FAZA 1 -----")
                    self.phase_1_play()
                else:
                    phase = 2
                    print("----- FAZA 2 -----")
                    self.phase_2_play()
                self.player_turn = "B"
            else:
                start_time = time.time()
                if self.current_state.is_phase_one():
                    self.min_max_2(3, MIN, MAX, True)
                    print("pijun -> " + str(move_set[0]))
                    # + " faza 1 -> " + str(move_set[1])
                    self.current_state.set_value(move_set[0][0], move_set[0][1], "B")
                    self.player_turn = "W"
                    if self.current_state.is_morris(move_set[0][0], move_set[0][1], "B"):
                        best_removal = self.eval_best_morris()[1]
                        self.current_state.remove_piece(best_removal[0], best_removal[1], "W")
                else:

                    self.min_max_2(3, MIN, MAX, True)
                    # print("pijun -> " + str(move_set[1]) + " potez -> " + str(move_set[0]))
                    print("pijun -> " + str(move_set_2[2]) + " potez -> " + str(move_set_2[1]))
                    self.current_state.remove_piece(move_set_2[2][0], move_set_2[2][1], "B")
                    self.current_state.set_value(move_set_2[1][0], move_set_2[1][1], "B")
                    # self.current_state.remove_piece(move_set[1][0], move_set[1][1], "B")
                    # self.current_state.set_value(move_set[0][0], move_set[0][1], "B")
                    self.player_turn = "W"
                    # if self.current_state.is_morris(move_set[0][0], move_set[0][1], "B"):
                    if self.current_state.is_morris(self.current_state.last_move[0], self.current_state.last_move[1],
                                                    "B"):
                        best_removal = self.eval_best_morris()[1]
                        self.current_state.remove_piece(best_removal[0], best_removal[1], "W")
                        print("Sklonjen pijun na poziciji -> " + str(best_removal))
                print("--- %s seconds ---" % (time.time() - start_time))


# move_set[0] -> polje na koje se postavlja figurica
# move_set[1] -> polje sa kog se skida figurica
move_set = [(0, 0), (0, 0)]
move_set_2 = ()
# game = Game()
# game.play_AI()


# game.current_state.set_value(0, 0, "W")
# game.current_state.set_value(3, 0, "W")
# game.current_state.set_value(3, 1, "W")
# game.current_state.set_value(5, 1, "W")
#
# game.current_state.set_value(0, 6, "B")
# game.current_state.set_value(6, 0, "B")
# game.current_state.set_value(1, 1, "B")
# game.current_state.set_value(3, 2, "B")
# game.player_turn = "W"
# setups = game.every_move_2()
# for i in setups:
#     print(i[0].current_state, end=" od -> ")
#     print(i[2], end=" do -> ")
#     print(i[1], end=" sledeci potez -> ")
#     print(i[0].player_turn)
#     set = i[0].every_move_2()
#     for m in set:
#         print(m[0].current_state, end=" od -> ")
#         print(m[2], end=" do -> ")
#         print(m[1], end=" sledeci potez -> ")
#         print(m[0].player_turn)

# print(game)
# game.play_AI()
# game.play()
# game.play_AI()

# game.current_state.set_value(0, 0, "W")
# game.player_turn = "B"
#
# game.min_max(3, MIN, MAX, True)
# game.current_state.set_value(move_set[0][0], move_set[0][1], "B")
# game.player_turn = "W"
#
# game.current_state.set_value(0, 3, "W")
# game.player_turn = "B"
#
# game.min_max(3, MIN, MAX, True)
# game.current_state.set_value(move_set[0][0], move_set[0][1], "B")
# game.player_turn = "W"
#
# print(game.current_state)

# game.current_state.set_value(3, 0, "W")
# game.current_state.set_value(3, 1, "W")
# game.current_state.set_value(6, 0, "B")
# game.current_state.set_value(3, 2, "B")
# game.current_state.set_value(5, 3, "B")
# game.current_state.set_value(3, 5, "B")
# game.current_state.set_value(6, 6, "W")
# game.current_state.set_value(3, 6, "B")
# game.current_state.set_value(2, 3, "W")
# game.current_state.set_value(3, 4, "B")
# game.player_turn = "W"
# game.pijuni()
# print(game.eval_best_morris())
# setup = game.eval_best_morris()
# print(setup[0].current_state, end=" ")
# print(setup[1], end=" ")
# print(setup[0].player_turn)
# print(setup[2].current_state, end=" ")
# print(setup[3], end=" ")
# print(setup[2].player_turn)

# setups = game.every_move_1()
# for s in setups:
#     print(s[0].current_state, end="  ")
#     print(s[1], end=" ")
#     print(s[0].player_turn)
# print(game.player_turn)


# print(game.current_state)
# game.min_max(3, MIN, MAX, True)
# game.current_state.set_value(move_set[0][0], move_set[0][1], "B")
# print(game.current_state)

"""NAJBOLJA OTKLONJENA PROTIVNICKA FIGURICA"""
# game.current_state.set_value(0, 0, "B")
# game.current_state.set_value(1, 1, "W")
#
# game.current_state.set_value(0, 3, "B")
# game.current_state.set_value(1, 3, "W")
#
# game.current_state.set_value(3, 1, "W")
# game.current_state.set_value(6, 3, "W")
#
# game.current_state.set_value(0, 6, "B")
# potezi = game.eval_best_morris()
# print(potezi[0].current_state, end=" najbolji: ")
# print(potezi[1])
#
# print(potezi[2].current_state, end=" najgori: ")
# print(potezi[3])

"""MOGUCI POTEZI SA SVOJIM TABLAMA -> FAZA 1"""
# for potez in game.every_move_1():
#     print(potez[0].current_state, end="    start: ")
#     print(potez[1])

"""MOGUCI POTEZI SA SVOJIM TABLAMA -> FAZA 2"""
# game.current_state.set_value(0, 0, "W")
# game.current_state.set_value(0, 3, "W")
# game.current_state.set_value(3, 0, "W")
#
# game.current_state.set_value(1, 1, "B")
# game.current_state.set_value(1, 3, "B")
# game.current_state.set_value(3, 1, "B")
#
# game.current_state.set_value(6, 6, "B")
# game.current_state.set_value(5, 1, "W")
# game.player_turn = "B"
#
# for potez in game.every_move_2():
#     print(potez[0].current_state, end="    start: ")
#     print(potez[1], end=" -> ")
#     print(potez[2])