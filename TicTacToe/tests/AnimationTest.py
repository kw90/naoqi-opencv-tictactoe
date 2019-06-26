import unittest
import qi
import time
from AnimationPlayer import AnimationPlayer

from Posture import rest_position


class PointMoveTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.session = qi.Session()
        self.session.connect('tcp://192.168.1.101:9559')
        self.motion = self.session.service('ALMotion')
        self.posture = self.session.service("ALRobotPosture")
        self.animation_player = AnimationPlayer(self.session, motion=self.motion)
        self.motion.setCollisionProtectionEnabled('Arms', False)
        self.motion.setExternalCollisionProtectionEnabled('All', False)
        rest_position(session=self.session)

    def test_reaction_won(self):
        self.animation_player.play_win_animation()

    def test_reaction_lost(self):
        self.animation_player.play_lose_animation()

    def test_reaction_draw(self):
        self.animation_player.play_draw_animation()


if __name__ == '__main__':
    unittest.main()
