import io
import os
from pathlib import Path

from errors import FileAlreadyExistsError, TypeInSkip
from utils import GLOBAL

VanillaPrint = print
from utils import printToFile as print


class SelfPost:
    def __init__(self, dir, post):

        if "self" in GLOBAL.arguments.skip:
            raise TypeInSkip

        if not os.path.exists(dir):
            os.makedirs(dir)

        f_name = GLOBAL.config["f_name"].format(**post)

        fileDir = dir / (f_name + ".md")
        print(fileDir)
        print(f_name + ".md")

        if Path.is_file(fileDir):
            raise FileAlreadyExistsError

        try:
            self.writeToFile(fileDir, post)
        except FileNotFoundError:
            fileDir = post["POSTID"] + ".md"
            fileDir = dir / fileDir

            self.writeToFile(fileDir, post)

    @staticmethod
    def writeToFile(dir, post):

        """Self posts are formatted here"""
        content = (
            "## ["
            + post["TITLE"]
            + "]("
            + post["CONTENTURL"]
            + ")\n"
            + post["CONTENT"]
            + "\n\n---\n\n"
            + "submitted to [r/"
            + post["SUBREDDIT"]
            + "](https://www.reddit.com/r/"
            + post["SUBREDDIT"]
            + ") by [u/"
            + post["REDDITOR"]
            + "](https://www.reddit.com/user/"
            + post["REDDITOR"]
            + ")"
        )

        with io.open(dir, "w", encoding="utf-8") as FILE:
            VanillaPrint(content, file=FILE)

        print("Downloaded")
