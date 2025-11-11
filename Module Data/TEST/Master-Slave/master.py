import board
import busio
import time
from adafruit_bus_device.i2c_device import I2CDevice

# --- Configuration ---
# This MUST match the address in the Arduino code
ESP32_ADDRESS = 0x08
# This MUST match the buffer size in the Arduino code
MAX_BUFFER_LEN = 20

# Initialize the I2C bus
try:
    i2c = busio.I2C(board.SCL, board.SDA)
    print("I2C Bus initialized successfully.")
except Exception as e:
    print(f"I2C Error: Could not initialize I2C bus: {e}")
    exit()

# Create an I2CDevice object to represent the ESP32 slave
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
        in_buffer = bytearray(MAX_BUFFER_LEN)

        # Use a context manager to lock the I2C bus and communicate
        with esp32_device:
            # Read MAX_BUFFER_LEN bytes from the device into the buffer
            esp32_device.readinto(in_buffer)

        # Decode the bytes into a UTF-8 string
        # This will look like 'Meteo-OK\x00\x00\x00\x00\x00...'
        received_string_raw = in_buffer.decode('utf-8')

        # KEY CHANGE: Strip all null characters ('\x00') from the right side
        received_string = received_string_raw.rstrip('\x00')

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
        time.sleep(2)  # Poll every 2 seconds


if __name__ == "__main__":
    main()