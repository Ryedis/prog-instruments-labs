import logging
import json


from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import (
    load_pem_public_key,
    load_pem_private_key,
)
from cryptography.hazmat.primitives.asymmetric import rsa


class Io:
    """
    Class for input output

    Args:
        None

    Methods:
        read_json(path: str) -> dict:
            The function reads data from .json file
        write_txt(data: str, file_path: str) -> None:
            The function writes data into the file at the specified path
        read_txt(file_path: str) -> str:
            The function reads the file at the specified path and saves it to a variable
        write_bytes(file_path: str, data: str) -> None:
            The function writes bytes into a file
        read_bytes(file_path: str) -> str:
            The function reads file data
        serialize_symmetric_key(key: bytes, file_path: str) -> None:
            The function writes a symmetric key into a file
        deserialize_symmetric_key(file_path: str) -> bytes:
            The function deserializes the symmetric encryption key
        serialize_public_key(public_pem: str, public_key: rsa.RSAPublicKey) -> None:
            The function makes the RSA public key serialization
        serialize_private_key(private_pem: str, private_key: rsa.RSAPrivateKey) -> None:
            The function serializes a RSA private key
        deserialize_public_key(public_pem: str) -> rsa.RSAPublicKey:
            The function deserializes a RSA public key
        deserialize_private_key(private_pem: str) -> rsa.RSAPrivateKey:
            The function deserializes a RSA private key
    """
    def __init__(self):
        pass

    def read_json(path: str) -> dict:
        """The function reads data from .json file
        Args:
            path(str): path to json file
        Returns:
            dict: data
        """
        with open(path, "r", encoding="UTF-8") as file:
            return json.load(file)

    def write_txt(data: str, file_path: str) -> None:
        """The function writes data into the file at the specified path

        Args:
            data(str): the data which needs to be into the file
            file_path(str): path to the file where data was saved
        """
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(data)
        except Exception as e:
            logging.error(f'Error while writing the file: {e}')

    def read_txt(file_path: str) -> str:
        """The function reads the file at the specified path and saves it to a variable

        Args:
            file_path(str): Path to a file

        Returns:
            str: a variable contains data from the file
        """
        try:
            with open(file_path, "r", encoding="UTF-8") as file:
                return file.read()
        except Exception as e:
            logging.error(f'Error while reading the file: {e}')

    def write_bytes(file_path: str, data: str) -> None:
        """The function writes bytes into a file
        Args:
            file_path(str): path to file
            data(str): data needed to be written
        """
        try:
            with open(file_path, "wb") as file:
                file.write(data)
        except Exception as e:
            logging.error(f'Error while writing the file: {e}')

    def read_bytes(file_path: str) -> str:
        """The function reads file data
        Args:
            file_path(str): path to file
        Returns:
            str: data
        """
        try:
            with open(file_path, "rb") as file:
                data = file.read()
            return data
        except Exception as e:
            logging.error(f'Error while reading the file: {e}')

    def serialize_symmetric_key(key: bytes, file_path: str) -> None:
        """The function writes a symmetric key into a file

        Args:
            key(bytes): The symmetric key to write.
            file_path(str): The path of the file to write the key to.
        """
        try:
            with open(file_path, 'wb') as f:
                f.write(key)
        except Exception as e:
            logging.error(f'Error writing symmetric key to file: {e}')

    def deserialize_symmetric_key(file_path: str) -> bytes:
        """The function deserializes the symmetric encryption key
        Args:
            file_path(str): file_path for deserialization
        Returns:
            bytes: symmetric key
        """
        try:
            with open(file_path, "rb") as key_file:
                return key_file.read()
        except Exception as e:
            logging.error(f'Error while deserialization the key: {e}')

    def serialize_public_key(public_pem: str, public_key: rsa.RSAPublicKey) -> None:
        """The function makes the RSA public key serialization
        Args:
            public_pem(str): file_path for public RSA key serialization
            public_key(str): public RSA-key
        """
        try:
            with open(public_pem, "wb") as public_out:
                public_out.write(
                    public_key.public_bytes(
                        encoding=serialization.Encoding.PEM,
                        format=serialization.PublicFormat.SubjectPublicKeyInfo,
                    )
                )
        except Exception as e:
            logging.error(f'Error while serialization the key: {e}')

    def serialize_private_key(private_pem: str, private_key: rsa.RSAPrivateKey) -> None:
        """The function serializes a RSA private key
        Args:
            private_pem(str): file_path for private RSA key serialization
            private_key(rsa.RSAPrivateKey): private RSA-key
        """
        try:
            with open(private_pem, "wb") as private_out:
                private_out.write(
                    private_key.private_bytes(
                        encoding=serialization.Encoding.PEM,
                        format=serialization.PrivateFormat.TraditionalOpenSSL,
                        encryption_algorithm=serialization.NoEncryption(),
                    )
                )
        except Exception as e:
            logging.error(f'Error while serialization the key: {e}')

    def deserialize_public_key(public_pem: str) -> rsa.RSAPublicKey:
        """The function deserializes a RSA public key
        Args:
            public_pem(str): file_path for public RSA key deserialization
        Returns:
            rsa.RSAPublicKey: RSA public Key
        """
        try:
            with open(public_pem, "rb") as pem_in:
                public_bytes = pem_in.read()
            return load_pem_public_key(public_bytes)
        except Exception as e:
            logging.error(f'Error while deserialization the key: {e}')

    def deserialize_private_key(private_pem: str) -> rsa.RSAPrivateKey:
        """The function deserializes a RSA private key
        Args:
            private_pem(str): file_path for private RSA key deserialization
        Returns:
            rsa.RSAPrivateKey: RSA private Key
        """
        try:
            with open(private_pem, "rb") as pem_in:
                private_bytes = pem_in.read()
            return load_pem_private_key(
                private_bytes,
                password=None,
            )
        except Exception as e:
            logging.error(f'Error while deserialization the key: {e}')
             
