# coding=utf-8
from SpeechDetection import SpeechDetection
from ShowScreen import ShowScreen
from Speech import Speech
from TicTacToe import TicTacToe
from MoveReader import MoveReader
from AnimationPlayer import AnimationPlayer
import time
import qi
import almath


class GameHandler(object):

    def __init__(self, session, ip, motion, leds):
        # self.__play_array = ["top left", "top middle", "top right", "middle left", "middle middle", "middle right", "bottom left", "bottom middle", "bottom right"]
        self.__session = session
        self.__speech = Speech(self.__session)
        self.__showScreen = ShowScreen(self.__session, ip)
        self.__showScreen.show_screen("")
        self.__game = TicTacToe(self.__session, self.__speech, self.__showScreen)
        self.__moveReader = MoveReader(self.__session, self.__game)
        self.__speechDetection = SpeechDetection(self.__session, ["Let's Play", "Stop"], self.speech_callback)
        self.__animationPlayer = AnimationPlayer(self.__session, motion)
        self.__waiting_game_start = 1
        self.__playing = 1
        self.__program_running = 1
        self.__motion = motion
        self.__leds = leds
        while self.__program_running:
            while self.__waiting_game_start:
                input = raw_input('Say ´lets play´ or press enter to start a game.')
                if input == "":
                    #self.__speechDetection.unsubscribe()
                    self.look_at_player_and_say("Okay, Let's do this!", False)
                    self.__waiting_game_start = 0
                    self.__showScreen.show_screen("")
                    self.__game.restart()
                    self.__playing = 1
                pass
            while self.__playing:
                delta = 0
                self.__speech.say("Now make your move")
                while delta != 1:
                    time.sleep(0.5)
                    delta = self.__moveReader.read_move()
                    # if delta == 1:
                        # self.__speech.say("move detected please play my stone here")
                    if delta > 1:
                        self.look_at_player_and_say("Too many moves detected! Restore my image board", True)
                        time.sleep(1)

                self.__showScreen.show_screen(self.__game.get_url_params())
                print self.__game.get_url_params()

                delta2 = 1
                while delta2 != 0:
                    delta2 = self.__moveReader.check_correct_board()
                    if delta2 > 0:
                        self.look_at_player_and_say("Wrong move.", True)
                        self.__game.say_move(self.__game.move_player2)
                    time.sleep(1)

                self.__playing = self.__game.player_won() == 0
            winner = self.__game.player_won()
            if winner == 3:
                self.__animationPlayer.play_draw_animation()
            if winner == 2:
                self.__animationPlayer.play_win_animation()
            if winner == 1:
                self.__animationPlayer.play_lose_animation()
            print "End of Game"
            self.__waiting_game_start = 1
            self.__playing = 1
            self.__speechDetection.unsubscribe()
            self.__speechDetection = SpeechDetection(self.__session, ["Let's Play", "Stop"], self.speech_callback)
        #self.__speechDetection.unsubscribe()



    def say_reaction(self, reaction_text):
        self.__speech.say(text=reaction_text)
        return True

    def do_animation(self, animation):
        return animation

    def speech_callback(self, value):
        print(value)
        if value[0] == "Let's Play":
            if value[1] > 0.3:
                self.__speechDetection.unsubscribe()
                self.look_at_player_and_say("Okay, Let's do this!", False)
                self.__waiting_game_start = 0
                self.__showScreen.show_screen("")
                self.__game.restart()
                self.__speechDetection = SpeechDetection(self.__session, self.__play_array, self.play_callback)
                self.__playing = 1
        if value[0] == "Stop":
            if value[1] > 0.4:
                self.__playing = 0
                self.__waiting_game_start = 0
                self.__program_running = 0


    def look_at_player_and_say(self, text, warning_led):
        self.__motion.setStiffnesses("Head", 1.0)
        names = ["HeadYaw", "HeadPitch"]
        angles = [78. * almath.TO_RAD, -30. * almath.TO_RAD]
        times = [1., 1.]
        is_absolute = True
        self.__motion.angleInterpolation(names, angles, times, is_absolute)
        if warning_led:
            qi.async(self.rotate_eyes, delay=0)
        self.__speech.say(text=text)
        angles = [0., 0.]
        times = [1., 1.]
        is_absolute = True
        self.__motion.angleInterpolation(names, angles, times, is_absolute)

    def rotate_eyes(self):
        self.__leds.setIntensity('RightFaceLedsRed', 1.0)
        self.__leds.setIntensity('LeftFaceLedsRed', 1.0)
        self.__leds.rotateEyes(16711680, 1, 6)


