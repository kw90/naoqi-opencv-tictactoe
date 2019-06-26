import cv2


class CVBasicConfigData:

    def __init__(self):
        self.__DEBUG = True
        self.__cv_version = cv2.getVersionString()

    @property
    def cv_version_string(self):
        return self.__cv_version

    @property
    def debug(self):
        return self.__DEBUG
