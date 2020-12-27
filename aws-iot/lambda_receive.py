import sys
import boto3
import json
def lambda_handler(event, context):

    iot = boto3.client('iot-data')

    #再生させたいwavファイルを以下で指定。ファイルは同じフォルダに入っているモノ限定
    command = "message.wav" payload = { "message": command
            }
    topic = 'things/AichiTechPrototype001' qos = 0 try: iot.publish( 
            topic = topic, qos = 0, payload=json.dumps(payload, 
            ensure_ascii=False)
        ) return "Succeeded"
    except Exception as e: print(e)
        return "Failed"
