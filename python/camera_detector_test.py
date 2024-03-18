import cv2
import serial

serial_port = serial.Serial(port='COM3', baudrate=9600)


cap = cv2.VideoCapture(1)  # video capture source camera (Here webcam of laptop)

count = 1

while cap.isOpened():

    serial_code = serial_port.read(2)

    ret, frame = cap.read()  # return a single frame in variable `frame`
    cv2.imshow('img1', frame)  # display the captured image
    if serial_code == "F1":  # detected first frame
        count = 1
        cv2.imwrite('frame' + str(count) + '.png', frame)
    elif serial_code == "F2":
        count += 1
        cv2.imwrite('frame' + str(count) + '.png', frame)

    if cv2.waitKey(1) == ord('q'):  # quit on pressing q
        cap.release()
        cv2.destroyAllWindows()
        break
