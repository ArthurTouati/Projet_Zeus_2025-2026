import smbus2
import time

# Adresse I2C de l'ESP32
I2C_ADDRESS = 0x20
# Numéro du bus I2C (généralement 1 sur la Jetson Orin Nano)
I2C_BUS = 1
# Taille du tampon de données
BUFFER_SIZE = 32

# Initialisation du bus I2C
bus = smbus2.SMBus(I2C_BUS)


def read_i2c_data():
    """
    Lit un bloc de données depuis l'ESP32 via I2C.
    """
    try:
        # La fonction read_i2c_block_data est idéale pour lire un tampon de données
        # Le premier paramètre est l'adresse de l'esclave.
        # Le second est la "commande" qui peut être utilisée par l'esclave (ici, on lit directement).
        # Le troisième est le nombre de bytes à lire.
        data_block = bus.read_i2c_block_data(I2C_ADDRESS, 0x00, BUFFER_SIZE)

        # Décoder les données reçues
        rx_data = "".join([chr(byte) for byte in data_block if byte != 0])

        if rx_data:
            print(f"Données reçues via I2C : {rx_data}")
        else:
            print("Pas de nouvelles données à lire.")

    except FileNotFoundError:
        print("Erreur : Bus I2C non trouvé. Vérifiez les permissions et l'activation.")
    except Exception as e:
        print(f"Erreur I2C : {e}")


if __name__ == "__main__":
    try:
        while True:
            read_i2c_data()
            time.sleep(1)  # Vérification toutes les secondes

    except KeyboardInterrupt:
        print("Arrêt du script.")
    finally:
        bus.close()