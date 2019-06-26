from TicTacToeAiRand import TicTacToeAiRand
from TicTacToeAiHeuristic import TicTacToeAiHeuristic
import PositionTransformator
from MoveMotors import MoveMotors
import threading
import qi

class TicTacToe:
    """"TicTacToe Game Class"""
    playField = [[0 for x in range(3)] for y in range(3)]
    actual_Player = 0
    colourPlayer1 = "red"
    colourPlayer2 = "blue"
    # player1 = user
    #player2 = TicTacToeAiHeuristic()
    player2 = TicTacToeAiRand()

    def __init__(self, session, speech, show_screen):
        self.__speech = speech
        self.print_field()
        self.__session = session
        self.__moveMotors = MoveMotors(self.__session)
        self.__showScreen = show_screen
        self.move_player2 = None

    def restart(self):
        self.playField = [[0 for x in range(3)] for y in range(3)]

    def place(self, x, y):
        if self.playField[x][y] != 1 and self.playField[x][y] != 2:
            self.playField[x][y] = 1
            if self.player_won() == 0:
                self.move_player2 = self.player2.getmove(self.playField, 2)
                self.playField[self.move_player2[0]][self.move_player2[1]] = 2
                if self.move_player2[1] == 2:
                    self.move_player2[1] = 0
                else:
                    if self.move_player2[1] == 0:
                        self.move_player2[1] = 2
                self.__showScreen.show_screen(self.get_url_params())
                self.__speech.say("move detected")
                future_say = qi.async(self.say_move, self.move_player2, delay=1000000)
                future_point = qi.async(self.point_move, self.move_player2, delay=0)
                future_say.wait()
                future_point.wait()
                #target=self.__moveMotors.point_to_position, args=(move_player2[0], move_player2[1]))
            self.print_field()
            return True
        return False

    def say_move(self, move_player2):
        # TODO remove "move detected" due to unnatural interaction
        if move_player2[0] == 0 and move_player2[1] == 0:
            self.__speech.say("place my stone at the field A1")
        elif move_player2[0] == 0 and move_player2[1] == 1:
            self.__speech.say("place my stone at the field A2")
        elif move_player2[0] == 0 and move_player2[1] == 2:
            self.__speech.say("place my stone at the field A3")
        elif move_player2[0] == 1 and move_player2[1] == 0:
            self.__speech.say("place my stone at the field B1")
        elif move_player2[0] == 1 and move_player2[1] == 1:
            self.__speech.say("place my stone at the field B2")
        elif move_player2[0] == 1 and move_player2[1] == 2:
            self.__speech.say("place my stone at the field B3")
        elif move_player2[0] == 2 and move_player2[1] == 0:
            self.__speech.say("place my stone at the field C1")
        elif move_player2[0] == 2 and move_player2[1] == 1:
            self.__speech.say("place my stone at the field C2")
        elif move_player2[0] == 2 and move_player2[1] == 2:
            self.__speech.say("place my stone at the field C3")
        return True

    def point_move(self, move_player2):
        self.__moveMotors.point_to_position(move_player2[0], move_player2[1])
        return True

    def get_field(self):
        return self.playField

    def print_field(self):
        print('\n'.join([''.join(['{:4}'.format(item) for item in row])
                         for row in self.playField]))

    def player_won(self):
        for x in range(3):
            # check horizontal
            player = self.playField[1][x]
            if player == self.playField[0][x] and player == self.playField[2][x]:
                return player
            # check vertical
            player = self.playField[x][1]
            if player == self.playField[x][0] and player == self.playField[x][2]:
                return player
        # check diagonal
        player = self.playField[1][1]
        if player == self.playField[0][0] and player == self.playField[2][2]:
            return player
        if player == self.playField[0][2] and player == self.playField[2][0]:
            return player
        if self.full_board():
            return 3
        return 0

    def full_board(self):
        for x in range(3):
            for y in range(3):
                if self.playField[x][y] != 1 and self.playField[x][y] != 2:
                    return False
        return True

    def get_url_params(self):
        text = "?"
        for x in range(3):
            for y in range(3):
                if self.playField[x][y] == 1:
                    text += PositionTransformator.get_string_from_coordinates(x, y) + "=" + self.colourPlayer1 + "&"
                if self.playField[x][y] == 2:
                    text += PositionTransformator.get_string_from_coordinates(x, y) + "=" + self.colourPlayer2 + "&"
        text = text[:-1]
        return text


# cce = TicTacToe()
# while True:
#    text = raw_input("you'r Move (bsp: 1 2): ")
#    text_split = text.split(" ")
#    cce.place(int(text_split[0]), int(text_split[1]))

