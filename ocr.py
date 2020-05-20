from imutils.object_detection import non_max_suppression
import numpy as np
import cv2

class OCR:
	
	def __init__(self, min_confidence=0.5):

		self.net = cv2.dnn.readNet("frozen_east_text_detection.pb")
		self.min_confidence = min_confidence

	def read_image(self, inp):
		"""
		inputs: image filepath (as a string)
		outputs: list of strings of detected 
		"""
		img = cv2.imread(inp)
		orig = img.copy()

		M, N = img.shape[:2]
		rM = M / 320
		rN = N / 320

		img = cv2.resize(img, (320, 320))
		M, N = img.shape[:2]

		layerNames = ["feature_fusion/Conv_7/Sigmoid", "feature_fusion/concat_3"]
		blob = cv2.dnn.blobFromImage(img, 1.0, (N, M), (123.68, 116.78, 103.94), swapRB=True, crop=False)
		self.net.setInput(blob)
		scores, geometry = self.net.forward(layerNames)

		# show timing information on text prediction
		# print("[INFO] text detection took {:.6f} seconds".format(end - start))

		# grab the number of rows and columns from the scores volume, then
		# initialize our set of bounding box rectangles and corresponding
		# confidence scores
		(numRows, numCols) = scores.shape[2:4]
		rects = []
		confidences = []

		# loop over the number of rows
		for y in range(0, numRows):
			# extract the scores (probabilities), followed by the geometrical
			# data used to derive potential bounding box coordinates that
			# surround text
			scoresData = scores[0, 0, y]
			xData0 = geometry[0, 0, y]
			xData1 = geometry[0, 1, y]
			xData2 = geometry[0, 2, y]
			xData3 = geometry[0, 3, y]
			anglesData = geometry[0, 4, y]

			# loop over the number of columns
			for x in range(0, numCols):
				# if our score does not have sufficient probability, ignore it
				if scoresData[x] < self.min_confidence:
					continue

				# compute the offset factor as our resulting feature maps will
				# be 4x smaller than the input image
				(offsetX, offsetY) = (x * 4.0, y * 4.0)

				# extract the rotation angle for the prediction and then
				# compute the sin and cosine
				angle = anglesData[x]
				cos = np.cos(angle)
				sin = np.sin(angle)

				# use the geometry volume to derive the width and height of
				# the bounding box
				h = xData0[x] + xData2[x]
				w = xData1[x] + xData3[x]

				# compute both the starting and ending (x, y)-coordinates for
				# the text prediction bounding box
				endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
				endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
				startX = int(endX - w)
				startY = int(endY - h)

				# add the bounding box coordinates and probability score to
				# our respective lists
				rects.append((startX, startY, endX, endY))
				confidences.append(scoresData[x])

		# apply non-maxima suppression to suppress weak, overlapping bounding
		# boxes
		boxes = non_max_suppression(np.array(rects), probs=confidences)

		# loop over the bounding boxes
		for (startX, startY, endX, endY) in boxes:
			# scale the bounding box coordinates based on the respective
			# ratios
			startX = int(startX * rN)
			startY = int(startY * rM)
			endX = int(endX * rN)
			endY = int(endY * rM)

			# draw the bounding box on the image
			cv2.rectangle(orig, (startX, startY), (endX, endY), (0, 255, 0), 2)

		# show the output image
		cv2.imshow("Text Detection", orig)
		# cv2.waitKey(0)