import time
import board
import busio
from datetime import datetime
import GPSHandler as Gps

i2c = busio.I2C(board.SCL,board.SDA)
gps = Gps.GPSHandler(i2c)

i = 0

while i <= 10:
    time.sleep(0.5)
    gps.read_data()
    i+= 0.5

gps_dict = gps.export_to_dict()
print(gps_dict)
