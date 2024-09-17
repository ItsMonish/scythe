from config import *
from .sneaks import obfuscation

def makeConfig() -> None:
    METHODS["sneak"] = getSneak(PARAM["sneak"])

def getSneak(param: str) -> object:
    match param:
        case "aes128":
            return obfuscation.aes128
        case "aes192":
            return obfuscation.aes192
        case "aes256":
            return obfuscation.aes256
        case "base64":
            return obfuscation.base64
        case _:
            return obfuscation.nothing