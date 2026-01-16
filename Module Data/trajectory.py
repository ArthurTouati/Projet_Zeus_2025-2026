import time
import board
import busio
from datetime import datetime
import IMUHandler as Imu
import GPSHandler as Gps
import DataHandler as Data

class Trajectory:
    def __init__(self,max_time=10,time_step=0.5):
        self.imu_dict = None
        self.gps_dict = None
        self.header = ['gt','rt']
        self.time_dict = dict.fromkeys(self.header)
        self.i2c = busio.I2C(board.SCL,board.SDA)
        self.imu = Imu.IMUHandler(self.i2c)
        self.gps = Gps.GPSHandler()
        self.ground_time, self.rocket_time = [],[]
        self.actual_time = 0
        self.time_step = time_step
        self.max_time = max_time
        self.trajectory_file = Data.TrajectoryData()

    def recover_trajectory_data(self):
        while self.actual_time <= self.max_time:
            time.sleep(self.time_step)
            self.imu.read_data()
            self.gps.read_data()
            self.ground_time.append(datetime.now().strftime('%H:%M:%S'))
            self.rocket_time.append(self.actual_time)
            self.actual_time+=self.time_step

        self.imu_dict = self.imu.export_to_dict()
        self.gps_dict = self.gps.export_to_dict()
        print(self.time_dict)
        print(self.imu_dict)
        print(self.gps_dict)
        self.trajectory_file.export_data(self.time_dict,self.gps_dict,self.imu_dict)
        self.imu.clear_dict()
        self.gps.clear_dict()
        self.time_dict.clear()
        print("Data recovered and exported to csv file !")