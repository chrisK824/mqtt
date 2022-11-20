import paho.mqtt.client as mqtt
from storeSensors import payloadHandler

# MQTT Settings
MQTT_Broker = "hairdresser.cloudmqtt.com"
MQTT_Port = 17214
Keep_Alive_Interval = 60
MQTT_Topic = "laptop/stats/#"
USERNAME = "ixyzuhmh"
PASSWORD = "XNfCz_qhTNOi"

def on_connect(client, userdata, flags, rc):
    print("Connected to broker")

def on_message(client, userdata, msg):
    print("MQTT Topic: " + msg.topic + "   Data: " + msg.payload.decode("utf-8"))
    payloadHandler(msg.topic, msg.payload)


mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.username_pw_set(USERNAME, password=PASSWORD)
mqttc.connect(MQTT_Broker, MQTT_Port, Keep_Alive_Interval)
mqttc.subscribe(MQTT_Topic)
mqttc.loop_forever()
