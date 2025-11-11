import board
from Adafruit_ADS1x15 import ADS1115,AnalogIn,ads1x15
from Adafruit_ADS1x15.ads1x15 import Mode

i2c = board.I2C()
ads = ADS1115(i2c)
ads.mode = Mode.CONTINUOUS
chan1 = AnalogIn(ads, ads1x15.Pin.A0)
chan2 = AnalogIn(ads, ads1x15.Pin.A1)
print(chan1.value, chan1.voltage)
print(chan2.value, chan2.voltage)