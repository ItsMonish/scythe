from config import *
from modules.configMaker import makeConfig
import requests
import sys

def isCxnActive() -> bool:
    urls = ["https://github.com", "https://google.com", "https://duckduckgo.com", "https://bing.com"]
    for url in urls:
        try:
            stat = requests.head(url, timeout=5).status_code
            if stat:
                return True
        except requests.ConnectionError:
            continue
    return False


if __name__ == "__main__":
    if(not isCxnActive()):
        exit(0)
    update(argline=sys.argv[1:])
    makeConfig()
    e = METHODS["sneak"]("hello there")
    print(e)
    