import board
import busio
import pynmea2
import time

# --- Configuration ---
SAM_M10Q_ADDR = 0x42  # Adresse correcte (7-bit) pour u-blox
I2C_FREQ = 100000  # 100kHz pour une meilleure stabilité


def read_sam_m10q():
    """
    Lit et décode les données NMEA du module GPS SAM-M10Q via I2C.
    """
    try:
        # Initialisation du bus I2C (board.SCL/SDA sélectionnent le bon bus sur Orin Nano)
        i2c = busio.I2C(board.SCL, board.SDA, frequency=I2C_FREQ)
        print(f"Bus I2C ouvert avec succès.")
        print("En attente d'un signal GPS (Fix)... Appuyez sur Ctrl+C pour arrêter.")

        read_buffer = b""

    except Exception as e:
        print(f"Erreur d'initialisation I2C : {e}")
        return

    try:
        while True:
            # TENTATIVE DE VERROUILLAGE DU BUS
            if i2c.try_lock():
                try:
                    # 1. Demander au GPS combien d'octets sont disponibles (Registres 0xFD/0xFE)
                    size_reg = bytes([0xFD])
                    size_data = bytearray(2)
                    i2c.writeto_then_readfrom(SAM_M10Q_ADDR, size_reg, size_data)

                    num_bytes = (size_data[0] << 8) | size_data[1]

                    # 2. Si des données sont disponibles, on les lit via le registre 0xFF
                    if 0 < num_bytes < 0xFFFF:
                        # On lit par blocs de 64 octets maximum pour ne pas saturer le bus
                        to_read = min(num_bytes, 64)
                        data_in = bytearray(to_read)

                        i2c.writeto_then_readfrom(SAM_M10Q_ADDR, bytes([0xFF]), data_in)
                        read_buffer += data_in

                        # 3. Décodage des trames NMEA
                        try:
                            decoded_str = read_buffer.decode('ascii', errors='ignore')
                            if '\r\n' in decoded_str:
                                lines = decoded_str.split('\r\n')
                                # On garde le dernier fragment incomplet dans le buffer
                                read_buffer = lines[-1].encode('ascii')

                                for line in lines[:-1]:
                                    if line.startswith('$GNGGA'):
                                        try:
                                            msg = pynmea2.parse(line)
                                            if msg.gps_qual > 0:
                                                print(f"\n[FIX ACQUIS] Satellites: {msg.num_sats}")
                                                print(
                                                    f"Lat: {msg.latitude:.6f} | Lon: {msg.longitude:.6f} | Alt: {msg.altitude}m")
                                            else:
                                                print("Signal faible : Recherche de satellites...", end='\r')
                                        except pynmea2.ParseError:
                                            pass
                        except Exception as e:
                            print(f"Erreur décodage : {e}")

                except OSError as e:
                    # L'erreur 121 (NACK) sera captée ici
                    print(f"Erreur I2C (0x42): {e}. Vérifiez le câblage.")

                finally:
                    # LIBÉRATION DU BUS (Crucial)
                    i2c.unlock()

            # Pause pour laisser le processeur souffler et le GPS remplir son buffer
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nArrêt du script.")
    finally:
        # Nettoyage final
        i2c.deinit()


if __name__ == "__main__":
    read_sam_m10q()