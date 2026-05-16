from cv2 import detail
import cv2
import numpy as np

mascara = np.zeros((400,400), dtype=np.uint8)
print(mascara)
cv2.circle(mascara, center=(200,200), radius=70, color=255, thickness=-1)
print(mascara)
cv2.imshow("Mascara", mascara)
cv2.waitKey(0)
cv2.destroyAllWindows()


circulos = cv2.HoughCircles(
    mascara,
    cv2.HOUGH_GRADIENT,
    dp=1,
    minDist=50,
    param1=50,
    param2=10,
    minRadius=5,
    maxRadius=100
)

print("Círculos encontrados:", circulos)