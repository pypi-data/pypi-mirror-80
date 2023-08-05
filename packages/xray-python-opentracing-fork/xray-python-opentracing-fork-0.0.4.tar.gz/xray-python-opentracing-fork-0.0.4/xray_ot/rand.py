import binascii
import os


def generate_64bit_id_as_hex() -> str:
    return binascii.b2a_hex(os.urandom(8)).decode("ascii")
