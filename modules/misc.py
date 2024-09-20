from io import BytesIO
from PIL import ImageGrab
from time import sleep

def grabSS(delay: int = 0) -> str:
    sleep(delay)
    img = ImageGrab.grab()
    imgBytes = BytesIO()
    img.save(imgBytes, format="JPEG")
    return imgBytes.getvalue().hex()