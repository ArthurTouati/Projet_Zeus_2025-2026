from datetime import datetime
from adafruit_bus_device.i2c_device import I2CDevice

class ESP32Handler:
    def __init__(self,i2c):
        # Recovered data :
        self.gt = []
        self.rt = []
        self.state = []

        # Constant :
        self.string_length = 20

        # Export dict :
        self.header = ['gt','st']
        self.esp32_dict = dict.fromkeys(self.header)

        # Init connection :
        self.address = 0x08
        self.esp32 = I2CDevice(i2c,self.address)

    def read_data(self):
        # Create a buffer to store the incoming bytes
        in_buffer = bytearray(self.string_length)

        # Use a context manager to lock the I2C bus and communicate
        with self.esp32:
            # Read MAX_BUFFER_LEN bytes from the device into the buffer
            self.esp32.readinto(in_buffer)

        # Decode the bytes into a UTF-8 string and strip all null characters ('\x00') from the right side
        self.state.append(in_buffer.decode('utf-8').rstrip('\x00'))
        self.gt.append(datetime.now().strftime('%H:%M:%S'))

    def export_to_dict(self):
        self.esp32_dict['gt'] = self.gt
        self.esp32_dict['st'] = self.state
        return self.esp32_dict

    def clear_dict(self):
        self.gt.clear()
        self.state.clear()
        self.esp32_dict.clear()