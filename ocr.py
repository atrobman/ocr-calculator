from imutils.object_detection import non_max_suppression
import numpy as np
import cv2

class OCR:
	
	def __init__(self, min_confidence=0.5):

		self.net = cv2.dnn.readNet("./frozen_east_test_detection.pb")
		self.min_confidence = min_confidence
		self.image = None
		self.rescale = (0,0)

	def read_image(self, inp):

		img = cv2.imread(inp)
		orig = img.copy()

		M, N = img.shape[:2]
		rM = M / 320
		rN = N / 320
		self.rescale = (rM, rN)

		self.img = cv2.resize(img, (320, 320))