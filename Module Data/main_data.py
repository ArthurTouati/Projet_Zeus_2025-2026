import time
import board
import busio
from datetime import datetime
import IMUHandler as Imu
#import GPSHandler as Gps
import DataHandler as Data
import ESP32Handler as Esp32
import ADCHandler as Adc

""" Code trajectoire : 
# Setup
i2c = busio.I2C(board.SCL,board.SDA)
imu = Imu.IMUHandler(i2c)
gps = Gps.GPSHandler()
esp32 = Esp32.ESP32Handler(i2c)
i = 0
header_time = ['gt','rt']
time_dict = dict.fromkeys(header_time)
ground_time, rocket_time = [],[]

while i <= 10:
    time.sleep(0.5)
    imu.read_data()
    gps.read_data()
    ground_time.append(datetime.now().strftime('%H:%M:%S'))
    rocket_time.append(i)
    i+= 0.5

imu_dict = imu.export_to_dict()
gps_dict = gps.export_to_dict()
time_dict['gt'] = ground_time
time_dict['rt'] = rocket_time
print(time_dict)
print(imu_dict)
print(gps_dict)
trajectory_file = Data.TrajectoryData()
trajectory_file.export_data(time_dict,gps_dict,imu_dict)
"""

""" Code fusée : """
# Setup :
i2c = busio.I2C(board.SCL,board.SDA)
esp32 = Esp32.ESP32Handler(i2c)
adc = Adc.ADCHandler(i2c)
rocket_file = Data.RocketData()
i = 0

while i<=10:
    time.sleep(0.5)
    esp32.read_data()
    adc.read_data()
    i+=0.5

esp32_dict = esp32.export_to_dict()
batt_dict = adc.export_to_dict()
print(batt_dict)
print(esp32_dict)
rocket_file.export_data(esp32_dict,batt_dict)