import time
import board
import busio
import adafruit_bmp280
import adafruit_bno08x
from adafruit_bno08x import BNO_REPORT_ACCELEROMETER, BNO_REPORT_GYROSCOPE, BNO_REPORT_MAGNETOMETER, \
    BNO_REPORT_ROTATION_VECTOR
from adafruit_bno08x.i2c import BNO08X_I2C


# Créez l'objet I2C.
# Assurez-vous que le bus I2C 1 est utilisé (pins 27 et 28 sur le header GPIO 40-pin)
i2c = busio.I2C(board.SCL,board.SDA,frequency=800000)

# Créez l'objet du capteur BMP280
#bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)
bno = BNO08X_I2C(i2c)
bno.enable_feature(BNO_REPORT_ACCELEROMETER)
bno.enable_feature(BNO_REPORT_GYROSCOPE)
bno.enable_feature(BNO_REPORT_MAGNETOMETER)
bno.enable_feature(BNO_REPORT_ROTATION_VECTOR)

# Modifiez le paramètre de suréchantillonnage de la température
# pour un résultat plus précis si nécessaire
#bmp280.temperature_oversampling = 8

# Modifiez le paramètre de suréchantillonnage de la pression
# pour un résultat plus précis si nécessaire
#bmp280.pressure_oversampling = 8

# Ajustez la pression atmosphérique au niveau de la mer pour un calcul
# de l'altitude plus précis (valeur par défaut : 1013.25 hPa)
# bmp280.sea_level_pressure = 1013.25

print("Capteur BM0280 initialisé!")

while True:
    # Lecture de la température en degrés Celsius
    #temperature = bmp280.temperature
    # Lecture de la pression en hPa
    #pressure = bmp280.pressure
    # Lecture de l'altitude en mètres
    #altitude = bmp280.altitude

    #print(f"Température: {temperature:.2f} C")
    #print(f"Pression: {pressure:.2f} hPa")
    #print(f"Altitude approximative: {altitude:.2f} m")
    # Attendez 2 secondes avant la prochaine lecture
    time.sleep(2)
    print("Acceleration:")
    ax,ay,az = bno.acceleration
    print("X; %0.6f  Y: %0.6f  Z: %0.6f m/s2" % (ax,ay,az))
    print("")

    print("Gyro:")
    gx, gy, gz = bno.gyro
    print("X; %0.6f  Y: %0.6f  Z: %0.6f rad/s" % (gx, gy, gz))
    print("")

    print("Magnetometer:")
    mx, my, mz = bno.magnetic
    print("X; %0.6f  Y: %0.6f  Z: %0.6f uT" % (mx, my, mz))
    print("")

    print("Rotation Vector Quaternion:")
    qx, qy, qz, qr= bno.quaternion
    print("X; %0.6f  Y: %0.6f  Z: %0.6f  Real: %0.6f " % (qx, qy, qz, qr))
    print("")