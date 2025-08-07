import time
import smbus2

# MMC56x3 I2C address
I2C_ADDRESS = 0x30

# MMC56x3 register addresses
REG_XOUT_L = 0x01
REG_YOUT_L = 0x03
REG_ZOUT_L = 0x05
REG_STATUS = 0x06
REG_CTRL0 = 0x07
REG_CTRL1 = 0x08
REG_CTRL2 = 0x09
REG_CTRL3 = 0x0A

# I2C bus number for the Jetson Orin Nano
I2C_BUS_NUM = 7  # Check with 'i2cdetect -y 7'

# Initialize I2C bus
try:
    bus = smbus2.SMBus(I2C_BUS_NUM)
    print(f"I2C bus {I2C_BUS_NUM} initialized successfully.")
except FileNotFoundError:
    print(f"Error: I2C bus {I2C_BUS_NUM} not found. Please check your bus number.")
    exit()
except Exception as e:
    print(f"An error occurred during bus initialization: {e}")
    exit()


def initiate_measurement():
    """Triggers a single measurement on the MMC56x3."""
    try:
        # Write 0x01 to REG_CTRL0 to enable measurement
        bus.write_byte_data(I2C_ADDRESS, REG_CTRL0, 0x01)
        # Write 0x01 to REG_CTRL2 to start a single measurement
        bus.write_byte_data(I2C_ADDRESS, REG_CTRL2, 0x01)
        # 0x01 = SET bit
        # 0x02 = RESET bit
        # 0x04 = CM_EN (Continuous Mode)
        # 0x08 = One-time measurement
        # The correct way to start a measurement is to set the `CM_EN` bit for continuous mode or the one-time measurement bit.
    except Exception as e:
        print(f"Failed to initiate measurement: {e}")


def read_sensor_data():
    """Reads the raw magnetometer data from the MMC56x3."""
    try:
        # Wait until the data is ready
        status = 0
        while (status & 0x40) == 0:  # Data Ready bit (BIT 6)
            status = bus.read_byte_data(I2C_ADDRESS, REG_STATUS)
            time.sleep(0.01)  # Small delay to prevent busy-waiting

        # Read the 16-bit X-axis data (L and H bytes)
        x_L = bus.read_byte_data(I2C_ADDRESS, REG_XOUT_L)
        x_H = bus.read_byte_data(I2C_ADDRESS, REG_XOUT_L + 1)
        x_raw = (x_H << 8) | x_L

        # Read the 16-bit Y-axis data (L and H bytes)
        y_L = bus.read_byte_data(I2C_ADDRESS, REG_YOUT_L)
        y_H = bus.read_byte_data(I2C_ADDRESS, REG_YOUT_L + 1)
        y_raw = (y_H << 8) | y_L

        # Read the 16-bit Z-axis data (L and H bytes)
        z_L = bus.read_byte_data(I2C_ADDRESS, REG_ZOUT_L)
        z_H = bus.read_byte_data(I2C_ADDRESS, REG_ZOUT_L + 1)
        z_raw = (z_H << 8) | z_L

        return x_raw, y_raw, z_raw

    except Exception as e:
        print(f"An error occurred while reading data: {e}")
        return None, None, None


if __name__ == "__main__":
    while True:
        # 1. Trigger a new measurement
        initiate_measurement()

        # 2. Read the data after a short delay
        x, y, z = read_sensor_data()

        if x is not None:
            # Convert raw values to microtesla (uT)
            sensitivity = 0.0625  # uT/LSB from datasheet
            x_uT = x * sensitivity
            y_uT = y * sensitivity
            z_uT = z * sensitivity

            print(f"Raw: X={x}, Y={y}, Z={z}")
            print(f"uT: X={x_uT:.2f}, Y={y_uT:.2f}, Z={z_uT:.2f}")

        time.sleep(1)  # Wait 1 second before the next cycle