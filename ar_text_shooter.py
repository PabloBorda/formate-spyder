# USAGE
# python ar_text_shooter.py

# import the necessary packages
import numpy
from PIL import ImageGrab
from imutils.object_detection import non_max_suppression
from subprocess import call
import PIL

import numpy as np
import pytesseract
import argparse
import cv2
import math
import time
import json
import re
import io
import pyautogui



class ARTextShooter():
    def __init__(self):
        pytesseract.pytesseract.tesseract_cmd = r'tesseract'

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

                # extract the rotation angle for the prediction and
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



    def shoot_around_mouse(self,window):


        rows_per_screen = 8
        screenWidth, screenHeight = pyautogui.size()  # Get the size of the primary monitor.

        def to_global_coordinates(button_rect, mouse_x=None, mouse_y=None):
            row_height = int(screenHeight/rows_per_screen)
            current_row_number = int(screenHeight/mouse_y)
            previous_rows_sum_height = int(current_row_number*row_height)
            button_rect[0][1] = button_rect[0][1] + previous_rows_sum_height


            return button_rect;

        def row_number_to_global_coordinates(rownumber):
            row_height_in_pixels = screenHeight/rows_per_screen
            return (0,row_height_in_pixels*rows_per_screen)


        while True:
            currentMouseX, currentMouseY = pyautogui.position()  # Get the XY position of the mouse.
            print("Mouse position:" + str(currentMouseX) + "," + str(currentMouseY))
            screen_row_number = int(currentMouseY/(screenHeight/rows_per_screen))     # We divide the screen in 8 rows and have priority to update the row where the mouse is present and the one before and the one after
            print("Screen row number: "+str(screen_row_number))
            area_around_mouse_width = screenWidth*2
            area_around_mouse_height = (screenHeight*2/rows_per_screen)

            area_around_mouse_centered_position = row_number_to_global_coordinates(screen_row_number)
            area_around_mouse_bbox = (area_around_mouse_centered_position[0], area_around_mouse_centered_position[1], area_around_mouse_width,area_around_mouse_height)
            image_around_mouse = pyautogui.screenshot(region=area_around_mouse_bbox)
            # image_around_mouse.show()
            start = time.time()
            content_to_buttonize = self.shoot(image=image_around_mouse)
            content_to_buttonize_parsed_json = json.loads(content_to_buttonize)
            content_to_buttonize_parsed_json_global_coordinates = list(map(lambda button_rect: to_global_coordinates(button_rect=button_rect,mouse_x=currentMouseX, mouse_y=currentMouseY), content_to_buttonize_parsed_json))
            end = time.time()
            print("Time OCR: " + str(end - start))
            window.buttonize(content_to_buttonize)
            #cv2.imshow("Text Detection", image_around_mouse)
            #cv2.waitKey(0)

    def shoot(self, image=None, rects=None):
        # load the input image and grab the image dimensions
        if image is None:
            im = ImageGrab.grab()
        else:
            im = image

        image_bytes_array = numpy.array(im).copy()

        # image = cv2.imdecode(np.fromstring(image_bytes_array, np.uint8), cv2.IMREAD_COLOR)

        image = cv2.cvtColor(image_bytes_array, cv2.IMREAD_COLOR)

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

        # load the pre-trained EAST text detector
        # print("[INFO] loading EAST text detector...")
        net = cv2.dnn.readNet('frozen_east_text_detection.pb')

        # construct a blob from the image and then perform a forward pass of
        # the model to obtain the two output layer sets
        blob = cv2.dnn.blobFromImage(image, 1.0, (W, H),
                                     (123.68, 116.78, 103.94), swapRB=True, crop=False)
        net.setInput(blob)
        (scores, geometry) = net.forward(layerNames)

        # decode the predictions, then  apply non-maxima suppression to
        # suppress weak, overlapping bounding boxes
        (rects, confidences) = self.decode_predictions(scores, geometry)
        boxes = non_max_suppression(np.array(rects), probs=confidences)
        # print(boxes)
        # initialize the list of results
        results = []

        # loop over the bounding boxes
        for (startX, startY, endX, endY) in boxes:
            # scale the bounding box coordinates based on the respective
            # ratios
            startX = int(startX * rW)
            startY = int(startY * rH)
            endX = int(endX * rW)
            endY = int(endY * rH)

            # in order to obtain a better OCR of the text we can potentially
            # apply a bit of padding surrounding the bounding box -- here we
            # are computing the deltas in both the x and y directions
            dX = 2
            dY = 4

            # apply padding to each side of the bounding box, respectively
            startX = max(0, startX - dX)
            startY = max(0, startY - dY)
            endX = min(origW, endX + (dX * 2))
            endY = min(origH, endY + (dY * 2))

            # extract the actual padded ROI
            roi = orig[startY:endY, startX:endX]

            # in order to apply Tesseract v4 to OCR text we must supply
            # (1) a language, (2) an OEM flag of 4, indicating that the we
            # wish to use the LSTM neural net model for OCR, and finally
            # (3) an OEM value, in this case, 7 which implies that we are
            # treating the ROI as a single line of text

            text = pytesseract.image_to_string(roi, config='-l eng --oem 1 --psm 7')
            # add the bounding box coordinates and OCR'd text to the list
            # of results
            results.append(((startX, startY, endX, endY), text))
            # print(str(results))

        # sort the results bounding box coordinates from top to bottom
        results = sorted(results, key=lambda r: r[0][1])
        output = orig.copy()
        # print("[startX,startY,endX,endY]=[Text]\n")
        # loop over the results
        # print(json.dumps(results).replace("\n\f", ""))
        out = "["

        for ((startX, startY, endX, endY), text) in results:
            # display the text OCR'd by Tesseract
            normalized_text = re.sub(r'\W+', '', text)
            out = out + "[[{},{},{},{}],{}],".format(startX, startY, endX, endY, '"' + normalized_text + '"')

            # strip out non-ASCII text so we can draw the text on the image
            # using OpenCV, then draw the text and a bounding box surrounding
            # the text region of the input image
            # text = "".join([c if ord(c) < 128 else "" for c in text]).strip()
            # output = orig.copy()
            # cv2.rectangle(output, (startX, startY), (endX, endY),
            #	(0, 255, 0), 1)
            # cv2.putText(output, text, (startX, startY + 40),
            #	cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1)

            # show the output image
        out = out[:-1]
        out = out + "]"
        # print(out)
        return out
# cv2.imshow("Text Detection", output)
# cv2.waitKey(0)
