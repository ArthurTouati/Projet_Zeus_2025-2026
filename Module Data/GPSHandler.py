import numpy as np
import smbus2
import pynmea2

class GPSHandler:
    def __init__(self):
        # Coordinate :
        self.x = []
        self.y = []
        self.z = []

        # Constant :
        self.EARTH_RADIUS = 6371000

        # Export dict :
        self.header = ['x','y','z']
        self.gps_dict = dict.fromkeys(self.header)

        # Sensor init :
        self.I2C_BUS_NUM = 1  
        self.SAM_M10Q_ADDR = 0x42
        self.bus = smbus2.SMBus(self.I2C_BUS_NUM)
        self.readbuffer = b""

    def convert_lat_long_to_xy(self,lat,long,altitude):
        # Convert latitude and longitude into radians
        lat_rad = lat * (np.pi / 180)
        lon_rad = long * (np.pi / 180)

        r = self.EARTH_RADIUS + altitude

        # Calculate x, y coordinates
        self.x.append(r * np.cos(lat_rad) * np.cos(lon_rad))
        self.y.append(r * np.cos(lat_rad) * np.sin(lon_rad))
        self.z.append(r * np.sin(lat_rad))
        
    def export_to_dict(self):
        # Add each list to the dictionary
        self.gps_dict['x'] = self.x
        self.gps_dict['y'] = self.y
        self.gps_dict['z'] = self.z

        # Export dictionary
        return self.gps_dict

    def clear_dict(self):
        self.gps_dict.clear()

        # Clear all list
        self.x.clear()
        self.y.clear()
        self.z.clear()

    def read_data(self):
        # Recover data from GPS :
        data = self.bus.read_i2c_block_data(self.SAM_M10Q_ADDR, 0xFF, 32)
        self.read_buffer += data
        lines = self.read_buffer.decode('ascii', errors='ignore').split('\r\n')
        self.read_buffer = lines[-1].encode('ascii')

        # Process lines :
        for line in lines[:-1]:
            if line.startswith('$GNGGA'):
                try:
                    msg = pynmea2.parse(line)
                        if msg.is_valid and msg.gps_qual > 0:
                            lat = msg.latitude
                            long = msg.longitude
                            altitude = msg.altitude
                            # Convert and add value into xyz coordinate :
                            self.convert_lat_long_to_xy(lat,long,altitude)
                        except pynmea2.ParseError as e:
                            pass