import time
import board
import adafruit_bmp280

# Créez l'objet I2C.
# Assurez-vous que le bus I2C 1 est utilisé (pins 27 et 28 sur le header GPIO 40-pin)
i2c = board.I2C()

# Créez l'objet du capteur BMP280
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)

# Modifiez le paramètre de suréchantillonnage de la température
# pour un résultat plus précis si nécessaire
bmp280.temperature_oversampling = 8

# Modifiez le paramètre de suréchantillonnage de la pression
# pour un résultat plus précis si nécessaire
bmp280.pressure_oversampling = 8

# Ajustez la pression atmosphérique au niveau de la mer pour un calcul
# de l'altitude plus précis (valeur par défaut : 1013.25 hPa)
# bmp280.sea_level_pressure = 1013.25

print("Capteur BMP280 initialisé!")

while True:
    # Lecture de la température en degrés Celsius
    temperature = bmp280.temperature
    # Lecture de la pression en hPa
    pressure = bmp280.pressure
    # Lecture de l'altitude en mètres
    altitude = bmp280.altitude

    print(f"Température: {temperature:.2f} C")
    print(f"Pression: {pressure:.2f} hPa")
    print(f"Altitude approximative: {altitude:.2f} m")

    # Attendez 2 secondes avant la prochaine lecture
    time.sleep(2)