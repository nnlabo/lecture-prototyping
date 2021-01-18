import datetime
import os
import subprocess
import time
from line_notify_sender import LINENotifySender

import cv2
import dlib

detector = dlib.get_frontal_face_detector()

sender = LINENotifySender(access_token='pDp8OxWBdfzJvzzN7UTjs4zpww6vCjikjZIjoLAmS69')

def detect_face():
    """ Wait until faces detected using dlib """
    camera = cv2.VideoCapture(0)
    while True:
        _, frame = camera.read()
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results, _, _ = detector.run(frame_rgb, 0)
        for result in results:
            cv2.rectangle(frame_rgb, (result.left(), result.top()), (result.right(), result.bottom()), (0, 0, 255))
        cv2.imwrite('detected_image.jpg', frame_rgb)
        if results:
            break
    camera.release()
    return


def notify_line():
    notify_message = f"""セキュリティカメラで顔を検出しました。"""
    print(notify_message)
    sender.send(message=notify_message, image='detected_image.jpg')

def main():
    print("start surveillance application")
    while True:
        detect_face()
        print("face detected: Sending pic to LINE")
        notify_line()
        time.sleep(5)

if __name__ == '__main__':
    main()

