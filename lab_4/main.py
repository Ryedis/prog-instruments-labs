import argparse
import logging
from algoritms.asymmetrical import RSA
from algoritms.symmetrical import SM4
from algoritms.in_out_functions import Io

def configure_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        filename="app.log",
        filemode="a",
    )
    return logging.getLogger(__name__)

logger = configure_logger()
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", type=str, help="Choose generate_key/encrypt/decrypt")
    args = parser.parse_args()
    setting = Io.read_json("setting.json")
    
    logger.info("Application started")

    match args.mode:
        case "generate_key":
            logger.info("Starting key generation...")
            try:
                symmetric_key = SM4.generate_key()
                Io.serialize_symmetric_key(symmetric_key, setting["symmetric_key"])
                logger.info(f"SM4 symmetric key saved to {setting['symmetric_key']}")

                public_key, private_key = RSA.key_generation()
                Io.serialize_public_key(setting["public_key"], public_key)
                Io.serialize_private_key(setting["private_key"], private_key)
                logger.info(f"RSA public and private keys saved to {setting['public_key']} and {setting['private_key']}")
            except Exception as e:
                logger.error(f"Error during key generation: {e}")

        case "encrypt":
            logger.info("Starting encryption process...")
            try:
                SM4.encrypt(
                    setting["origin_file"],
                    setting["symmetric_key"],
                    setting["encrypted_file"],
                )
                logger.info(f"File encrypted and saved to {setting['encrypted_file']}")

                RSA.encrypt(
                    setting["public_key"],
                    setting["symmetric_key"],
                    setting["encrypted_symmetric_key"],
                )
                logger.info(f"Symmetric key encrypted and saved to {setting['encrypted_symmetric_key']}")
            except Exception as e:
                logger.error(f"Error during encryption: {e}")

        case "decrypt":
            logger.info("Starting decryption process...")
            try:
                RSA.decrypt(
                    setting["private_key"],
                    setting["encrypted_symmetric_key"],
                    setting["decrypted_symmetric_key"],
                )
                logger.info(f"Symmetric key decrypted and saved to {setting['decrypted_symmetric_key']}")

                SM4.decrypt(
                    setting["symmetric_key"],
                    setting["encrypted_file"],
                    setting["decrypted_file"],
                )
                logger.info(f"File decrypted and saved to {setting['decrypted_file']}")
            except Exception as e:
                logger.error(f"Error during decryption: {e}")

        case _:
            logger.error("Invalid mode selected. Exiting application.")
            print("No such function. Try again and enter << generate_key OR encrypt OR decrypt >>")
    
    logger.info("Application finished")


if __name__ == "__main__":
    main()

#python main.py generate_key
#python main.py encrypt
#python main.py decrypt