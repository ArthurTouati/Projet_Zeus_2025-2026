import board
import busio
import time
from adafruit_bus_device.i2c_device import I2CDevice

# --- Configuration ---
# This MUST match the address in the Arduino code
ESP32_ADDRESS = 0x08
# This MUST match the length in the Arduino code
STRING_LENGTH = 10

# Initialize the I2C bus.
# 'board.SCL' and 'board.SDA' will automatically find the
# correct I2C bus (e.g., bus 7) on the Jetson's 40-pin header.
try:
    i2c = busio.I2C(board.SCL, board.SDA)
    print("I2C Bus initialized successfully.")
except ValueError:
    print("I2C Error: Could not initialize I2C bus.")
    print("Make sure Jetson.GPIO is installed and user has I2C permissions.")
    exit()
except NotImplementedError:
    print("I2C Error: SCL/SDA pins not found for this board.")
    print("Please ensure Adafruit Blinka is correctly set up for Jetson.")
    exit()


# Create an I2CDevice object to represent the ESP32 slave
# This manages locking the bus for communication
try:
    esp32_device = I2CDevice(i2c, ESP32_ADDRESS)
    print(f"Locked onto ESP32 at address 0x{ESP32_ADDRESS:02X}")
except ValueError:
    print(f"I2C Error: No device found at address 0x{ESP32_ADDRESS:02X}")
    print("Please check wiring, ESP32 code, and I2C address.")
    exit()


def read_string_from_esp32():
    try:
        # Create a buffer to store the incoming bytes
        in_buffer = bytearray(STRING_LENGTH)
        
        # Use a context manager to lock the I2C bus and communicate
        with esp32_device:
            # Read STRING_LENGTH bytes from the device into the buffer
            esp32_device.readinto(in_buffer)
            
        # Decode the bytes into a UTF-8 string
        received_string = in_buffer.decode('utf-8')
        
        print(f"Received from ESP32: '{received_string}'")
        
    except (IOError, OSError) as e:
        print(f"I2C Communication Error: {e}")
        print("Lost connection to ESP32? Check wiring.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def main():
    print("Starting I2C Master (using busio/board)")
    print(f"Polling ESP32 (Address 0x{ESP32_ADDRESS:02X}) every 2 seconds...")
    
    while True:
        read_string_from_esp32()
        time.sleep(2) # Poll every 2 seconds

if __name__ == "__main__":
    main()
