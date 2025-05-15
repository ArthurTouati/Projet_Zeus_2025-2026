<p align="center">
  <br>
  <a href="#">
    <img src="Logo_IPSA.png" alt="Logo du Projet" width="200">
  </a>
  <br>
</p>

<h1 align="center">PMI - Projet Zeus </h1>

<p align="center">
  Projet réalisé par : Corentin GAUDARD / Charbel Ghanem / Antoine ROUYER / Arthur TOUATI
  <br>
  License : MIT
  <br>
  Version : 1.0
  <br>
</p>

---

## Table des matières

- [Description](#Description-du-projet)
- [Matériel Requis](#matériel-requis)
- [Logiciel Requis](#logiciel-requis)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Configuration](#configuration) (Optionnel)
- [Bibliothèques Utilisées](https://www.google.com/search?q=%23biblioth%C3%A8ques-utilis%C3%A9es)
- [Schéma de Câblage](https://www.google.com/search?q=%23sch%C3%A9ma-de-c%C3%A2blage) (Optionnel)
- [Crédits](#crédits)
- [Licence](#licence)
- [Remerciements](#remerciements) (Optionnel)

## Description du Projet

Le but de ce projet est de fabriquer une fusée expérimentale avec deux mission principales : 
**Analyse météo :**
Nous alons mesurer des données météorologiques grâce a un larguage de charge utile de type cansat à une altitude d’environ 3km, afin de faire une étude des nuages en moyennes altitude.
Pour cela nous utilisons de nombreux capteurs tel qu'un BME680, un anémometre à ultrason, un pyranometre, un gps et un imu.
 
**Prédiction et analyse de trajectoire en temp réel :**
Nous dévelopons un réseau de neurone afin de de prédire la trajectoire de notre fusée en fonction de different parametre (le poid, la position au décollage, les conditions météo sol au décollage) et nous allons analyser en temp réel la variation entre notre trajectoire et la prédiction de celle ci.
