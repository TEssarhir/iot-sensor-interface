from network import LoRa
import ubinascii
lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868)
print("DevEUI: %s" % (ubinascii.hexlify(lora.mac()).decode('ascii')))
# DevEUI: 70b3d5499c44b33d