DROP DATABASE IF EXISTS salle206R;
CREATE DATABASE salle206R;
USE salle206R;

CREATE TABLE mesures (
    time VARCHAR(45),
    capteur_id VARCHAR(45),
    temperature VARCHAR(45),
    humidity VARCHAR(45),
    PRIMARY KEY (time, capteur_id)
);
