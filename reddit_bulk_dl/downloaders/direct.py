import os

from downloaders.downloaderUtils import getFile, getExtension
from utils import GLOBAL


class Direct:
    def __init__(self, dir, POST):
        POST["EXTENSION"] = getExtension(POST["CONTENTURL"])
        if not os.path.exists(dir):
            os.makedirs(dir)

        f_name = GLOBAL.config["f_name"].format(**POST) + POST["EXTENSION"]
        shortf_name = POST["POSTID"] + POST["EXTENSION"]

        getFile(f_name, shortf_name, dir, POST["CONTENTURL"])
