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
collectionId='Family'
fileName='input.jpg'
threshold = 70
maxFaces=5
interrupted = False

d = {'dda30189-795a-4bfb-9a93-5f85ac763b8b': 'BigDaddy',
     '2aa75dd5-3023-4fa6-a8c0-7ff628521d40': 'NOBU',
     '21bce709-425d-4261-9d2f-73cd32f5f578': 'A',
     '55a33684-4022-470a-b433-2f5e0061ea3d': 'B',
     'af0653a8-d016-4a8e-811c-82d37c99584d': 'C',
     '4e10abd6-de92-4f72-a9df-b081434118a2': 'D'}


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
    client=boto3.client('rekognition', 
        aws_access_key_id=aws_id,
        aws_secret_access_key=aws_key,
        region_name=aws_region)
    
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
            print('Family Member Found!! Open SESAME!')
        else:
            print('Not a Family Member')

    #If no face detected
    except Exception:
        print('No face detected')
        pass

    #Initialize status
    Family=False
    

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
