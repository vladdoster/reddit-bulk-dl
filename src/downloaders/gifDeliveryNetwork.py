import os
import urllib.request

from bs4 import BeautifulSoup

from src.downloaders.downloaderUtils import getExtension, getFile
from src.errors import NotADownloadableLinkError
from src.utils import GLOBAL


class GifDeliveryNetwork:
    def __init__(self, directory, post):
        try:
            post["MEDIAURL"] = self.getLink(post["CONTENTURL"])
        except IndexError:
            raise NotADownloadableLinkError("Could not read the page source")

        post["EXTENSION"] = getExtension(post["MEDIAURL"])

        if not os.path.exists(directory):
            os.makedirs(directory)

        filename = GLOBAL.config["filename"].format(**post) + post["EXTENSION"]
        short_filename = post["POSTID"] + post["EXTENSION"]

        getFile(filename, short_filename, directory, post["MEDIAURL"])

    @staticmethod
    def getLink(url):
        """Extract direct link to the video from page's source
        and return it
        """
        if (
            ".webm" in url.split("/")[-1]
            or ".mp4" in url.split("/")[-1]
            or ".gif" in url.split("/")[-1]
        ):
            return url

        if url[-1:] == "/":
            url = url[:-1]

        url = "https://www.gifdeliverynetwork.com/" + url.split("/")[-1]
        page_source = urllib.request.urlopen(url).read().decode()

        soup = BeautifulSoup(page_source, "html.parser")
        attributes = {"id": "mp4Source", "type": "video/mp4"}
        content = soup.find("source", attrs=attributes)

        if content is None:
            raise NotADownloadableLinkError("Could not read the page source")

        return content["src"]
