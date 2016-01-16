#!/usr/bin/python -u
# -u to unbuffer stdout, plays nicer with supervisor

import unicornhat as unicorn
import json
import os
import logging
import paho.mqtt.client as paho

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M')

logger = logging.getLogger(os.path.basename(__file__))

logger.debug('Starting...')

""" hostname and topic of MQTT """
hostname = os.getenv('MQTT_HOST')
topic = os.getenv('MQTT_TOPIC')
""" Optional username and password for MQTT """
username = os.getenv('MQTT_USER', None)
password = os.getenv('MQTT_PASSWORD', None)


def change_color(color):

    r = color['r']
    g = color['g']
    b = color['b']
    a = color['a']

    logger.debug("Setting to r:%d g:%d b:%d brightness:%.2f" % (r,g,b,a))

    unicorn.brightness(a)

    for y in range(8):
            for x in range(8):
                    unicorn.set_pixel(x,y,int(r),int(g),int(b))
                    unicorn.show()


def on_message(client, userdata, message):
    """Called whenever a message is received. 

    """

    try:
        data = json.loads(message.payload)
    except:
        logging.debug("failed to parse json. message=%s" % message.payload)
        return False

    color = data['color']
    logger.debug("Detected color: %s" % color)
    change_color(color)


def on_connect(client, userdata, rc):
    logging.debug("connected with result code=%s " % str(rc))


if __name__ == "__main__":

    mqttc = paho.Client()
    mqttc.on_message = on_message

    mqttc.on_connect = on_connect
    if username is not None and password is not None:
        logging.debug("connected to MQTT with authentication")
        mqttc.username_pw_set(username, password)
    else:
        logging.debug("connected to MQTT without authentication")

    try:
        mqttc.connect(hostname)
    except Exception as e:
        logging.debug("failed to connect: %s" % e)

    logging.debug("subscribing to topic: %s" % topic)
    mqttc.subscribe(topic)

    while mqttc.loop() == 0:
        pass
