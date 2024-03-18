import numpy as np
import cv2
from datetime import datetime
import time

cap = cv2.VideoCapture(0)
while True:
    _, frame = cap.read()

    # cv2.imshow('frame', frame)
    outfile = 'saved_images/%s.jpg' % ("zoetrope_cam" + str(datetime.now()))
    cv2.imwrite(outfile, frame)
    time.sleep(0.125)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()