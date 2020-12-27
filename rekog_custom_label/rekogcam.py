import json
import cv2
from boto3.session import Session
import numpy as np

PROFILE = 'default'
REGION = 'us-east-1'
MODEL_ARN = 'arn:aws:rekognition:us-east-1:994958086421:project/Gundam_unicorn_barbados/version/Gundam_unicorn_barbados.2020-12-28T01.34.15/1609086854919'

CLASSES = ['Barbados','Unicorn']

# Webカメラ
deviceId = 0 
height = 600
width = 800

# ターゲット（推論の対象）
W = 400
H = 400
BIAS = 50

class Rekognition():
    def __init__(self, profile, region, modelArn):
        self.__modelArn = modelArn
        session = Session(profile_name = profile, region_name = region)
        self.__client = session.client('rekognition')

    def detect(self, image):
        data = self.__client.detect_custom_labels(
            ProjectVersionArn = self.__modelArn,
            Image = {
                "Bytes": image
            },
            MaxResults = 100,
            MinConfidence = 30
        )
        return data["CustomLabels"]


def main():
    global width
    global height
    
    rekognition = Rekognition(PROFILE, REGION, MODEL_ARN)

    # カメラ初期化
    cap = cv2.VideoCapture(deviceId)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print("FPS:{}　WIDTH:{}　HEIGHT:{}".format(fps, width, height))

    # 推論の対象
    x1 = int(width/2-W/2)
    x2 = int(width/2+W/2)
    y1 = int(height/2-H/2-BIAS)
    y2 = int(height/2+H/2-BIAS)

    while True:

        # カメラ画像取得
        ret, frame = cap.read()
        if(frame is None):
            continue

        # 推論の対象を切り取る
        img = frame[y1: y2, x1: x2]

        # 推論
        _, jpg = cv2.imencode('.jpg', img)
        results = rekognition.detect(jpg.tostring())

        # 表示
        if(len(results) > 0):
            str = "{} Confidence:{:.2f}%".format(results[0]["Name"], results[0]["Confidence"])
            cv2.putText(frame,str,(20, int(height)-20), cv2.FONT_HERSHEY_SIMPLEX, 2.0, (255,255,255), 2, cv2.LINE_AA)
        frame = cv2.rectangle(frame,(x1, y1), (x2, y2), (155,155,0),1)
        cv2.imshow('frame', frame)
        cv2.waitKey(1)

    cap.release()
    cv2.destroyAllWindows()

main()
