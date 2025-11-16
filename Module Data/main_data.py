import time
import board
import busio
import DataHandler as Data
import ESP32Handler as Esp32
import ADCHandler as Adc

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
rocket_file.export_data(esp32_dict,batt_dict)