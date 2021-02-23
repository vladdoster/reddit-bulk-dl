import os
import sys

import youtube_dl

from downloaders.downloaderUtils import createHash
from errors import FileAlreadyExistsError
from utils import GLOBAL
from utils import printToFile as print


class Youtube:
    def __init__(self, dir, post):
        if not os.path.exists(dir):
            os.makedirs(dir)

        f_name = GLOBAL.config["f_name"].format(**post)
        print(f_name)

        self.download(f_name, dir, post["CONTENTURL"])

    def download(self, f_name, dir, url):
        ydl_opts = {
            "format": "best",
            "outtmpl": str(dir / (f_name + ".%(ext)s")),
            "progress_hooks": [self._hook],
            "playlistend": 1,
            "nooverwrites": True,
            "quiet": True,
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        location = dir / (f_name + ".mp4")

        if GLOBAL.arguments.no_dupes:
            try:
                fileHash = createHash(location)
            except FileNotFoundError:
                return None
            if fileHash in GLOBAL.downloadedPosts():
                os.remove(location)
                raise FileAlreadyExistsError
            GLOBAL.downloadedPosts.add(fileHash)

    @staticmethod
    def _hook(d):
        if d["status"] == "finished":
            return print("Downloaded")
        downloadedMbs = int(d["downloaded_bytes"] * (10 ** (-6)))
        fileSize = int(d["total_bytes"] * (10 ** (-6)))
        sys.stdout.write("{}Mb/{}Mb\r".format(downloadedMbs, fileSize))
        sys.stdout.flush()
