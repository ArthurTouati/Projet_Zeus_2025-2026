from adafruit_ads1x15 import ADS1115,AnalogIn,ads1x15
from adafruit_ads1x15.ads1x15 import Mode
from datetime import datetime

class ADCHandler:
    def __init__(self,i2c):
        # Batterie level :
        self.ground_time = []
        self.batt_seq = []
        self.batt_data = []

        # Export dictionary :
        self.batt_header = ['gt', 'bs', 'bd']
        self.batt_dict = dict.fromkeys(self.batt_header)

        # Init sensor
        self.ads = ADS1115(i2c)
        self.ads.mode = Mode.CONTINUOUS
        print("ADS1115 init done !")

    def read_data(self):
        # Read raw data (voltage) :
        voltage_seq = AnalogIn(self.ads, ads1x15.Pin.A0).voltage
        voltage_data = AnalogIn(self.ads, ads1x15.Pin.A1).voltage

        # Convert voltage into battery level :
        # Max level = 5V
        # Min level = 4.69 V
        level_seq = ((voltage_seq - 4.69) / (5 - 4.69)) * 100.0
        level_data = ((voltage_data - 4.69) / (5 - 4.69)) * 100.0
        print(f"Battery level : {level_seq}%")
        print(f"Battery level : {level_data}%")

        # Verify if the level is between 0 and 100% and correct if there is a mistake :
        if level_seq > 100.0:
            level_seq = 100.0
        elif level_seq < 0.0:
            level_seq = 0.0

        if level_data > 100.0:
            level_data = 100.0
        elif level_data < 0.0:
            level_data = 0.0

        # Add to list
        self.ground_time.append(datetime.now().strftime('%H:%M:%S'))
        self.batt_seq.append(level_seq)
        self.batt_data.append(level_data)

    def export_to_dict(self):
        self.batt_dict['gt'] = self.ground_time
        self.batt_dict['bs'] = self.batt_seq
        self.batt_dict['bd'] = self.batt_data
        return self.batt_dict

    def clear_dict(self):
        self.ground_time.clear()
        self.batt_seq.clear()
        self.batt_data.clear()
        self.batt_dict.clear()