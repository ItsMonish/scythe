import requests

def isCxnActive() -> bool:
    urls = ["https://google.com", "https://duckduckgo.com", "https://bing.com"]
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