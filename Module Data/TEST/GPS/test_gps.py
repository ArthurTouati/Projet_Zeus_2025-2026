import smbus2
import pynmea2
import time

# --- Configuration ---
# *** CHANGE THIS *** to the I2C bus number you found with i2cdetect
I2C_BUS_NUM = 7
SAM_M10Q_ADDR = 0x84  # Default u-blox I2C address
# ---------------------

def read_sam_m10q():
    """
    Reads and parses NMEA data from the SAM-M10Q GPS module over I2C.
    """
    try:
        bus = smbus2.SMBus(I2C_BUS_NUM)
        print(f"Successfully opened I2C bus {I2C_BUS_NUM}.")
        print("Reading GPS data... Press Ctrl+C to stop.")
        print("Waiting for a valid GPS fix...")
        
        read_buffer = b""

        while True:
            try:
                # u-blox modules stream data from the 0xFF register.
                # We read 32 bytes at a time, which is a common block size.
                data = bus.read_i2c_block_data(SAM_M10Q_ADDR, 0xFF, 32)
                
                read_buffer += data
                
                # Decode to string (ignoring errors) and split by NMEA sentence
                lines = read_buffer.decode('ascii', errors='ignore').split('\r\n')
                
                # Keep the last (likely incomplete) line for the next read
                # and re-encode it to bytes
                read_buffer = lines[-1].encode('ascii')
                
                # Process all complete lines
                for line in lines[:-1]:
                    if line.startswith('$GNGGA'):
                        try:
                            msg = pynmea2.parse(line)
                            
                            # Check if we have a valid GPS fix
                            # msg.gps_qual > 0 means we have a fix
                            if msg.is_valid and msg.gps_qual > 0:
                                print(f"\n--- Valid GPS Fix Acquired ---")
                                print(f"Timestamp: {msg.timestamp}")
                                print(f"Latitude:  {msg.latitude:.6f} {msg.lat_dir}")
                                print(f"Longitude: {msg.longitude:.6f} {msg.lon_dir}")
                                print(f"Altitude:  {msg.altitude} {msg.altitude_units}")
                                print(f"Fix Type:  {msg.gps_qual} (1=GPS, 2=DGPS, etc.)")
                                print(f"Sats Used: {msg.num_sats}")
                                print("-" * 30)
                            
                        except pynmea2.ParseError as e:
                            # Ignore lines that fail to parse (e.g., checksum error)
                            # print(f"Parse error: {e}")
                            pass

            except IOError as e:
                # Handle I2C read errors (e.g., sensor disconnected)
                print(f"I2C Error: {e}. Check connection.")
                time.sleep(2)
            
            # Don't hammer the I2C bus too hard
            time.sleep(0.1)

    except FileNotFoundError:
        print(f"Error: I2C bus {I2C_BUS_NUM} not found.")
        print("Please check your I2C_BUS_NUM variable and Jetson config.")
    except KeyboardInterrupt:
        print("\nStopping script.")
    finally:
        if 'bus' in locals():
            bus.close()
            print("I2C bus closed.")

if __name__ == "__main__":
    read_sam_m10q()
