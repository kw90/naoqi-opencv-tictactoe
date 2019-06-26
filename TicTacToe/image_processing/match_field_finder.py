import cv2
from image_optimizer import ImageOptimizer
from cv_basic_config_data import CVBasicConfigData


class MatchFieldFinder:

    def __init__(self):
        self.__img_optimizer = ImageOptimizer()
        self.__cv_basic_conf = CVBasicConfigData()
        self.__img_cnt = 0

    def get_match_filed_base_fields(self, image, img_cnt):
        self.__img_cnt = img_cnt

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.blur(gray, (2, 2))

        self.__img_optimizer.save_images_for_debug(gray, "gray" + str(img_cnt), self.__cv_basic_conf.debug)

        #gray = ImageOptimizer.transform_image_to_black_white(gray, 125)

        #self.__img_optimizer.save_images_for_debug(gray, "gray_binary" + str(img_cnt), self.__cv_basic_conf.debug)

        # detect edges in the image
        edged = cv2.Canny(gray, 150, 255)

        self.__img_optimizer.save_images_for_debug(edged, "canny" + str(img_cnt),  self.__cv_basic_conf.debug)

        # find contours (in the image

        contours = self.__find_contours(edged.copy(), cv2.RETR_LIST)
        return sorted(contours, key=cv2.contourArea, reverse=True)[:20]

    # Method to use the cv findContours method independent from cv version
    def __find_contours(self, source_image, mode, method=cv2.CHAIN_APPROX_SIMPLE, contours=None, hierarchy=None, offset=None):
        if str.find(self.__cv_basic_conf.cv_version_string, "3.4.") != -1:
            im2, contours, hierarchy = cv2.findContours(source_image, mode, method, contours, hierarchy, offset)
            self.__img_optimizer.save_images_for_debug(im2, "contours" + str(self.__img_cnt), self.__cv_basic_conf.debug)
        else:
            contours, hierarchy = cv2.findContours(source_image, mode, method)
        return contours
