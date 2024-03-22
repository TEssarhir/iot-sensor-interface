import os
import socket
import time
import struct
from network import LoRa
import ujson

import pycom
from pycoproc_1 import Pycoproc
# from LIS2HH12 import LIS2HH12
from SI7006A20 import SI7006A20
from LTR329ALS01 import LTR329ALS01
from MPL3115A2 import MPL3115A2, ALTITUDE, PRESSURE
#Les commentaires anglais viennent du code présent sur le git officiel permettant de tester une communication LoRa
py = Pycoproc(Pycoproc.PYSENSE)
si = SI7006A20(py)
lt = LTR329ALS01(py)
# li = LIS2HH12(py)
# A basic package header, B: 1 byte for the deviceId, B: 1 bytes for the pkg size
_LORA_PKG_FORMAT = "BB%ds"
_LORA_PKG_ACK_FORMAT = "BBB"
DEVICE_ID = 0x03
# Open a Lora Socket, use tx_iq to avoid listening to our own messages # Please pick the region that matches where you are using the device: # Asia = LoRa.AS923
# Australia = LoRa.AU915
# Europe = LoRa.EU868
# United States = LoRa.US915
lora = LoRa(mode=LoRa.LORA, tx_iq=True, region=LoRa.EU868)
lora_sock = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
indice = 1 #juste pour numeroter les paquets
while(True):
#Stockage de toutes les donnees des capteurs dans un dictionnaire python
    mpAlt = MPL3115A2(py,mode=ALTITUDE)
    list = {
        "sensor_Id": 423,
        "indice": indice,
        "humidity": si.humidity(),
        "temperature" : (mpAlt.temperature() + si.temperature() )/2
    }
    #on peut ajouter d'autres donnees dans le dictionnaire 'list'
    # print(list)
    liste = ujson.dumps(list)
    print(liste)
    pkg = struct.pack(_LORA_PKG_FORMAT % len(liste), DEVICE_ID, len(liste), liste)
    print(pkg)
    lora_sock.setblocking(True)
    lora_sock.send(pkg)
    lora_sock.setblocking(False)
    indice += 1