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

## Description du Projet

Le but de ce projet est de fabriquer une fusée expérimentale avec deux mission principales : 
**Analyse météo :**
Nous alons mesurer des données météorologiques grâce a un larguage de charge utile de type cansat à une altitude d’environ 3km, afin de faire une étude des nuages en moyennes altitude.
Pour cela nous utilisons de nombreux capteurs tel qu'un BME680, un anémometre à ultrason, un pyranometre, un gps et un imu.
 
**Prédiction et analyse de trajectoire en temp réel :**
Nous dévelopons un réseau de neurone afin de de prédire la trajectoire de notre fusée en fonction de different parametre (le poid, la position au décollage, les conditions météo sol au décollage) et nous allons analyser en temp réel la variation entre notre trajectoire et la prédiction de celle ci.

## Installation

Pour installer et exécuter ce projet, veuillez suivre les étapes suivantes :

1.  **Installer les dépendances :**

    Assurez-vous d'avoir Arduino IDE installé sur votre système. Ensuite, clonez le dépôt et installez les librairies nécessaires à l'aide de pip. Un fichier `requirements.txt` est généralement fourni pour lister ces dépendances.

    ```bash
    git clone [https://github.com/NFXSTUDIO/Calcul_symbolique_IA](https://github.com/NFXSTUDIO/Calcul_symbolique_IA)
    cd votre-repo
    pip install -r requirements.txt
    ```

2.  **Lancer le code :**

    Le projet propose plusieurs fichiers trié en deux catégorie : .

    * **Calcul symbolique :** Exécutez les differents fichiers pour comprendre le calcul symbolique

        ```bash
        python exercice_1.py
        ```

        ```bash
        python exercice2.py
        ```

        ```bash
        python exercice3.py
        ```

        ```bash
        python exo4.py
        ```

        ```bash
        python code_gen.py
        ```

        ```bash
        python code_gen2.py
        ```

        ```bash
        python genetic_algo.py
        ```

    * **Robotique :** Exécutez les differents fichiers pour comprendre le calcul symbolique appliqué en robotique pour calculer les differentes équations kinématiques

        ```bash
        python code_robot.py
        ```

        ```bash
        python code_3dof.py
        ```

3.  **Analyser les résultats :**

    Une fois l'exécution terminée, les résultats (par exemple, des visualisations, des métriques d'évaluation) seront sauvegardés dans des fichiers spécifiques ou affichés dans la console. Consultez la documentation ou les sorties du programme pour interpréter les résultats obtenus.
