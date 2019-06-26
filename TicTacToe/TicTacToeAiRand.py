from random import randint


class TicTacToeAiRand:
    def __init__(self):
        i = 0

    def getmove(self, board, player):
        print "RandAiMakesMove"
        x = randint(0, 2)
        y = randint(0, 2)
        while board[x][y]:
            x = randint(0, 2)
            y = randint(0, 2)
        return [x, y]
