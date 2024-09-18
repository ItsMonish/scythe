from typing import Callable, Dict, Any

PARAM: dict[str, str] = dict()
METHODS: Dict[str, Callable[..., Any]] = dict()

def update(argline: list) -> None:
    for i in range(0, len(argline)):
        match argline[i]:
            case "mode":
                if argline[i+1] in ["server","listen"]:
                    PARAM["mode"] = "listen"
                    i += 1
            case "sneak":
                PARAM["sneak"] = argline[i+1]
                i += 1
            case "key":
                PARAM["key"] = argline[i+1]
                i += 1
            case "interval":
                PARAM["interval"] = argline[i+1]
                i += 1
            case "repo":
                PARAM["repo"] = argline[i+1]
                i += 1
            case _:
                continue
    if(PARAM.get("repo") == None):
        raise Exception("Repository required to start")