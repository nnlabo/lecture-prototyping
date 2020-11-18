import boto3

# for AWS configuration
#aws_id='AKIAIOIUZOQ43SRVK5ZQ'
#aws_key='ttFGdFbD6a0L+NIJ+WCG1XPY9QIKaxnN99K/CN53'
#aws_region='ap-northeast-1'
collectionId='Family'
maxResults=2


client=boto3.client('rekognition')

#Create a collection
print('Creating collection:' + collectionId)
response=client.create_collection(CollectionId=collectionId)
print('Collection ARN: ' + response['CollectionArn'])
print('Status code: ' + str(response['StatusCode']))
print('Done...')

#Result
#Creating collection:Family
#Collection ARN: aws:rekognition:ap-northeast-1:581431195943:collection/Family
#Status code: 200
#Done...
