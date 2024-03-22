import mysql.connector
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import Rbf
from matplotlib import cm

xi = np.random.rand(3)
yi = np.random.rand(3)

coordonees = {}

def fetch_last():
    "Se connecte à la base de données et renvoie les dernières valeurs de la temperature et de l'humidité par capteur existant"

    cnx = mysql.connector.connect(user='root', password='', host='localhost', database='salle206R')
    cursor = cnx.cursor()

    # Fetch the last value for each unique capteur_id
    cursor.execute("SELECT capteur_id, temperature, humidity FROM mesures WHERE (capteur_id, time) IN (SELECT capteur_id, MAX(time) FROM mesures GROUP BY capteur_id)")
    last_results = cursor.fetchall()

    capteur_ids = [row[0] for row in last_results]
    temp = [float(row[1]) for row in last_results]
    humi = [float(row[2]) for row in last_results]

    cursor.close()
    cnx.close()

    return capteur_ids, temp, humi

def update_plot():
    "Mets à jour la figure en reprenant dans un laps de temps prédéfini les dernières valeurs de la base de données"

    capteur_ids, temp, humi = fetch_last()

    global coordonees
    if len(coordonees) < len(capteur_ids) :
        for id in capteur_ids:
            coordonees[id] = {
                "xi" : np.random.rand(),
                "yi" : np.random.rand(),
                "nom" : id,
            }
    
    ti = np.linspace(0, 1, 100)
    XI, YI = np.meshgrid(ti, ti)

    xi = [coordonees[id]["xi"] for id in capteur_ids]
    yi = [coordonees[id]["yi"] for id in capteur_ids]

    rbf_T = Rbf(xi, yi, temp, function='gaussian')
    rbf_H = Rbf(xi, yi, humi, function='gaussian')
    Z_T = rbf_T(XI, YI)
    Z_H = rbf_H(XI, YI)

    plt.clf()

    # Plot Temperature
    plt.subplot(2, 1, 1)
    plt.title("Temperature")
    plt.pcolor(XI, YI, Z_T, cmap=cm.jet)
    plt.scatter(xi, yi, 50, temp, cmap=cm.jet)
    plt.colorbar()
    plt.xlim(0, 1)
    plt.ylim(0, 1)


    for id in coordonees:
        capt = coordonees[id]
        plt.text(capt["xi"], capt["yi"], capt["nom"], color='black', ha='center', va='bottom')


    plt.subplot(2, 1, 2)
    plt.title("Humidité")
    plt.pcolor(XI, YI, Z_H, cmap=cm.jet)
    plt.scatter(xi, yi, 50, humi, cmap=cm.jet)
    plt.colorbar()
    plt.xlim(0, 1)
    plt.ylim(0, 1)

    for id in coordonees:
        capt = coordonees[id]
        plt.text(capt["xi"], capt["yi"], capt["nom"], color='black', ha='center', va='bottom')

    plt.pause(0.001)

while True:
    update_plot()
    plt.pause(1)
