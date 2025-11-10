import numpy as np
class GPSHandler:
    def __init__(self):
        # GPS coordinates :
        self.lat = 0.0
        self.lon = 0.0

        # Coordinate :
        self.x = []
        self.y = []
        self.z = []

        # Export dict :
        self.header = ['x','y','z']
        self.gps_dict = dict.fromkeys(self.header)

        # Sensor init :

    def read_data(self):
        self.convert_lat_long_to_xyz()
        pass

    def convert_lat_long_to_xyz(self):
        # Convert latitude and longitude into radians
        lat_rad = self.lat * (np.pi / 180)
        lon_rad = self.lon * (np.pi / 180)

        # Calculate x, y coordinates
        self.x.append(np.cos(lat_rad) * np.cos(lon_rad))
        self.y.append(np.cos(lat_rad) * np.sin(lon_rad))