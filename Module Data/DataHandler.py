import csv

class TrajectoryData:
    def __init__(self):
        # Header :
        self.trajectory_header = ['Temp sol (HH:MM:SS)', 'Temp fusee (s)', 'Position x (m)', 'Position y (m)', 'Position z (m)', 'Acceleration x (m/s2)', 'Acceleration y (m/s2)', 'Acceleration z (m/s2)', 'Gyroscope x (rad/s)', 'Gyroscope y (rad/s)', 'Gyroscope z (rad/s)', 'Magnetometre x (uT)', 'Magnetometre y (uT)', 'Magnetometre z (uT)', 'Quaternion i', 'Quaternion j', 'Quaternion k', 'Quaternion reel', 'Roulis (deg)', 'Tangage (deg)', 'Lacet (deg)']
        self.time_header = ['gt','rt']
        self.gps_header = ['x','y','z']
        self.imu_header = ['ax','ay','az','gx','gy','gz','mx','my','mz','qi','qj','qk','qreal','roll','pitch','yaw']

        # Dictionary :
        self.time_dict = dict.fromkeys(self.time_header)
        self.gps_dict = dict.fromkeys(self.gps_header)
        self.imu_dict = dict.fromkeys(self.imu_header)
        self.trajectory_dict = dict.fromkeys(self.trajectory_header)

        # Data file :
        self.file = 'data_exp/trajectory_data.csv'

    def convert_data_into_trajectory(self):
        # Convert time dictionary :
        j = 0
        for i in self.time_header:
            self.trajectory_dict[self.trajectory_header[j]] = self.time_dict[i]
            j += 1

        # Convert GPS dictionary :
        for i in self.gps_header:
            self.trajectory_dict[self.trajectory_header[j]] = self.gps_dict[i]
            j += 1

        # Convert IMU dictionary :
        for i in self.imu_header:
            self.trajectory_dict[self.trajectory_header[j]] = self.imu_dict[i]
            j += 1

    def export_data(self,time_data,gps_data,imu_data):
        # Add external dictionary into the class
        self.time_dict = time_data
        self.gps_dict = gps_data
        self.imu_dict = imu_data
        self.convert_data_into_trajectory()

        # Open trajectory_data.csv and write data into it
        with open(self.file,'w',newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.trajectory_header)
            writer.writeheader()
            for i in range(len(time_data['gt'])):
                row = {}
                for key in self.trajectory_header:
                    row[key] = self.trajectory_dict[key][i]
                writer.writerow(row)
        print('Export completed !')

class RocketData:
    def __init__(self):
        # Header :
        self.rocket_header = ['Temp sol (HH:MM:SS)', 'Niveau de batterie Sequenceur (%)', 'Niveau de batterie Data (%)', 'Etats']
        self.esp32_header = ['gt','st']
        self.batt_header = ['gt','bs','bd']

        # Dictionary :
        self.esp32_dict = dict.fromkeys(self.esp32_header)
        self.batt_dict = dict.fromkeys(self.batt_header)
        self.rocket_dict = dict.fromkeys(self.rocket_header)

        # Data file :
        self.file = 'data_exp/rocket_data.csv'

    def convert_data_into_rocket(self):
        # Add esp32 dict into rocket dict :
        self.rocket_dict['Temp sol (HH:MM:SS)'] = self.esp32_dict['gt']
        self.rocket_dict['Etats'] = self.esp32_dict['st']

        # Add batt dict into rocket dict :
        self.rocket_dict['Niveau de batterie Sequenceur (%)'] = self.batt_dict['bs']
        self.rocket_dict['Niveau de batterie Data (%)'] = self.batt_dict['bd']

        # Order the dictionary using 'Temp sol (HH:MM:SS)'
        self.rocket_dict = dict(sorted(self.rocket_dict.items()))

    def export_data(self,esp32_data,batt_data):
        # Add external dictionary into the class
        self.esp32_dict = esp32_data
        self.batt_dict = batt_data
        self.convert_data_into_rocket()

        # Open trajectory_data.csv and write data into it
        with open(self.file,'w',newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.rocket_header)
            writer.writeheader()
            for i in range(len(self.rocket_dict['gt'])):
                row = {}
                for key in self.rocket_header:
                    row[key] = self.rocket_dict[key][i]
                writer.writerow(row)
        print('Export completed !')