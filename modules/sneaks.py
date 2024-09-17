from base64 import b64encode
from config import PARAM
from .cryptos import AESModule

class obfuscation:
    @staticmethod
    def nothing(con: str) -> str:
        return con

    @staticmethod
    def base64(con: str) -> str:
        return b64encode(con.encode()).decode()
    
    @staticmethod
    def aes128(con: str) -> str:
        key = PARAM["key"]
        aes = AESModule(128, key)
        return aes.encrypt(con)
    
    @staticmethod
    def aes192(con: str) -> str:
        key = PARAM["key"]
        aes = AESModule(192, key)
        return aes.encrypt(con)
    
    @staticmethod
    def aes256(con: str) -> str:
        key = PARAM["key"]
        aes = AESModule(256, key)
        return aes.encrypt(con)
