import unittest
import qi
import os

from MoveMotors import MoveMotors
from Posture import rest_position


class PointMoveTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.session = qi.Session()
        self.session.connect('tcp://'+os.environ['PEPPER_IP']+':9559')
        self.motion = self.session.service('ALMotion')
        self.autonomous_life = self.session.service("ALAutonomousLife")
        self.posture = self.session.service("ALRobotPosture")
        self.move_motors = MoveMotors(session=self.session)
        self.motion.wakeUp()
        self.motion.setCollisionProtectionEnabled('Arms', True)
        self.motion.setExternalCollisionProtectionEnabled('All', False)

    def test_autonomous_life(self):
        self.assertEqual('disabled', self.autonomous_life.getState())

    def test_sleep_position(self):
        rest_position(self.session)

    def test_point_to_lower_left(self):
        print 'pointing to lower left'
        self.move_motors.point_to_position(2, 0)
        rest_position(self.session)

    def test_point_to_middle_left(self):
        print 'pointing to middle left'
        self.move_motors.point_to_position(1, 0)
        rest_position(self.session)

    def test_point_to_upper_left(self):
        print 'pointing to upper left'
        self.move_motors.point_to_position(0, 0)
        rest_position(self.session)

    def test_point_to_upper_right(self):
        print 'pointing to upper left'
        self.move_motors.point_to_position(0, 2)
        rest_position(self.session)


if __name__ == '__main__':
    unittest.main()
