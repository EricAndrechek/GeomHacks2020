from pyzbar.pyzbar import decode
import cv2

print(decode(cv2.imread('img-resources/work.JPG')))