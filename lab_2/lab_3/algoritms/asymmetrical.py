import logging

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa

from algoritms.in_out_functions import Io


logger = logging.getLogger()
logger.setLevel("INFO")


class RSA:
    """
    Class for RSA cipher

    Args:
        None

    Methods:
        key_generation() -> tuple[rsa.RSAPublicKey, rsa.RSAPrivateKey]: 
        Generats keys for RSA
        encrypt(
            public: str, path_to_key: str, path_for_encripted: str
        ) -> None: 
        Encrypts the text
        decrypt(
            private: str, path_to_encripted: str, path_to_decripted: str
        ) -> bytes:
        Decrypts the text
    """
    def __init__(self):
        pass

    def key_generation() -> tuple[rsa.RSAPublicKey, rsa.RSAPrivateKey]:
        """The function generates asymmetric keys (public and private)

        Returns:
            tuple[rsa.RSAPublicKey, rsa.RSAPrivateKey]: public and private keys
        """
        key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        logging.info("Asymmetric keys have been generated")
        return key.public_key(), key

    def encrypt(
        public: str,
        path_to_key: str,
        path_to_encrypted: str
    ) -> None:
        """The function encripts symmetric key by asymmetric public key

        Args:
            public(str): path to public asymmetric key
            path_to_key(str): path to symmetric key
            path_for_encripted(str): path to save encripted symmetric key
        """
        symmetric_key = Io.deserialize_symmetric_key(path_to_key)
        public_key = Io.deserialize_public_key(public)
        encripted_key = public_key.encrypt(
            symmetric_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
        Io.write_bytes(path_to_encrypted, encripted_key)
        logging.info(f"Encrypted symmetric key saved to {path_to_encrypted}")

    def decrypt(
        private: str,
        path_to_encrypted: str,
        path_to_decrypted: str
    ) -> bytes:
        """The function decripts symmetric key by asymmetric private key

        Args:
            private(str): path to private asymmetric key
            path_to_encrypted(str): path to encrypted symmetric key
            path_to_decrypted(str): path to decrypted symmetric key

        Returns:
            bytes: decrypted key
        """
        symmetric_encripted = Io.deserialize_symmetric_key(path_to_encrypted)
        private_key = Io.deserialize_private_key(private)
        decripted_key = private_key.decrypt(
            symmetric_encripted,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
        Io.serialize_symmetric_key(decripted_key, path_to_decrypted)
        logging.info(f"Decrypted symmetric key saved to {path_to_decrypted}")
        return decripted_key
 