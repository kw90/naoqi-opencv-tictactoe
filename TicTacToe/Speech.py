class Speech(object):

    def __init__(self, session):
        self.__speech = session.service("ALAnimatedSpeech")
        self.__textToSpeech = session.service("ALTextToSpeech")
        self.__configuration = {"bodyLanguageMode": "disabled"}

        #self.__textToSpeech.getParameter("speed")
        self.__textToSpeech.setParameter("speed", 90)

        # say the text with the local configuration
        # self.__speech.say("Speech configuration done", self.__configuration)
        print "speech configuration done"

    def say(self, text):
        self.__speech.say(text, self.__configuration)
