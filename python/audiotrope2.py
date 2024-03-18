import pymedia
import cv2
import numpy as np
import json
import glob
import serial
import random

serial_port = serial.Serial(port='COM3', baudrate=9600)

# kernel for erosion and dilation
kernel = np.ones((2, 2), np.uint8)

TOTAL_FRAMES = 16


def thresholding(img):
    # convert frame image to greyscale, and then blur
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (9, 9), 0)

    # binary threshold on the frame
    re, thr = cv2.threshold(blur, 250, 255, cv2.THRESH_BINARY)

    # erosion and then dilation on the frame
    opened = cv2.morphologyEx(thr, cv2.MORPH_OPEN, kernel)

    return opened


players = []
""" List to hold the pymedia Player instances for each key object."""

audio = []
""" List to store paths to all the necessary audio files. """

filename = raw_input('Please provide the full name of the calibration file: ')
with open(filename, 'r') as importfile:
    calib = json.load(importfile)

obj_num = len(calib)
""" Total number of calibrated objects. """
print(obj_num)

obj_coords = []
""" List to hold the coordinates of each "action object" in each frame. """

for obj in calib:

    obj_audio = [[]] * TOTAL_FRAMES

    for sound in calib[obj]['audio']:
        first_frame_index = int(sound[0]) - 1
        last_frame_index = int(sound[1])
        wav_path = sound[3]

        for i in range(first_frame_index, last_frame_index):
            obj_audio[i].append(wav_path)\

    audio.append(obj_audio)

    coords = []

    new_player = pymedia.Player()
    new_player.start()
    players.append(new_player)

    for frame in range(TOTAL_FRAMES):
        coords.append(calib[obj]['location'][str(frame)])

    obj_coords.append(coords)


current_frame = None
"""Variable to hold what the current frame is """

prev_frame = 0
""" Variable to hold what the previous frame was, set to 1 each time first frame is viewed """

prev_obj = None
""" Variable to hold the index of the previously illuminated object, if any """


cap = cv2.VideoCapture(1)
while cap.isOpened():
    _, frame = cap.read()

    # process the frame
    thresh = thresholding(frame)

    serial_code = serial_port.read(2)
    # serial_code = int(raw_input('1 for 1st frame, 2 for frame, 0 for no frame: '))

    obj_detected = False
    """ Variable to hold whether or not an "action" object is illuminated in the frame.
        Initially False, True if object detected. """

    current_obj = None
    """ Variable to hold the index of the current illuminated object, if any """

    if serial_code == "F1":
        current_frame = 1
        print('On frame 1.')
    elif serial_code == "FN":
        current_frame = prev_frame + 1
        print('On frame ' + str(current_frame) + '.')
    else:
        current_frame = None
        print('In-between frames.')

    if current_frame is not None:
        for i in range(obj_num):
            temp_frame = thresh[obj_coords[i][current_frame-1][0]:obj_coords[i][current_frame-1][1],
                                obj_coords[i][current_frame-1][2]:obj_coords[i][current_frame-1][3]]

            if 255 in temp_frame:
                obj_detected = True
                current_obj = i
                print('Detected object ' + str(current_obj))
                break

        # If no key objects are illuminated and a sound is currently playing, stop the sound
        if not obj_detected:
            print("No objects of interest are illuminated.")
            if prev_obj is not None:
                players[prev_obj].stopPlayback()
                print("Stopped playback for object " + str(prev_obj) + ".")
                current_obj = None

        else:
            if current_obj != prev_obj:
                # if there was an object detected in the previous frame, and it is not the same as the current object,
                # stop the playback of sound for the previous object
                if prev_obj is not None and players[prev_obj].isPlaying():
                    players[prev_obj].stopPlayback()
                    print("Stopped playback for object " + str(prev_obj) + ".")

                if audio[current_obj][current_frame-1]:
                    # play sound for detected object
                    players[current_obj].startPlayback(random.choice(audio[current_obj][current_frame-1]))
                    print("Playing audio for object " + str(current_obj) + ".")

            else:
                if not audio[current_obj][current_frame-1] and players[current_obj].isPlaying():
                    players[current_obj].stopPlayback()
                    print("Stopped playback for object " + str(current_obj) + ".")

                if set(audio[current_obj][current_frame - 1]) != set(audio[current_obj][prev_frame - 1]):

                    if players[current_obj].isPlaying():
                        players[current_obj].stopPlayback()
                        print("Stopped playback for object " + str(current_obj) + ".")

                    if audio[current_obj][current_frame - 1]:
                        players[current_obj].startPlayback(random.choice(audio[current_obj][current_frame-1]))

        prev_frame = current_frame
        prev_obj = current_obj

    # display frames and exit
    cv2.imshow('original frame', frame)
    # cv2.imshow('threshold frame', thresh)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
