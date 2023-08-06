import os
import inspect
import json
import icon

server = None
cert = None
keep_passwd = False
elevate = None
TRAY_ICON = os.path.dirname(inspect.getfile(icon)) + '/lockWithe.png'
TRAY_ICON_OK = os.path.dirname(inspect.getfile(icon)) + '/lockGreen.png'
TRAY_ICON_ERROR = os.path.dirname(inspect.getfile(icon)) + '/lockRed.png'


def init():
    with open(os.environ["HOME"] + "/.config/snxtray.json") as json_file:
        data = json.load(json_file)
        globals()["server"] = data["server"]
        globals()["cert"] = data["cert"]
        if "keep_passwd" in data.keys():
            globals()["keep_passwd"] = data["keep_passwd"]
        if "elevate" in data.keys():
            globals()["elevate"] = data["elevate"]
