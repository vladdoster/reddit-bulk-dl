import os
import urllib.request
from html.parser import HTMLParser

from downloaders.downloaderUtils import getExtension
from downloaders.downloaderUtils import getFile
from errors import (
    AlbumNotDownloadedCompletely,
    NotADownloadableLinkError,
    FileAlreadyExistsError,
)
from utils import GLOBAL
from utils import printToFile as print


class Erome:
    def __init__(self, dir, post):
        try:
            IMAGES = self.getLinks(post["CONTENTURL"])
        except urllib.error.HTTPError:
            raise NotADownloadableLinkError("Not a downloadable link")

        imagesLenght = len(IMAGES)
        howManyDownloaded = imagesLenght
        duplicates = 0

        if imagesLenght == 1:

            extension = getExtension(IMAGES[0])

            """f_names are declared here"""

            f_name = GLOBAL.config["f_name"].format(**post) + post["EXTENSION"]
            shortf_name = post["POSTID"] + extension

            imageURL = IMAGES[0]
            if "https://" not in imageURL or "http://" not in imageURL:
                imageURL = "https://" + imageURL

            getFile(f_name, shortf_name, dir, imageURL)

        else:
            f_name = GLOBAL.config["f_name"].format(**post)

            print(f_name)

            folderDir = dir / f_name

            try:
                if not os.path.exists(folderDir):
                    os.makedirs(folderDir)
            except FileNotFoundError:
                folderDir = dir / post["POSTID"]
                os.makedirs(folderDir)

            for i in range(imagesLenght):

                extension = getExtension(IMAGES[i])

                f_name = str(i + 1) + extension
                imageURL = IMAGES[i]
                if "https://" not in imageURL and "http://" not in imageURL:
                    imageURL = "https://" + imageURL

                print("  ({}/{})".format(i + 1, imagesLenght))
                print("  {}".format(f_name))

                try:
                    getFile(f_name, f_name, folderDir, imageURL, indent=2)
                    print()
                except FileAlreadyExistsError:
                    print("  The file already exists" + " " * 10, end="\n\n")
                    duplicates += 1
                    howManyDownloaded -= 1

                except Exception as exception:
                    # raise exception
                    print("\n  Could not get the file")
                    print(
                        "  "
                        + "{class_name}: {info}".format(
                            class_name=exception.__class__.__name__, info=str(exception)
                        )
                        + "\n"
                    )
                    howManyDownloaded -= 1

            if duplicates == imagesLenght:
                raise FileAlreadyExistsError
            elif howManyDownloaded + duplicates < imagesLenght:
                raise AlbumNotDownloadedCompletely("Album Not Downloaded Completely")

    def getLinks(self, url, lineNumber=129):

        content = []
        lineNumber = None

        class EromeParser(HTMLParser):
            tag = None

            def handle_starttag(self, tag, attrs):
                self.tag = {tag: {attr[0]: attr[1] for attr in attrs}}

        pageSource = urllib.request.urlopen(url).read().decode().split("\n")

        """ FIND WHERE ALBUM STARTS IN ORDER NOT TO GET WRONG LINKS"""
        for i in range(len(pageSource)):
            obj = EromeParser()
            obj.feed(pageSource[i])
            tag = obj.tag

            if tag is not None:
                if "div" in tag:
                    if "id" in tag["div"]:
                        if tag["div"]["id"] == "album":
                            lineNumber = i
                            break

        for line in pageSource[lineNumber:]:
            obj = EromeParser()
            obj.feed(line)
            tag = obj.tag
            if tag is not None:
                if "img" in tag:
                    if "class" in tag["img"]:
                        if tag["img"]["class"] == "img-front":
                            content.append(tag["img"]["reddit_bulk_dl"])
                elif "source" in tag:
                    content.append(tag["source"]["reddit_bulk_dl"])

        return [
            link
            for link in content
            if link.endswith("_480p.mp4") or not link.endswith(".mp4")
        ]
