from ocr import OCR
from calc import Calc
import cv2

x = OCR(None, 0.5)
x.read_image("./images/sign.jpg")

cv2.waitKey(0) #press any key to end program
cv2.destroyAllWindows()