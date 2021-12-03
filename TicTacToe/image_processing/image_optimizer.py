import cv2


class ImageOptimizer:
    def __init__(self):
        self.__img_path = "debug_images/images_debug_"

    @staticmethod
    def transform_image_to_black_white(image, threshold):
        for i in range(0, len(image[0])):
            for j in range(0, len(image)):
                if image[j][i] > threshold:
                    image[j][i] = 255
                else:
                    image[j][i] = 0
        return image

    def save_images_for_debug(self, image, name, debug=True):
        if debug:
            cv2.imwrite(self.__img_path + name + ".jpg", image)
