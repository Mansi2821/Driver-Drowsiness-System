from scipy.spatial import distance as dist
from imutils.video import VideoStream
from imutils import face_utils
from threading import Thread
import numpy as np
import pygame
import argparse
import imutils
import time
import dlib
import cv2
import matplotlib.pyplot as plt

pygame.init()

def alarm(msg):
    global alarm_status
    global alarm_status2
    global saying

    while alarm_status:
        print('call')
        alert_sound = pygame.mixer.Sound(r"C:\Users\krati\example_WAV_1MG.wav")
        try:
            alert_sound.play()
        except pygame.error as e:
            print("Error playing sound:", e)

    if alarm_status2:
        print('call')
        saying = True
        alert_sound = pygame.mixer.Sound(r"C:\Users\krati\mixkit-classic-alarm-995.wav")
        try:
            alert_sound.play()
        except pygame.error as e:
            print("Error playing sound:", e)
        saying = False

def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])

    ear = (A + B) / (2.0 * C)

    return ear

def final_ear(shape):
    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

    leftEye = shape[lStart:lEnd]
    rightEye = shape[rStart:rEnd]

    leftEAR = eye_aspect_ratio(leftEye)
    rightEAR = eye_aspect_ratio(rightEye)

    ear = (leftEAR + rightEAR) / 2.0
    return (ear, leftEye, rightEye)

def lip_distance(shape):
    top_lip = shape[50:53]
    top_lip = np.concatenate((top_lip, shape[61:64]))

    low_lip = shape[56:59]
    low_lip = np.concatenate((low_lip, shape[65:68]))

    top_mean = np.mean(top_lip, axis=0)
    low_mean = np.mean(low_lip, axis=0)

    distance = abs(top_mean[1] - low_mean[1])
    return distance

ap = argparse.ArgumentParser()
ap.add_argument("-w", "--webcam", type=int, default=0,
                help="index of webcam on system")
args = vars(ap.parse_args())

EYE_AR_THRESH = 0.3
EYE_AR_CONSEC_FRAMES = 30
YAWN_THRESH = 20
alarm_status = False
alarm_status2 = False
saying = False
COUNTER = 0

print("-> Loading the predictor and detector...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

print("-> Starting Video Stream")
vs = VideoStream(src=args["webcam"]).start()
time.sleep(1.0)

ear_values = []

# Initialize a window to display the video stream and graph
cv2.namedWindow("Video Stream and EAR Graph", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Video Stream and EAR Graph", 800, 600)

while True:
    frame = vs.read()
    frame = imutils.resize(frame, width=450)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    rects = detector(gray, 0)

    for rect in rects:
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)
        eye = final_ear(shape)
        ear = eye[0]

        ear_values.append(ear)

        leftEyeHull = cv2.convexHull(eye[1])
        rightEyeHull = cv2.convexHull(eye[2])
        cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

        distance = lip_distance(shape)
        lip = shape[48:60]
        cv2.drawContours(frame, [lip], -1, (0, 255, 0), 1)

        if ear < EYE_AR_THRESH:
            COUNTER += 1

            if COUNTER >= EYE_AR_CONSEC_FRAMES:
                if alarm_status == False:
                    alarm_status = True
                    t = Thread(target=alarm, args=('wake up sir',))
                    t.daemon = True
                    t.start()

                cv2.putText(frame, "DROWSINESS ALERT!", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        else:
            COUNTER = 0
            alarm_status = False

        if distance > YAWN_THRESH:
            cv2.putText(frame, "Yawn Alert", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            if alarm_status2 == False and saying == False:
                alarm_status2 = True
                t = Thread(target=alarm, args=('take some fresh air sir',))
                t.daemon = True
                t.start()
        else:
            alarm_status2 = False

        cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, "YAWN: {:.2f}".format(distance), (300, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # Plot the EAR values
    frame_numbers = list(range(1, len(ear_values) + 1))  # Generate frame numbers
    plt.plot(frame_numbers, ear_values)
    plt.xlabel('Frame Number')
    plt.ylabel('Eye Aspect Ratio (EAR)')
    plt.title('Eye Aspect Ratio Over Time')
    plt.grid(True)

    # Convert the matplotlib figure to an OpenCV image
    plot_img = plt.gcf()
    plot_img.canvas.draw()
    plot_img_cv = np.array(plot_img.canvas.renderer.buffer_rgba())
    plot_img_cv = cv2.cvtColor(plot_img_cv, cv2.COLOR_RGBA2BGR)

    # Resize the graph to match the height of the video frame
    frame_height, frame_width, _ = frame.shape
    plot_img_cv = cv2.resize(plot_img_cv, (frame_width, frame_height))

    # Combine the video frame and the graph
    combined_frame = np.hstack((frame, plot_img_cv))

    cv2.imshow("Video Stream and EAR Graph", combined_frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

pygame.quit()
cv2.destroyAllWindows()
vs.stop()
