# Bureau d'étude : Mise en œuvre d'une application IoT


## Introduction

Le but de ce bureau d'étude est de construire une application IoT de bout en bout pour collecter des grandeurs physiques (température, humidité, ...) d'une salle de l'ENSEM.

Dans un premier temps on code les cartes pycom afin de capter et de transmettre les données via le protocole LoRa, les données sont ensuite lues par d'autres capteurs et traité dans un dashboard node-red. Ensuite on stocke les données dans une base de données MySQL afin de les traiter ultérieurement. En parallèle à cela, on publie les données sur The Things Network pour un meilleur usage sur le cloud, et enfin on la base de données SQL est traité par un script python pour créer une cartographie thermique de la salle en question.

## Activité 1

Le dossier `A1` comporte les codes `sender` et `receiver` qui seront importer sur deux cartes pycom distincts : l'une pour collecter et transmettre les données et l'autre pour lire et traiter. Dans le dossier `lib` se trouve les modules et les librairies nécessaires pour les cartes pycom.

## Activité 2

Les flows `node-red` sont disponibles dans le dossier `Annexe`, l'éxecution se fait avec la commande `node-red -u '<chemin vers le dossier Annexe>'`. N.B : il faut installer les modules `node-red-dahsboard` et `node-red-node-mysql` afin d'avoir les nœuds les manquant au flow.

Dans cette partie on exécute le fichier python `Annexe/A2/mqtt_receiver.py` qui est en permanence à l'écoute des données reçues par les autres capteurs, le programme ensuite se connecte à un broker MQTT, filtre les données non provenant des autres capteurs, et les publies ensuite dans deux sub-topic MQTT : une pour la température, et l'autre pour l'humidité.