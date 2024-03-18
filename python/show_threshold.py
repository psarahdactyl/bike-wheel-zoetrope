import numpy as np
import cv2

# kernel for erosion and dilation
kernel = np.ones((2, 2), np.uint8)

def thresholding(img):
    # convert frame image to greyscale, and then blur
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (9, 9), 0)

    # binary threshold on the frame
    re, thr = cv2.threshold(blur, 250, 255, cv2.THRESH_BINARY)

    # erosion and then dilation on the frame
    opened = cv2.morphologyEx(thr, cv2.MORPH_OPEN, kernel)

    return opened

cap = cv2.VideoCapture(0)
while True:
    _, frame = cap.read()

    # process the frame
    thresh = thresholding(frame)

    cv2.imshow('thresh', thresh)
    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()