def rest_position(session):
    motion_service = session.service("ALMotion")
    posture_service = session.service("ALRobotPosture")
    posture_service.goToPosture("StandInit", 0.5)
    motion_service.setStiffnesses("Head", 1.0)
    names = ["HeadYaw", "HeadPitch"]
    angles = [0., 0.]
    times = [1., 1.]
    is_absolute = True
    motion_service.angleInterpolation(names, angles, times, is_absolute)
