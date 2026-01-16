import board
import busio
import pynmea2
import numpy as np


# On n'utilise plus smbus2

class GPSHandler:
    def __init__(self,i2c):
        # Coordinate :
        self.x = []
        self.y = []
        self.z = []

        # Constant :
        self.EARTH_RADIUS = 6371000

        # Export dict :
        self.header = ['x', 'y', 'z']
        self.gps_dict = dict.fromkeys(self.header)

        # --- NOUVEAU CODE INIT ---
        self.SAM_M10Q_ADDR = 0x42

        # board.SCL et SDA trouvent automatiquement le bon bus (8 sur Orin Nano)
        self.i2c = i2c

        self.read_buffer = b""

    def convert_lat_long_to_xy(self, lat, long, altitude):
        lat_rad = lat * (np.pi / 180)
        lon_rad = long * (np.pi / 180)
        r = self.EARTH_RADIUS + altitude
        self.x.append(r * np.cos(lat_rad) * np.cos(lon_rad))
        self.y.append(r * np.cos(lat_rad) * np.sin(lon_rad))
        self.z.append(r * np.sin(lat_rad))

    def export_to_dict(self):
        self.gps_dict['x'] = self.x
        self.gps_dict['y'] = self.y
        self.gps_dict['z'] = self.z
        return self.gps_dict

    def clear_dict(self):
        self.gps_dict.clear()
        self.x.clear()
        self.y.clear()
        self.z.clear()

    def read_data(self):
        # Avec busio, il faut TOUJOURS verrouiller le bus avant de l'utiliser
        while not self.i2c.try_lock():
            pass

        try:
            # --- ÉTAPE 1 : Lire la taille (Registres 0xFD/0xFE) ---
            # Equivalent de : write(0xFD) -> restart -> read(2 bytes)
            cmd_avail = bytes([0xFD])
            buf_avail = bytearray(2)

            # writeto_then_readfrom gère le "Repeated Start" automatiquement
            self.i2c.writeto_then_readfrom(self.SAM_M10Q_ADDR, cmd_avail, buf_avail)

            num_bytes = (buf_avail[0] << 8) | buf_avail[1]

            # --- ÉTAPE 2 : Lire les données (Registre 0xFF) ---
            if num_bytes > 0:
                to_read = min(num_bytes, 32)

                cmd_data = bytes([0xFF])
                buf_data = bytearray(to_read)

                self.i2c.writeto_then_readfrom(self.SAM_M10Q_ADDR, cmd_data, buf_data)

                # Ajout au buffer principal
                self.read_buffer += bytes(buf_data)

                # --- ÉTAPE 3 : Décodage (Identique à avant) ---
                try:
                    decoded_str = self.read_buffer.decode('ascii', errors='ignore')
                    if '\r\n' in decoded_str:
                        lines = decoded_str.split('\r\n')
                        self.read_buffer = lines[-1].encode('ascii')

                        for line in lines[:-1]:
                            # print(f"GPS: {line}") # Debug
                            if line.startswith('$GNGGA'):
                                try:
                                    msg = pynmea2.parse(line)
                                    if msg.is_valid and msg.gps_qual > 0:
                                        lat = msg.latitude
                                        long = msg.longitude
                                        alt = msg.altitude
                                        self.convert_lat_long_to_xy(lat, long, alt)
                                except pynmea2.ParseError:
                                    pass
                except Exception:
                    pass

        except Exception as e:
            # print(f"Erreur I2C: {e}")
            pass

        finally:
            # TRES IMPORTANT : Toujours déverrouiller le bus à la fin
            self.i2c.unlock()