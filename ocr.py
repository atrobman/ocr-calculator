from imutils.object_detection import non_max_suppression
import numpy as np
import cv2

class OCR:
	
	def __init__(self, east, min_confidence=0.5):

		self.east = east
		self.min_confidence = min_confidence
		self.image = None
	
	def read_image(self, inp):

		img = cv2.imread(inp)
		orig = img.copy()

		M, N = img.shape[:2]
		rM = M / 320
		rN = N / 320

		img = cv2.resize(img, (320, 320))

		cv2.imshow('test', img)
		cv2.imshow('orig', orig)