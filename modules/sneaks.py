from base64 import b64encode, b64decode
from config import PARAM
from .cryptos import AESModule


class obfuscation:
    SNEAKS = {
        "nothing": lambda con: obfuscation.nothing(con),
        "base64": lambda con: obfuscation.base64(con),
        "aes128": lambda con: obfuscation.aes128(con),
        "aes192": lambda con: obfuscation.aes192(con),
        "aes256": lambda con: obfuscation.aes256(con),
    }

    DSNEAKS = {
        "nothing": lambda con: obfuscation.nothing(con),
        "base64": lambda con: obfuscation.deBase64(con),
        "aes128": lambda con: obfuscation.deAes128(con),
        "aes192": lambda con: obfuscation.deAes192(con),
        "aes256": lambda con: obfuscation.deAes256(con),
    }

    @staticmethod
    def nothing(con: str) -> str:
        return con

    @staticmethod
    def base64(con: str) -> str:
        return b64encode(con.encode()).decode()

    @staticmethod
    def deBase64(con: str) -> str:
        return b64decode(con).decode()

    @staticmethod
    def aes128(con: str) -> str:
        key = PARAM["key"]
        aes = AESModule(128, key)
        return aes.encrypt(con)

    @staticmethod
    def deAes128(con: str) -> str:
        key = PARAM["key"]
        aes = AESModule(128, key)
        return aes.decrypt(con)

    @staticmethod
    def aes192(con: str) -> str:
        key = PARAM["key"]
        aes = AESModule(192, key)
        return aes.encrypt(con)

    @staticmethod
    def deAes192(con: str) -> str:
        key = PARAM["key"]
        aes = AESModule(192, key)
        return aes.decrypt(con)

    @staticmethod
    def aes256(con: str) -> str:
        key = PARAM["key"]
        aes = AESModule(256, key)
        return aes.encrypt(con)

    @staticmethod
    def deAes256(con: str) -> str:
        key = PARAM["key"]
        aes = AESModule(256, key)
        return aes.decrypt(con)
