# coding: UTF-8
import snowboydecoder
import sys
import signal
import cv2
import sys
import boto3

# for AWS configuration
aws_id='AKIAYOX777ETSSDDPWG4'
aws_key='HqLdR4s58oRGtT4V+Y4TgDwVIm112ouDJuRNLJ7T'
aws_region='ap-northeast-1'
bucket='nagoyaboost2019'

interrupted = False

def takephoto():
    # Take Photo
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    frame = cv2.resize(frame, (640,480))
    filename = "photo.jpg"
    cv2.imwrite(filename, frame)
    cap.release()
    # Upload to S3
    s3 = boto3.resource('s3')
    s3.Bucket(bucket).upload_file('./photo.jpg', 'photo.jpg')

def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted

if len(sys.argv) == 1:
    print("Error: need to specify model name")
    print("Usage: python demo.py your.model")
    sys.exit(-1)

model = sys.argv[1]

# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

detector = snowboydecoder.HotwordDetector(model, sensitivity=0.5)
print('Listening... Press Ctrl+C to exit')

#camera = takephoto()

# main loop
detector.start(detected_callback=takephoto,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)

detector.terminate()
