import time
import board
import busio
from adafruit_bno08x import (BNO_REPORT_ACCELEROMETER,BNO_REPORT_GYROSCOPE,BNO_REPORT_MAGNETOMETER,BNO_REPORT_ROTATION_VECTOR,)
from adafruit_bno08x.i2c import BNO08X_I2C

def setup_imu():
    try:
        global bno
        i2c = busio.I2C(board.SCL, board.SDA, frequency=400000)
        bno = BNO08X_I2C(i2c)
        bno.enable_feature(BNO_REPORT_ACCELEROMETER)
        bno.enable_feature(BNO_REPORT_GYROSCOPE)
        bno.enable_feature(BNO_REPORT_MAGNETOMETER)
        bno.enable_feature(BNO_REPORT_ROTATION_VECTOR)
        return True
    except ValueError as e:
        print(f"Erreur d'initialisation IMU : {e}")
        return False
    except OSError as e:
        print(f"Erreur de communication I2C : {e}")
        return False


def read_imu_data():
    try:
        accel_x, accel_y, accel_z = bno.acceleration
        gyro_x, gyro_y, gyro_z = bno.gyro
        mag_x, mag_y, mag_z = bno.magnetic
        quat_i, quat_j, quat_k, quat_real = bno.quaternion
        return True, (accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z, 
                     mag_x, mag_y, mag_z, quat_i, quat_j, quat_k, quat_real)
    except:
        return False, None

# Boucle principale
if __name__ == "__main__":
    if not setup_imu():
        print("Échec de l'initialisation de l'IMU")
        exit(1)
        
    try:
        while True:
            success, data = read_imu_data()
            if success:
                # Affichage des données
                print("Acceleration:")
                print("X: %0.6f  Y: %0.6f Z: %0.6f  m/s^2" % data[0:3])
                # ... reste des affichages ...
            else:
                print("Erreur de lecture des données")
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nArrêt du programme")