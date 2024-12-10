import os
import logging

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

from algoritms.in_out_functions import Io

logger = logging.getLogger()
logger.setLevel("INFO")


class SM4:
    """
    Class for SM4 cipher

    Args:
        None

    Methods:
        generate_key() -> bytes:
        Generate a 128-bit key for SM4
        encrypt(
            text_path: str, path_to_key: str, path_to_encrypted: str
        ) -> bytes:
        Encrypts the text using the SM4 algorithm
        decrypt(
            symmetric: str, path_to_encrypted: str, path_to_decrypted: str
        ) -> str:
        Decrypts the text using the SM4 algorithm
    """

    def __init__(self):
        pass

    @staticmethod
    def generate_key() -> bytes:
        """The function generates a fixed 128-bit key for SM4

        Returns:
            bytes: The generated key for SM4
        """
        key_size = 128
        logging.info("A 128-bit symmetric key for SM4 has been generated")
        return os.urandom(key_size // 8)

    @staticmethod
    def encrypt(
        text: str,
        path_to_key: str,
        path_to_encrypted: str,
    ) -> bytes:
        """The function encrypts text using the SM4 symmetric key with CBC mode

        Args:
            text(str): path to origin text
            path_to_key(str): path to symmetric key
            path_to_encrypted(str): path to save encrypted text

        Returns:
            bytes: encrypted text
        """
        text = Io.read_txt(text)
        symmetric_key = Io.deserialize_symmetric_key(path_to_key)

        iv = os.urandom(16)
    
        cipher = Cipher(algorithms.SM4(symmetric_key), modes.CBC(iv), default_backend())
        padder = padding.PKCS7(algorithms.SM4.block_size).padder()
        byte = bytes(text, "UTF-8")
        padded = padder.update(byte) + padder.finalize()
        encryptor = cipher.encryptor()
    
        encrypted = encryptor.update(padded) + encryptor.finalize()

        Io.write_bytes(path_to_encrypted, iv + encrypted)
    
        logging.info("The text has been successfully encrypted with SM4 in CBC mode")
        return encrypted

    @staticmethod
    def decrypt(
        symmetric: str,
        path_to_encrypted: str,
        path_to_decrypted: str,
    ) -> str:
        """The function decrypts text using the SM4 symmetric key with CBC mode

        Args:
            symmetric(str): path to symmetric key
            path_to_encrypted(str): path to encrypted text
            path_to_decrypted(str): path to decrypted text

        Returns:
            str: decrypted text
        """
        encrypted = Io.read_bytes(path_to_encrypted)
        symmetric_key = Io.deserialize_symmetric_key(symmetric)

        iv = encrypted[:16]
        encrypted_text = encrypted[16:]

        cipher = Cipher(algorithms.SM4(symmetric_key), modes.CBC(iv), default_backend())
        decryptor = cipher.decryptor()
    
        decrypted = decryptor.update(encrypted_text) + decryptor.finalize()

        unpadder = padding.PKCS7(algorithms.SM4.block_size).unpadder()
        unpadded = unpadder.update(decrypted) + unpadder.finalize()
        unpadded_text = unpadded.decode("UTF-8")

        Io.write_txt(unpadded_text, path_to_decrypted)
    
        logging.info("The text has been successfully decrypted with SM4 in CBC mode")
        return unpadded_text