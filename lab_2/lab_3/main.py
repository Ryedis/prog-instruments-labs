import argparse
import logging

from algoritms.asymmetrical import RSA
from algoritms.in_out_functions import Io
from algoritms.symmetrical import SM4

logger = logging.getLogger()
logger.setLevel("INFO")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "mode", type=str, help="Choose generate_key/encrypt/decrypt"
    )
    args = parser.parse_args()
    setting = Io.read_json("setting.json")

    match args.mode:
        case "generate_key":
            logging.info("Starting key generation...")
            symmetric_key = SM4.generate_key()
            Io.serialize_symmetric_key(symmetric_key, setting["symmetric_key"])
            logging.info(f"SM4 symmetric key saved to {setting['symmetric_key']}")

            public_key, private_key = RSA.key_generation()
            Io.serialize_public_key(setting["public_key"], public_key)
            Io.serialize_private_key(setting["private_key"], private_key)
            logging.info(f"RSA public and private keys saved to {setting['public_key']} and {setting['private_key']}")
        
        case "encrypt":
            logging.info("Starting encryption process...")
            encrypted = SM4.encrypt(
                setting["origin_file"],
                setting["symmetric_key"],
                setting["encrypted_file"],
            )
            logging.info(f"File encrypted and saved to {setting['encrypted_file']}")

            RSA.encrypt(
                setting["public_key"],
                setting["symmetric_key"],
                setting["encrypted_symmetric_key"],
            )
            logging.info(f"Symmetric key encrypted and saved to {setting['encrypted_symmetric_key']}")
        
        case "decrypt":
            logging.info("Starting decryption process...")
            RSA.decrypt(
                setting["private_key"],
                setting["encrypted_symmetric_key"],
                setting["decrypted_symmetric_key"],
            )
            logging.info(f"Symmetric key decrypted and saved to {setting['decrypted_symmetric_key']}")

            decrypted = SM4.decrypt(
                setting["symmetric_key"],
                setting["encrypted_file"],
                setting["decrypted_file"],
            )
            logging.info(f"File decrypted and saved to {setting['decrypted_file']}")
        
        case _:
            logging.error("Invalid mode. Try again and enter 'generate_key', 'encrypt', or 'decrypt'")
            print(
                "No such function. Try again and enter << generate_key OR encrypt OR decrypt >>"
            )


if __name__ == "__main__":
    main()

#python main.py generate_key
#python main.py encrypt
#python main.py decrypt