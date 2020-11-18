# coding: UTF-8
import snowboydecoder
import sys
import signal
import cv2
import sys
import boto3
import time
import RPi.GPIO as GPIO



# for AWS configuration
bucket='hatsumei2019'
collectionId='Family'
fileName='input.jpg'
threshold = 70
maxFaces=5
interrupted = False
open_pose=3.5
close_pose=8.0

d = {'31bde984-d84c-4ba1-8ab6-a61654dcb4a9': 'Watashi'}

#Stting for Servo
GPIO.setmode(GPIO.BCM)
#GPIO4を出力端子設定 
GPIO.setup(18, GPIO.OUT)
#GPIO4をPWM設定、周波数は50Hz 
p = GPIO.PWM(18, 50)
#Duty Cycle 0% 
p.start(0.0)
p.ChangeDutyCycle(close_pose)


#Start Processing
print('--------------------------------')
print('Start Processing')

def takephoto():
    # Initialize Flags
    Family=False
    # Take Photo
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    frame = cv2.resize(frame, (640,480))
    filename = "photo.jpg"
    cv2.imwrite(filename, frame)
    cap.release()
    # Upload to S3
    s3 = boto3.resource('s3')
    s3.Bucket(bucket).upload_file('./photo.jpg', fileName)
    #Use AWS Rekognition for search faces
    client=boto3.client('rekognition')
    
    print('Start Authorization')
    try:#to escape No Face Exception from AWS
        #Use Rekognition to Search Faces
        response = client.search_faces_by_image(CollectionId=collectionId,
                            Image={'S3Object':{'Bucket':bucket,'Name':fileName}},
                            FaceMatchThreshold=threshold,
                            MaxFaces=maxFaces)
        faceMatches=response['FaceMatches']

        #List matched faces
        print('Matching faces')
        for match in faceMatches:
            print('Name:' + d[match['Face']['FaceId']]) #Look for Name from FaceID Dict
            print('Similarity: ' + "{:.2f}".format(match['Similarity']) + "%")
            Family=True
        
        if Family:
            print('Family Member Found!! Unlocking Door for 5sec!')
            p.ChangeDutyCycle(open_pose)
            time.sleep(5)
            p.ChangeDutyCycle(close_pose)
        else:
            print('Not a Family Member')

    #If no face detected
    except Exception:
        print('No face detected')
        pass

    #Initialize status
    Family=False
    print('End Authorization')
    

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
