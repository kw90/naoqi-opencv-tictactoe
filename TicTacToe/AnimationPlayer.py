import qi
import almath
import time

from Posture import rest_position
from Speech import Speech


class AnimationPlayer:

    def __init__(self, session, motion):
        self.session = session
        self.animation_service = session.service("ALAnimationPlayer")
        self.animation_path = 'animations/Stand/'
        self.__speech = Speech(session=session)
        self.__motion = motion

    def reaction_won(self):
        self.animation_service.run(self.animation_path+'Emotions/Positive/Happy_4')
        rest_position(session=self.session)
        return True

    def reaction_lost(self):
        self.animation_service.run(self.animation_path + 'Emotions/Neutral/Embarrassed_1')
        rest_position(session=self.session)
        return True

    def reaction_draw(self):
        self.animation_service.run(self.animation_path + 'Gestures/IDontKnow_1')
        rest_position(session=self.session)
        return True

    def play_win_animation(self):
        future_say = qi.async(self.say_reaction, "I won the game!", delay=500)
        future_animation = qi.async(self.do_animation, self.reaction_won(), delay=0)
        while future_say == False or future_animation == False:
            time.sleep(0.5)
        self.look_at_player_and_say("Good luck next time!")

    def play_draw_animation(self):
        future_say = qi.async(self.say_reaction, "Sadly no one won.", delay=500)
        future_animation = qi.async(self.do_animation, self.reaction_draw(), delay=0)
        while future_say == False or future_animation == False:
            time.sleep(0.5)
        self.look_at_player_and_say("Let's try again!")

    def play_lose_animation(self):
        future_say = qi.async(self.say_reaction, "You won the Game!", delay=500)
        future_animation = qi.async(self.do_animation, self.reaction_draw(), delay=0)
        while future_say == False or future_animation == False:
            time.sleep(0.5)
        self.look_at_player_and_say("Congratulations!")

    def look_at_player_and_say(self, text):
        self.__motion.setStiffnesses("Head", 1.0)
        names = ["HeadYaw", "HeadPitch"]
        angles = [78. * almath.TO_RAD, -30. * almath.TO_RAD]
        times = [1., 1.]
        is_absolute = True
        self.__motion.angleInterpolation(names, angles, times, is_absolute)
        self.__speech.say(text=text)
        angles = [0., 0.]
        times = [1., 1.]
        is_absolute = True
        self.__motion.angleInterpolation(names, angles, times, is_absolute)

    def say_reaction(self, reaction_text):
        self.__speech.say(text=reaction_text)
        return True

    def do_animation(self, animation):
        return animation

