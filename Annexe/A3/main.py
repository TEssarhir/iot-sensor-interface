import binascii, socket, time, pycom
from network import LoRa
from pycoproc_1 import Pycoproc
from SI7006A20 import SI7006A20

pycom.heartbeat(False)
pycom.rgbled(0x0A0A08)

py = Pycoproc(Pycoproc.PYSENSE)

lora = LoRa(mode=LoRa.LORAWAN, rx_iq=True, region=LoRa.EU868)


# informations spécific au capteur et à l'application TTN
dev_eui = binascii.unhexlify('70B3D5499C44B33D')
app_eui = binascii.unhexlify('70B3D57ED0065D37')
app_key = binascii.unhexlify('E78595D0EFBAED63D539DDB08611A7F0')

# ajout de trois canaux
lora.add_channel(0, frequency=868500000, dr_min=0, dr_max=5)
lora.add_channel(1, frequency=868500000, dr_min=0, dr_max=5)
lora.add_channel(2, frequency=868500000, dr_min=0, dr_max=5)

lora.join(activation=LoRa.OTAA,
          auth=(dev_eui, app_eui, app_key),
          timeout=0, dr=5)


# attendre que le module rejoins le réseau
while not lora.has_joined():
    time.sleep(3)
    print('Not joined yet...')
else:
    print('Network joined')


# pour enlever les other canaux
for i in range(3,16):
    lora.remove_channel(i)

# création d'un socket LoRa
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

# fait en sorte que le capteur n'est pas bloqué
s.setblocking(False)
time.sleep(3)

si = SI7006A20(py)

# lecture et envoie des données
while True:
    print("Temperature : " + str(si.temperature()) + "deg C")
    print("Humidity : " + str(si.humidity()) + "%RH")
    s.send(str(si.temperature()))
    time.sleep(3)