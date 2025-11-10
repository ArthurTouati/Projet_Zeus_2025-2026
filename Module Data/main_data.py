import time
import IMUHandler as Imu
import GPSHandler as Gps
import board
import busio
import DataHandler as Data
from datetime import datetime

# Setup
i2c = busio.I2C(board.SCL,board.SDA)
imu = Imu.IMUHandler(i2c)
gps = Gps.GPSHandler() 
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
