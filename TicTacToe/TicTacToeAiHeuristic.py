"""
Heuristik:
win selber: +1000
2 besetzte Felder und moeglicher finish move selber: +10
2 besetzte Felder und moeglicher finish move gegner: -100
moeglichkeiten zum gewinnen: +1
moeglichkeiten Gegner zum gewinnen: -1
"""
import copy


class TicTacToeAiHeuristic:
    def __init__(self):
        i = 0

    def getmove(self, board, player):
        best_heuristic = -100000
        best_x = 0
        best_y = 0
        for x in range(3):
            for y in range(3):
                if board[x][y] == 0:
                    temp_board = copy.deepcopy(board)
                    temp_board[x][y] = player
                    new_heuristic = self.get_heurisitc(temp_board, player)
                    if new_heuristic > best_heuristic:
                        best_heuristic = new_heuristic
                        best_x = x
                        best_y = y
        return [best_x, best_y]

    def get_heurisitc(self, board, player):
        heuristic = 0
        for x in range(3):
            # horizontal
            heuristic += self.get_heuristic_of_combo(board[x], player)
            # vertical
            heuristic += self.get_heuristic_of_combo([board[0][x], board[1][x], board[2][x]], player)
        # diagonal
        heuristic += self.get_heuristic_of_combo([board[0][0], board[1][1], board[2][2]], player)
        heuristic += self.get_heuristic_of_combo([board[0][2], board[1][1], board[2][0]], player)
        return heuristic

    def get_heuristic_of_combo(self, fields, player):
        for x in range(3):
            if fields[x] == 2:
                fields[x] = 10

        summ = 0
        for x in range(3):
            summ += fields[x]

        if player == 1:
            enemy_fields = (summ - (summ % 10))/10
            own_fields = summ - (10*enemy_fields)
        else:
            own_fields = (summ - (summ % 10))/10
            enemy_fields = summ - (10*own_fields)

        if own_fields != 0 and enemy_fields != 0:
            return 0  # no one can win in this combo
        if own_fields == 0 and enemy_fields == 0:
            return 0  # no one played here yet
        if own_fields > 0:
            if own_fields == 1:
                return 1  # good position
            if own_fields == 2:
                return 10  # you have a win condition
            if own_fields == 3:
                return 1000  # you win
        else:
            if enemy_fields == 1:
                return -1  # enemy has more possibilities
            if enemy_fields == 2:
                return -100  # enemy can win
            if enemy_fields == 3:
                return -10000  # something wrong Enemy already won
        return 0
