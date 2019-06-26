import qi
import time
import almath

from Posture import rest_position


class MoveMotors(object):
    def __init__(self, session):
        self.session = session
        self.motion_service = session.service("ALMotion")
        self.namesL = ["LShoulderRoll", "LShoulderPitch", "LElbowYaw", "LElbowRoll", "LHand"]
        self.namesR = ["RShoulderRoll", "RShoulderPitch", "RElbowYaw", "RElbowRoll", "RHand"]
        hand_closed = 1
        shoulder_save_distance = 40 * almath.TO_RAD
        height_top_row = -52 * almath.TO_RAD
        height_middle_row = -45 * almath.TO_RAD
        height_bottom_row = -30 * almath.TO_RAD
        width_yaw = 8 * almath.TO_RAD
        width_left = -58 * almath.TO_RAD
        width_middle = -88 * almath.TO_RAD
        width_right = 58 * almath.TO_RAD

        angles_top = [[shoulder_save_distance, height_top_row, width_yaw, width_left, hand_closed],
                      [shoulder_save_distance, height_top_row, width_yaw, width_middle, hand_closed],
                      [-shoulder_save_distance, height_top_row + 15 * almath.TO_RAD, width_yaw, width_right, hand_closed]]
        angles_middle = [[shoulder_save_distance, height_middle_row, width_yaw, width_left, hand_closed],
                         [shoulder_save_distance, height_middle_row, width_yaw, width_middle, hand_closed],
                         [-shoulder_save_distance, height_middle_row + 15 * almath.TO_RAD, width_yaw, width_right, hand_closed]]
        angles_bottom = [[shoulder_save_distance, height_bottom_row, width_yaw, width_left, hand_closed],
                         [shoulder_save_distance, height_bottom_row, width_yaw, width_middle, hand_closed],
                         [-shoulder_save_distance, height_bottom_row + 15 * almath.TO_RAD, width_yaw, width_right, hand_closed]]
        self.angles = [angles_top, angles_middle, angles_bottom]
        self.return_angle = [40 * almath.TO_RAD, 90 * almath.TO_RAD, 8 * almath.TO_RAD, -58 * almath.TO_RAD, hand_closed]
        self.return_angleR = [-40 * almath.TO_RAD, 90 * almath.TO_RAD, 8 * almath.TO_RAD, 58 * almath.TO_RAD, hand_closed]
        self.fractionMaxSpeed = 0.2
        rest_position(self.session)

    def point_to_position(self, x, y):
        if y == 2:
            self.motion_service.setStiffnesses("RHand", 1.0)
            self.motion_service.setStiffnesses("RArm", 1.0)
            self.motion_service.setAngles(self.namesR, self.angles[x][y], self.fractionMaxSpeed)
            self.motion_service.setAngles("RHand", 1.0, self.fractionMaxSpeed)
        else:
            self.motion_service.setStiffnesses("LHand", 1.0)
            self.motion_service.setStiffnesses("LArm", 1.0)
            self.motion_service.setAngles(self.namesL, self.angles[x][y], self.fractionMaxSpeed)
            self.motion_service.setAngles("LHand", 1.0, self.fractionMaxSpeed)

        time.sleep(3.0)
        rest_position(self.session)


if __name__ == '__main__':
    ip = "192.168.1.101"
    connection_url = ip + ":9559"
    app = qi.Application(["--qi-url=" + connection_url])
    app.start()
    session = app.session
    print("started")
    mm = MoveMotors(session)
    print("start 0 0")
    #mm.point_to_position(0, 1)
    #time.sleep(2)
    #mm.point_to_position(1, 1)
    #time.sleep(2)
    #mm.point_to_position(2, 1)
    print("finished")
