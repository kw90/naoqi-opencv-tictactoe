import cv2
import numpy as np
import paramiko
import qi
import time
import os
from image_processing import ImageOptimizer
from image_processing import MatchFieldFinder


class DetectBoard:

    def __init__(self):
        self.__DEBUG = True
        self.__AVOID_LOOP = False
        self.__cv_version = cv2.getVersionString()
        self.__img_counter = 0
        self.__img_optimizer = ImageOptimizer()
        self.__match_filed_finder = MatchFieldFinder()
        self.__red_range_lower = np.array((17, 15, 60), dtype="uint8")
        self.__red_range_upper = np.array((50, 56, 255), dtype="uint8")
        self.__blue_range_lower = np.array((86, 31, 4), dtype="uint8")
        self.__blue_range_upper = np.array((220, 88, 50), dtype="uint8")
        self.__red_range_hsv_lower_1 = np.array([0, 50, 50])
        self.__red_range_hsv_lower_2 = np.array([150, 50, 50])
        self.__red_range_hsv_upper_1 = np.array([10, 255, 255])
        self.__red_range_hsv_upper_2 = np.array([190, 255, 255])
        self.__blue_range_hsv_lower = np.array([100, 70, 50])
        self.__blue_range_hsv_upper = np.array([130, 255, 255])

        self.__ip = os.getenv('PEPPER_IP')
        self.__pw = os.getenv('PEPPER_PW')

    def get_picture_board(self):
        matchfield = [[0 for x in range(3)] for y in range(3)]
        matchfield[0][0] = -1

        local_path = '../example-images/boards/board_9.jpg'

        while matchfield[0][0] == -1:
            matchfield = self.get_matchfield(local_path)
            if matchfield[0][0] == -1:
                print('Found nothing')
            else:
                print("found something")
                if self.__AVOID_LOOP:
                    matchfield[0][0] = -1    # avoid end loop

        self.__img_counter += 1000
        return self.rotate_clockwise(matchfield)

    def get_board(self, session):
        matchfield = [[0 for x in range(3)] for y in range(3)]
        matchfield[0][0] = -1

        camera = session.service("ALPhotoCapture")
        camera.setCameraID(0)
        path = "/home/nao/recordings/cameras/"
        fileName = "board.jpg"
        local_path = './pictures/board.jpg'

        while matchfield[0][0] == -1:
            camera.takePicture(path, fileName)

            transport = paramiko.Transport((self.__ip, 22))
            transport.connect(username='nao', password=self.__pw)
            sftp = paramiko.SFTPClient.from_transport(transport)
            sftp.get(path + fileName, local_path)
            sftp.close()
            transport.close()

            matchfield = self.get_matchfield(local_path)

            if matchfield[0][0] == -1:
                print('Found nothing')
            else:
                print("found something")
                if self.__AVOID_LOOP:
                    matchfield[0][0] = -1    # avoid end loop

        self.__img_counter += 1000
        return self.rotate_clockwise(matchfield)

    def get_matchfield(self, image_path):
        matchfield = [[0 for x in range(3)] for y in range(3)]

        image = cv2.imread(image_path)
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        test_image1 = image.copy()
        contours = self.__match_filed_finder.get_match_filed_base_fields(image, self.__img_counter)
        if cv2.contourArea(contours[18]) < 5000:
            matchfield[0][0] = -1
            return matchfield

        cv2.drawContours(image, contours, -1, (0, 255, 0), 3)
        self.__img_optimizer.save_images_for_debug(image, "piccont" + str(self.__img_counter), True)

        self.__img_counter += 1

        centers = []
        last_dimensions = []
        for contour in contours:
            # approximate the contour
            peri = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * peri, True)

            # if the approximated contour has four points its a rectangle
            if len(approx) == 4:
                (x, y, w, h) = cv2.boundingRect(approx)
                if h == 0:
                    h = 0.01
                aspect_ratio = w / float(h)
                # check if the rectangle is a square
                if 0.85 <= aspect_ratio <= 1.2:
                    if w >= 20 and h >= 20:
                        if not self.is_a_duplicate(last_dimensions, (x, y, w, h)):
                            moments = cv2.moments(approx)
                            m00 = moments['m00']
                            if m00 == 0:
                                m00 = 0.05

                            # get the center of the square
                            cx = int(moments['m10'] / m00)
                            cy = int(moments['m01'] / m00)
                            centers.append((cx, cy, x, y, w, h))
                            last_dimensions.append((x, y, w, h))

        biggest = (0, 0, 0, 0, 0, 0)
        for center in centers:
            if center[4] > biggest[4]:
                biggest = center
        if biggest != (0, 0, 0, 0, 0, 0):
            centers.remove(biggest)

        if len(centers) != 9:
            matchfield[0][0] = -1
            return matchfield

        first_row = []
        second_row = []
        third_row = []

        smallest_y = centers[0][1]
        biggest_y = centers[0][1]

        for center in centers:
            if center[1] < smallest_y:
                smallest_y = center[1]
            elif center[1] > biggest_y:
                biggest_y = center[1]

        offest = 20
        for center in centers:
            if (center[1] + offest) >= smallest_y >= (center[1] - offest):
                first_row.append(center)
            elif (center[1] + offest) >= biggest_y >= (center[1] - offest):
                third_row.append(center)
            else:
                second_row.append(center)

        first_row = sorted(first_row, key=lambda entry: entry[2])
        second_row = sorted(second_row, key=lambda entry: entry[2])
        third_row = sorted(third_row, key=lambda entry: entry[2])

        # find the colors within the specified boundaries and apply
        # the mask
        mask1 = cv2.inRange(hsv, self.__red_range_hsv_lower_1, self.__red_range_hsv_upper_1)
        mask2 = cv2.inRange(hsv, self.__red_range_hsv_lower_2, self.__red_range_hsv_upper_2)
        mask = cv2.bitwise_or(mask1, mask2)

        target_red = cv2.bitwise_and(hsv, hsv, mask=mask)
        contours = self.find_contours(mask.copy(), cv2.RETR_CCOMP)

        last_dimensions = []
        for contour in contours:
            peri = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
            (x, y, w, h) = cv2.boundingRect(approx)
            if not self.is_in_range(last_dimensions, (x, y)):
                last_dimensions.append((x, y))

                x_point, y_point = self.get_squares(first_row, second_row, third_row, x, y)
                if x_point != 4:
                    matchfield[y_point][x_point] = 1

                cv2.drawMarker(test_image1, (x, y), (0, 0, 255), markerType=cv2.MARKER_CROSS, markerSize=15, line_type=cv2.LINE_AA)
                self.__img_optimizer.save_images_for_debug(target_red, "mask_red_fields" + str(self.__img_counter), self.__DEBUG)
                self.__img_optimizer.save_images_for_debug(test_image1, "piccont_fields" + str(self.__img_counter), self.__DEBUG)


        # find the colors within the specified boundaries and apply
        # the mask
        mask = cv2.inRange(hsv, self.__blue_range_hsv_lower, self.__blue_range_hsv_upper)

        target_blue = cv2.bitwise_and(hsv, hsv, mask=mask)

        contours = self.find_contours(mask.copy(), cv2.RETR_CCOMP)

        last_dimensions = []
        for contour in contours:
            peri = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
            (x, y, w, h) = cv2.boundingRect(approx)
            if not self.is_in_range(last_dimensions, (x, y)):
                last_dimensions.append((x, y))

                x_point, y_point = self.get_squares(first_row, second_row, third_row, x, y)
                if x_point != 4:
                    matchfield[y_point][x_point] = 2

                cv2.drawMarker(test_image1, (x, y), (255, 0, 0), markerType=cv2.MARKER_CROSS,
                               markerSize=15, line_type=cv2.LINE_AA)
                self.__img_optimizer.save_images_for_debug(target_blue, "mask_blue_fields_2_" + str(self.__img_counter), self.__DEBUG)
                self.__img_optimizer.save_images_for_debug(test_image1, "piccont_fields_2_" + str(self.__img_counter), self.__DEBUG)

        # cv2.imshow("Image", image)

        return matchfield

    # Method to use the cv findContours method independent from cv version
    def find_contours(self, source_image, mode, method=cv2.CHAIN_APPROX_SIMPLE, contours=None, hierarchy=None, offset=None):
        if str.find(self.__cv_version, "3.4.") != -1:
            im2, contours, hierarchy = cv2.findContours(source_image, mode, method, contours, hierarchy, offset)
            self.__img_optimizer.save_images_for_debug(im2, "contours" + str(self.__img_counter), False)
        else:
            contours, hierarchy = cv2.findContours(source_image, mode, method)
        return contours

    def get_squares(self, first_row, second_row, third_row, x, y):
        x_point = 0
        y_point = 0
        for square in first_row:
            if square[2] <= x <= (square[2] + square[4]) and square[3] <= y <= (square[3] + square[5]):
                return x_point, y_point
            x_point += 1
        x_point = 0
        y_point += 1
        for square in second_row:
            if square[2] <= x <= (square[2] + square[4]) and square[3] <= y <= (square[3] + square[5]):
                return x_point, y_point
            x_point += 1
        x_point = 0
        y_point += 1
        for square in third_row:
            if square[2] <= x <= (square[2] + square[4]) and square[3] <= y <= (square[3] + square[5]):
                return x_point, y_point
            x_point += 1
        return 4, 4

    def is_a_duplicate(self, last_dimensions, (x, y, w, h)):
        offset = 3
        for lastDimension in last_dimensions:
            if (lastDimension[0] + offset) >= x >= (lastDimension[0] - offset) and (lastDimension[1] + offset) >= y >= (
                    lastDimension[1] - offset) and (lastDimension[2] + offset) >= w >= (lastDimension[2] - offset) and (
                    lastDimension[3] + offset) >= h >= (lastDimension[3] - offset):
                return True
        return False

    def is_in_range(self, last_dimensions, (x, y)):
        offset = 20
        for lastDimension in last_dimensions:
            if (lastDimension[0] + offset) >= x >= (lastDimension[0] - offset) and (lastDimension[1] + offset) >= y >= (
                    lastDimension[1] - offset):
                return True
        return False

    def rotate_clockwise(self, matrix):
        for x in range(3):
            temp = matrix[x][0]
            matrix[x][0] = matrix[x][2]
            matrix[x][2] = temp
        return matrix


if __name__ == '__main__':
    detect_board = DetectBoard()
    cv2_version = cv2.getVersionString()
    if str.find(cv2_version, "3.4.") != -1:
        print("Using opencv version ", cv2_version)

    connection_url = os.getenv('PEPPER_IP')+":9559"
    app = qi.Application(["--qi-url=" + connection_url])
    app.start()
    session = app.session

    # local testing pipeline
    # board = detect_board.get_picture_board()
    # detect board on pepper
    board = detect_board.get_board(session)
    print(board)

