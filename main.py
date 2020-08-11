# from ocr import OCR
from calc import Calc
# import cv2
from datetime import datetime

# start = datetime.now()
# e = Calc("zeta(2)")
# print(f"{e.string_eval()}")
# end = datetime.now()
# print("")
# print(f"Runtime: {((end-start).total_seconds()):.2f} seconds")

sentinel = False

while not sentinel:

	inp = input("Input an equation:\n")

	try:
		start = datetime.now()
		e = Calc(inp)
		out = e.string_eval()
		end = datetime.now()
		td = end - start

		print(f"Output: {out}        Runtime: {td.total_seconds():.2f} seconds")
	except Exception as e:
		print(f"Calculation failed. {e}")

	cont = ""

	while cont.upper() not in ("Y", "N"):
		cont = input("Would you like to continue? (Y/N) ")

	if cont.upper() == "N":
		sentinel = True