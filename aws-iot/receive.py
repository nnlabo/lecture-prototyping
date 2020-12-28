import paho.mqtt.client
import ssl
import json
import subprocess
import time

endpoint = "a1shzaucqrt7xx-ats.iot.us-east-1.amazonaws.com" #AWS endpoint
port = 8883 #AWS Endpoint Port
topic_to_aws ="things/AichiTechPrototype001"
rootCA = "./AmazonRootCA1.pem" # Route Certificate
cert = "./8e33139213-certificate.pem.crt" #Device Certificate
key = "./8e33139213-private.pem.key" # Private Key

def on_connect(client, userdata, flags, respons_code):
    print("Connected")
    client.subscribe(topic_to_aws) #Start Subscribe

def on_message(client, userdata, msg):
    print(msg.payload.decode("utf-8"))
    print("Received message '" + str(msg.payload) + "' on topic '" + msg.topic + "' with QoS " + str(msg.qos))
    remoteSoundCommandjson=json.loads(msg.payload.decode("utf-8"))
    print(remoteSoundCommandjson['message'])
    remoteSoundCommand=remoteSoundCommandjson['message']

    subprocess.call("aplay -D plughw:b1,0 "+remoteSoundCommand, shell=True)

if __name__ == '__main__':
    client = paho.mqtt.client.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.tls_set(ca_certs=rootCA, certfile=cert, keyfile=key, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)

    while True:
        try:
            client.connect(endpoint, port=port, keepalive=60)
            break
        except:
            time.sleep(10)

    print("StartScript")
    client.loop_forever()
