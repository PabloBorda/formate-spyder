import cv2


class FormateReadNeuralNet:
    net = cv2.dnn.readNet('frozen_east_text_detection.pb')