#!/bin/python3
import paho.mqtt.client as mqtt
import os, re, subprocess

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("heyu/#")


def run_heyu_command(cmd):
    for x in range(10):
        try:
            print("Running \"{}\"".format(cmd))
            subprocess.run(cmd, check=True, shell=True)
            break
            time.sleep(3)
        except Exception as e:
            print(str(e))
            pass
    else:
        print("too many attempts failing...")
        return False
    return True


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    topic = msg.topic

    print(msg.topic+" "+str(msg.payload))

    # example command topic: /x10/A1/set
    # example brightness topic /x10/A1/setb
    # brightness is not yet working
    light_re = re.search(r'/([A-Z][0-9][0-9]?)/', str(msg.topic))

    if light_re is None:
        print("no light")
        return
    light = light_re.group(1) # get first group, which should be the light name.
    state_topic  = "heyu/{}/state".format(light)
    payload_utf = msg.payload.decode('utf8')
    if topic.split('/')[-1] == 'set':
        if payload_utf.upper() == 'ON':
            cmd = "heyu on {}".format(light)
            if run_heyu_command(cmd):
                client.publish(state_topic, "ON")

        if payload_utf.upper() == 'OFF':
            cmd = "heyu off {}".format(light)
            if run_heyu_command(cmd):
                client.publish(state_topic, "OFF")
        print("done")


if __name__ == "__main__":

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(os.environ.get("MQTT_BROKER"), 1883, 60)

    client.loop_forever()
