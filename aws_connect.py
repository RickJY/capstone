import time
import paho.mqtt.client as mqtt
import ssl
import json
import os

link="https://drive.google.com/drive/u/0/folders/1GXcT1o8iFkjG6WV53lY_lk-Fu32pvFQ7"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to AWS IoT: Success")
        publishData()
    else:
        print(f"Connection to AWS IoT failed with result code {rc}")

client = mqtt.Client()
client.on_connect = on_connect
client.tls_set(ca_certs='./rootCA.pem', certfile='./certificate.pem.crt', keyfile='./private.pem.key', tls_version=ssl.PROTOCOL_SSLv23)
client.tls_insecure_set(True)
client.connect("a13dfjmp6yetj3-ats.iot.ca-central-1.amazonaws.com", 8883, 60)

def publishData():
    client.publish("detect/pub", payload=json.dumps({"Warning": link}), qos=0, retain=False)
    print("Data published")

# Wait for a brief moment (e.g., 1 second) before disconnecting
client.loop_start()
time.sleep(2)

# Disconnect from AWS IoT
client.loop_start()
client.disconnect()

os.system('python3 upload.py')

