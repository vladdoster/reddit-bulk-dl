import os
import subprocess

from src.downloaders.downloaderUtils import getFile
from src.utils import GLOBAL
from src.utils import printToFile as print


class VReddit:
    def __init__(self, directory, post):
        extension = ".mp4"
        if not os.path.exists(directory):
            os.makedirs(directory)

        filename = GLOBAL.config["filename"].format(**post) + extension
        short_filename = post["POSTID"] + extension

        try:
            fnull = open(os.devnull, "w")
            subprocess.call("ffmpeg", stdout=fnull, stderr=subprocess.STDOUT)
        except Exception:
            getFile(filename, short_filename, directory, post["CONTENTURL"])
            print("FFMPEG library not found, skipping merging video and audio")
        else:
            video_name = post["POSTID"] + "_video"
            video_url = post["CONTENTURL"]
            audio_name = post["POSTID"] + "_audio"
            audio_url = video_url[: video_url.rfind("/")] + "/DASH_audio.mp4"

            print(directory, filename, sep="\n")

            getFile(video_name, video_name, directory, video_url, silent=True)
            getFile(audio_name, audio_name, directory, audio_url, silent=True)
            try:
                self._mergeAudio(
                    video_name, audio_name, filename, short_filename, directory
                )
            except KeyboardInterrupt:
                os.remove(directory / filename)
                os.remove(directory / audio_name)
                os.rename(directory / video_name, directory / filename)

    @staticmethod
    def _mergeAudio(video, audio, filename, short_filename, directory):
        input_video = str(directory / video)
        input_audio = str(directory / audio)

        fnull = open(os.devnull, "w")
        cmd = "ffmpeg -i {} -i {} -c:v copy -c:a aac -strict experimental {}".format(
            input_audio, input_video, str(directory / filename)
        )
        subprocess.call(cmd.split(), stdout=fnull, stderr=subprocess.STDOUT)

        os.remove(directory / video)
        os.remove(directory / audio)
