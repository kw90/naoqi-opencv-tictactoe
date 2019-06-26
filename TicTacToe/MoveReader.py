from TicTacToe import TicTacToe
from DetectBoard import DetectBoard

class MoveReader(object):

    def __init__(self, session, game):
        self.__session = session
        self.__game = game
        self.__moveX = 0
        self.__moveY = 0
        self.__detectBoard = DetectBoard()

    def check_correct_board(self):
        board = self.__detectBoard.get_board(self.__session)
        delta = self.checkdelta(board)
        return delta

    def read_move(self):
        # TODO: Read kamera
        board = self.__detectBoard.get_board(self.__session)
        delta = self.checkdelta(board)
        print('\n'.join([''.join(['{:4}'.format(item) for item in row])
                         for row in board]))
        if delta == 1:
            self.__game.place(self.__moveX, self.__moveY)
        return delta

    def checkdelta(self, board):
        delta = 0
        for x in range(3):
            for y in range(3):
                if board[x][y] != self.__game.get_field()[x][y]:
                    delta += 1
                    self.__moveX = x
                    self.__moveY = y
        return delta