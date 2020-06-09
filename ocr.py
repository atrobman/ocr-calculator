from imutils.object_detection import non_max_suppression
import numpy as np
import cv2

class OCR:
	
	def __init__(self):
		pass

	def read_image(self, inp):
		"""
		inputs: image filepath (as a string)
		outputs: list of strings of detected 
		"""
		img = cv2.imread(inp)