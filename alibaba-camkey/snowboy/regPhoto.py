# coding: UTF-8
import sys
import boto3

# for AWS configuration
bucket='hatsumei2019'
collectionId='Family'

# Receive filename from Console
args = sys.argv
fileName = args[1]

#Upload photo to S3
s3 = boto3.resource('s3')
s3.Bucket(bucket).upload_file(fileName, fileName)

# Regist to rekogniton index_Face
client=boto3.client('rekognition')
response=client.index_faces(CollectionId=collectionId,
        Image={'S3Object':{'Bucket':bucket,'Name':fileName}},
        ExternalImageId=fileName,
        DetectionAttributes=['ALL'])

print ('Faces in ' + fileName)
for faceRecord in response['FaceRecords']:
        print (faceRecord['Face']['FaceId'])


