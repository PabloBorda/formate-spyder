from datetime import datetime

from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal, QThread
import numpy
from PIL import ImageGrab
from imutils.object_detection import non_max_suppression
import numpy as np
import pytesseract
import cv2
import math
import time
import json
import re
import pyautogui
import sys

from com_formate_computervision.FormateReadNeuralNet import FormateReadNeuralNet
from com_formate_glass.FormateRect import FormateRect
from com_formate_logs.FormateLogger import FormateLogger
from com_formate_logs.FormateLogEntry import FormateLogEntry

class FormateTesseract(QThread):

    net = FormateReadNeuralNet.net
    
    new_element_detected = pyqtSignal(FormateRect)

    def __init__(self, glass, parent=None,rect=None):
        super().__init__()
        pytesseract.pytesseract.tesseract_cmd = r'tesseract'
        self.running_shoot = True
        self.image = rect.im
        self.rect_to_process = rect
        self.elements_found = []
       


    def decode_predictions(self, scores, geometry):
        # grab the number of rows and columns from the scores volume, then
        # initialize our set of bounding box rectangles and corresponding
        # confidence scores
        (numRows, numCols) = scores.shape[2:4]
        rects = []
        confidences = []

        # loop over the number of rows
        for y in range(0, numRows):
            # extract the scores (probabilities), followed by the
            # geometrical data used to derive potential bounding box
            # coordinates that surround text
            scoresData = scores[0, 0, y]
            xData0 = geometry[0, 0, y]
            xData1 = geometry[0, 1, y]
            xData2 = geometry[0, 2, y]
            xData3 = geometry[0, 3, y]
            anglesData = geometry[0, 4, y]

            # loop over the number of columns
            for x in range(0, numCols):
                # if our score does not have sufficient probability,
                # ignore it
                if scoresData[x] < 0.5:  # 0.5 is min confidence, confidence range is 0 ~ 1.
                    continue

                # compute the offset factor as our resulting feature
                # maps will be 4x smaller than the input image
                (offsetX, offsetY) = (x * 4.0, y * 4.0)

                # etract the rotation angle for the prediction and
                # then compute the sin and cosine
                angle = anglesData[x]
                cos = np.cos(angle)
                sin = np.sin(angle)

                # use the geometry volume to derive the width and height
                # of the bounding box
                h = xData0[x] + xData2[x]
                w = xData1[x] + xData3[x]

                # compute both the starting and ending (x, y)-coordinates
                # for the text prediction bounding box
                endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
                endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
                startX = int(endX - w)
                startY = int(endY - h)

                # add the bounding box coordinates and probability score
                # to our respective lists
                rects.append((startX, startY, endX, endY))
                confidences.append(scoresData[x])

            # return a tuple of the bounding boxes and associated confidences
        return (rects, confidences)

    # def optimize_image_for_ocr(self,image):

    def shoot_around_mouse(self, glass):

        rows_per_screen = 8
        screenWidth, screenHeight = pyautogui.size()  # Get the size of the primary monitor.

        def to_global_coordinates(button_rect, mouse_x=None, mouse_y=None):
            row_height = int(screenHeight / rows_per_screen)
            current_row_number = int(screenHeight / mouse_y)
            previous_rows_sum_height = int(current_row_number * row_height)
            button_rect[0][1] = button_rect[0][1] + previous_rows_sum_height
            return button_rect

        def row_number_to_global_coordinates(rownumber):
            row_height_in_pixels = screenHeight / rows_per_screen
            return (0, row_height_in_pixels * rows_per_screen)

        while True:
            currentMouseX, currentMouseY = pyautogui.position()  # Get the XY position of the mouse.
            #print("Mouse position:" + str(currentMouseX) + "," + str(currentMouseY))
            screen_row_number = int(currentMouseY / (
                    screenHeight / rows_per_screen))  # We divide the screen in 8 rows and have priority to update the row where the mouse is present and the one before and the one after
            #print("Screen row number: " + str(screen_row_number))
            area_around_mouse_width = screenWidth * 2
            area_around_mouse_height = (screenHeight * 2 / rows_per_screen)

            area_around_mouse_centered_position = row_number_to_global_coordinates(screen_row_number)
            area_around_mouse_bbox = (
                area_around_mouse_centered_position[0], area_around_mouse_centered_position[1], area_around_mouse_width,
                area_around_mouse_height)
            image_around_mouse = pyautogui.screenshot(region=area_around_mouse_bbox)
            # image_around_mouse.show()
            start = time.time()
            content_to_buttonize = self.shoot(image=image_around_mouse)
            content_to_buttonize_parsed_json = json.loads(content_to_buttonize)
            content_to_buttonize_parsed_json_global_coordinates = list(map(
                lambda button_rect: to_global_coordinates(button_rect=button_rect, mouse_x=currentMouseX,
                                                          mouse_y=currentMouseY), content_to_buttonize_parsed_json))
            end = time.time()
            #print("Time OCR: " + str(end - start))
            glass.buttonize(content_to_buttonize)

    def shoot(self, image=None):
        self.running_shoot = True
        #   print("TESSERACT THREAD: Execute shoot from FormateTesseract")
        im = image
        image_bytes_array = numpy.array(im).copy()
        # image = cv2.imdecode(np.fromstring(image_bytes_array, np.uint8), cv2.IMREAD_GRAYSCALE)

        image = cv2.cvtColor(image_bytes_array, cv2.COLOR_GRAY2BGR)

        orig = image.copy()

        (origH, origW) = image.shape[:2]
        # print(origH, origW)
        # set the new width and height and then determine the ratio in change
        # for both the width and height
        # (newW, newH) = (args["width"], args["height"])
        (newW, newH) = (math.ceil(origW / 32) * 32, math.ceil(origH / 32) * 32)
        rW = origW / float(newW)
        rH = origH / float(newH)

        # resize the image and grab the new image dimensions
        image = cv2.resize(image, (newW, newH))
        (H, W) = image.shape[:2]

        # define the two output layer names for the EAST detector model that
        # we are interested -- the first is the output probabilities and the
        # second can be used to derive the bounding box coordinates of text
        layerNames = [
            "feature_fusion/Conv_7/Sigmoid",
            "feature_fusion/concat_3"]

        # construct a blob from the image and then perform a forward pass of
        # the model to obtain the two output layer sets
        blob = cv2.dnn.blobFromImage(image, 1.0, (W, H),
                                     (123.68, 116.78, 103.94), swapRB=True, crop=False)
        self.net.setInput(blob)
        (scores, geometry) = self.net.forward(layerNames)

        # decode the predictions, then  apply non-maxima suppression to
        # suppress weak, overlapping bounding boxes
        (rects, confidences) = self.decode_predictions(scores, geometry)
        boxes = non_max_suppression(np.array(rects), probs=confidences)
        # print(boxes)
        # initialize the list of results

        # loop over the bounding boxes
        for (startX, startY, endX, endY) in boxes:
            # scale the bounding box coordinates based on the respective
            # ratios
            startX = int(startX * rW)
            startY = int(startY * rH)
            endX = int(endX * rW)
            endY = int(endY * rH)
            dX = 2
            dY = 4

            # apply padding to each side of the bounding box, respectively
            startX = max(0, startX - dX)
            startY = max(0, startY - dY)
            endX = min(origW, endX + (dX * 2))
            endY = min(origH, endY + (dY * 2))

            # extract the actual padded ROI
            roi = orig[startY:endY, startX:endX]
            
            text_to_render = FormateRect(startX, startY, endX, endY, "text_to_detect", self.get_text_at_position(roi))
            self.elements_found.append(text_to_render)
            self.new_element_detected.emit(text_to_render)
            FormateLogger.log(FormateLogEntry(thread_name="FormateTesseract.py",description="Decode text from rect position",rect_involved=str(FormateRect(str(startX),str(startY),str(endX),str(endY)))))
        self.running_shoot = False
        return self.elements_found

    def normalize_text(self, str):
        return re.sub(r'\W+', '', str)

    def get_text_at_position(self, roi):
        start = time.time()
        text = pytesseract.image_to_string(roi, config='-l eng --oem 1 --psm 7')
        end = time.time()
        FormateLogger.log(FormateLogEntry(thread_name="FormateTesseract.py",description="Decode text from rect",processing_time=str(end - start)))
        return text

    def is_running_shoot(self):
        return self.running_shoot

    def run(self):
        self.shoot(image=self.formate_rect.im)
            

