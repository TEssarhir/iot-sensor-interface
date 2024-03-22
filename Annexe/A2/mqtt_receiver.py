import time
import paho.mqtt.client as paho
import serial
import json

CAPT_ALLOWED = [f"CAPT{i}" for i in range(420,430)]
COM = "/dev/tty.usbmodemPy3434341"              #? port de la carte variable en fonction du OS
serialPort = serial.Serial(port=COM,
                           baudrate=115200,
                           bytesize=8,
                           timeout=2,
                           stopbits=serial.
                           STOPBITS_ONE)

broker="localhost"

def on_message(client, userdata, message):
    time.sleep(1)
    print(f"received message = {message.payload.decode("utf-8")}")

client = paho.Client(paho.CallbackAPIVersion.VERSION2) #! cette syntaxe est spécific à la version 2 du module paho-mqtt
client.on_message = on_message

# connection au broker
print(f"connecting to broker {broker}")
client.connect(broker)
client.loop_start()

print("subscribing")
client.subscribe("ensem/CAPT")
time.sleep(2)

print("Debut lecture des capteurs")


try:
    while True:
        DATA = serialPort.read(100).decode('ascii').split("\n")
        for d in DATA:
            d = d.split(",")
            if ("CAPT" in d[0] and len(d) == 3) and d[0] in CAPT_ALLOWED and type(d[1]) == float and type([2]) == float:           # vérifier si les données captés sont autorisés
                id = d[0].replace("CAPT","")

                d_json = {
                    "id" : d[0],
                    "temp" : d[1],
                    "humi" : d[2]
                }
                d_json = json.dumps(d_json)

                print(f'Donnée reçue en provenance du capteur : {d}')
                client.publish(f"ensem/CAPT/{id}", d_json)

except KeyboardInterrupt:
    client.disconnect()
    client.loop_stop()