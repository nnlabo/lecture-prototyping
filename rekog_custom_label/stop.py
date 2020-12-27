import boto3
import time
def stop_model(model_arn): 
    client=boto3.client('rekognition') 
    print('Stopping model:' + model_arn)
    #Stop the model
    try:
        response=client.stop_project_version(ProjectVersionArn=model_arn)
        status=response['Status'] 
        print ('Status: ' + status)
    except Exception as e: 
        print(e) 
    print('Done...')

def main():

    model_arn='arn:aws:rekognition:us-east-1:994958086421:project/Gundam_unicorn_barbados/version/Gundam_unicorn_barbados.2020-12-28T01.34.15/1609086854919'
    stop_model(model_arn)
if __name__ == "__main__":
    main()
