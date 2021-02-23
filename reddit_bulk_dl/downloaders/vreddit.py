import os
import subprocess

from downloaders.downloaderUtils import getFile
from utils import GLOBAL
from utils import printToFile as print


class VReddit:
    def __init__(self, dir, post):
        extension = ".mp4"
        if not os.path.exists(dir):
            os.makedirs(dir)

        f_name = GLOBAL.config["f_name"].format(**post) + extension
        shortf_name = post["POSTID"] + extension

        try:
            FNULL = open(os.devnull, "w")
            subprocess.call("ffmpeg", stdout=FNULL, stderr=subprocess.STDOUT)
        except:
            getFile(f_name, shortf_name, dir, post["CONTENTURL"])
            print("FFMPEG library not found, skipping merging video and audio")
        else:
            videoName = post["POSTID"] + "_video"
            videoURL = post["CONTENTURL"]
            audioName = post["POSTID"] + "_audio"
            audioURL = videoURL[: videoURL.rfind("/")] + "/DASH_audio.mp4"

            print(dir, f_name, sep="\n")

            getFile(videoName, videoName, dir, videoURL, silent=True)
            getFile(audioName, audioName, dir, audioURL, silent=True)
            try:
                self._mergeAudio(videoName, audioName, f_name, shortf_name, dir)
            except KeyboardInterrupt:
                os.remove(dir / f_name)
                os.remove(dir / audioName)

                os.rename(dir / videoName, dir / f_name)

    @staticmethod
    def _mergeAudio(video, audio, f_name, shortf_name, dir):

        inputVideo = str(dir / video)
        inputAudio = str(dir / audio)

        FNULL = open(os.devnull, "w")
        cmd = f"ffmpeg -i {inputAudio} -i {inputVideo} -c:v copy -c:a aac -strict experimental {str(dir / f_name)}"
        subprocess.call(cmd.split(), stdout=FNULL, stderr=subprocess.STDOUT)

        os.remove(dir / video)
        os.remove(dir / audio)
