import paho.mqtt.client as mqtt
import time
from . import db
from . import broker

topic="boiler"
data=60
dict_mqtt={topic:data}

def on_connect(client,userdata,flags,rc):
    print("Connected with fresult code "+str(rc))
    client.subscribe(topic)
    client.publish(topic,data)
    db.Master.query(dict_mqtt)

def on_message(client,userdata,msg):
    newvalue=str(msg.payload.decode("utf-8"))
    print(newvalue)


def on_disconnect(client, userdata,rc=0):
    logging.debug("DisConnected result code "+str(rc))
    client.loop_stop()

client=mqtt.Client()
client.on_connect=on_connect
client.on_message=on_message
client.on_disconnect=on_disconnect

client.connect("broker.mqttdashboard.com",1883,60)

#client.loop_start()
