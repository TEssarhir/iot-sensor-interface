import os
import time
import socket
import struct
import ujson
import utime
from network import LoRa
# A basic package header, B: 1 byte for the deviceId, B: 1 byte for the pkg size, %ds: Formated string for string
_LORA_PKG_FORMAT = "!BB%ds"
# A basic ack package, B: 1 byte for the deviceId, B: 1 bytes for the pkg size, B: 1 byte for the Ok (200) or error messages
_LORA_PKG_ACK_FORMAT = "BBB"
# Open a LoRa Socket, use rx_iq to avoid listening to our own messages
lora = LoRa(mode=LoRa.LORA, rx_iq=True, region=LoRa.EU868)
lora_sock = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
lora_sock.setblocking(False)
gateway_Id='TP_lora_GW'
while (True):
    recv_pkg = lora_sock.recv(512)
    if (len(recv_pkg) > 2):
        recv_pkg_len = recv_pkg[1]
        try:
            DEVICE_ID, pkg_len, msg = struct.unpack(_LORA_PKG_FORMAT % recv_pkg_len, recv_pkg)
            #recuperation du dictionnaire python cree dans les nodes emetteurs
            dic = ujson.loads(msg.decode().strip())
            print("CAPT" + str(dic["sensor_Id"]) + "," + str(dic["temperature"]) + "," + str(dic["humidity"]))
            #fermeture du dump
        except:
            print("erreur_paquet recu par " + gateway_Id)