from naoqi import ALProxy
import qi

import time


class SpeechDetection(object):

    def __init__(self, session, vocabulary, callback):
        # Get the service ALMemory.
        self.memory = session.service("ALMemory")
        # Connect the event callback.
        self.subscriber = self.memory.subscriber("WordRecognized")
        self.subscriber.signal.connect(callback)

        self.__start_game_text = session.service("ALSpeechRecognition")

        self.__start_game_text.pause(True)
        self.__start_game_text.setLanguage("English")
        self.__start_game_text.setVocabulary(vocabulary, False)
        self.__start_game_text.pause(False)

        self.__start_game_text.subscribe("SpeechDetection")
        print('Speech recognition engine started')

    def on_speech_detected(self, value):
        print(value)

    def unsubscribe(self):
        self.__start_game_text.unsubscribe("SpeechDetection")

