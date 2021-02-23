#!/usr/bin/env python3
import json
import logging
import sys
from pathlib import Path

from prawcore.exceptions import InsufficientScope

from command_line import Arguments
from downloaders.direct import Direct
from downloaders.Erome import Erome
from downloaders.Gfycat import Gfycat
from downloaders.Imgur import Imgur
from downloaders.gallery import gallery
from downloaders.gifDeliveryNetwork import GifDeliveryNetwork
from downloaders.redgifs import Redgifs
from downloaders.selfPost import SelfPost
from downloaders.vreddit import VReddit
from downloaders.youtube import Youtube
from errors import (
    ImgurLimitError,
    FileAlreadyExistsError,
    ImgurLoginError,
    NotADownloadableLinkError,
    NoSuitablePost,
    FailedToDownload,
    TypeInSkip,
    DomainInSkip,
    AlbumNotDownloadedCompletely,
    full_exc_info,
)
from reddit import Reddit


def parse_logs(f_name):
    try:
        with open(f_name) as fh:
            content = json.load(fh)
            content.remove("HEADER")
    except (KeyError, OSError) as err:
        sys.exit(err)

    return [
        content[post][-1] for post in content if content[post][-1]["TYPE"] is not None
    ]


def isPostExists(POST, dir):
    """Figure out a file's name and checks if the file already exists"""

    f_name = GLOBAL.config["f_name"].format(**POST)

    possibleExtensions = [
        ".jpg",
        ".png",
        ".mp4",
        ".gif",
        ".webm",
        ".md",
        ".mkv",
        ".flv",
    ]

    for extension in possibleExtensions:

        path = dir / Path(f_name + extension)

        if path.exists():
            return True

    else:
        return False


def download_media(post, dir):
    downloaders = {
        "imgur": Imgur,
        "gfycat": Gfycat,
        "erome": Erome,
        "direct": Direct,
        "self": SelfPost,
        "redgifs": Redgifs,
        "gifdeliverynetwork": GifDeliveryNetwork,
        "v.redd.it": VReddit,
        "youtube": Youtube,
        "gallery": gallery,
    }

    print()
    if post["TYPE"] in downloaders:
        downloaders[post["TYPE"]](dir, post)
    else:
        raise NoSuitablePost

    return None


def download(submissions):
    """Analyze list of submissions and call the right function
    to download each one, catch errors, update the log files
    """

    downloadedCount = 0
    duplicates = 0

    FAILED_FILE = createLogFile("FAILED")

    if GLOBAL.arguments.unsave:
        reddit = Reddit(GLOBAL.config["credentials"]["reddit"]).begin()

    subsLenght = len(submissions)

    for i in range(len(submissions)):
        print(f"\n({i + 1}/{subsLenght})", end=" — ")
        print(
            submissions[i]["POSTID"],
            f"r/{submissions[i]['SUBREDDIT']}",
            f"u/{submissions[i]['REDDITOR']}",
            submissions[i]["FLAIR"] if submissions[i]["FLAIR"] else "",
            sep=" — ",
            end="",
        )
        print(f" – {submissions[i]['TYPE'].upper()}", end="", noPrint=True)

        dir = GLOBAL.dir / GLOBAL.config["folderpath"].format(**submissions[i])
        details = {
            **submissions[i],
            **{
                "TITLE": nameCorrector(
                    submissions[i]["TITLE"],
                    reference=str(dir)
                    + GLOBAL.config["f_name"].format(**submissions[i])
                    + ".ext",
                )
            },
        }
        f_name = GLOBAL.config["f_name"].format(**details)

        if isPostExists(details, dir):
            print()
            print(dir)
            print(f_name)
            print("It already exists")
            duplicates += 1
            continue

        if any(
            domain in submissions[i]["CONTENTURL"] for domain in GLOBAL.arguments.skip
        ):
            print()
            print(submissions[i]["CONTENTURL"])
            print("Domain found in skip domains, skipping post...")
            continue

        try:
            download_media(details, dir)
            GLOBAL.downloadedPosts.add(details["POSTID"])
            try:
                if GLOBAL.arguments.unsave:
                    reddit.submission(id=details["POSTID"]).unsave()
            except InsufficientScope:
                reddit = Reddit().begin()
                reddit.submission(id=details["POSTID"]).unsave()

            downloadedCount += 1

        except FileAlreadyExistsError:
            print("It already exists")
            GLOBAL.downloadedPosts.add(details["POSTID"])
            duplicates += 1

        except ImgurLoginError:
            print(
                "Imgur login failed. \nQuitting the program "
                "as unexpected errors might occur."
            )
            sys.exit()

        except ImgurLimitError as exception:
            FAILED_FILE.add(
                {
                    int(i + 1): [
                        "{class_name}: {info}".format(
                            class_name=exception.__class__.__name__, info=str(exception)
                        ),
                        details,
                    ]
                }
            )

        except NotADownloadableLinkError as exception:
            print(
                "{class_name}: {info}".format(
                    class_name=exception.__class__.__name__, info=str(exception)
                )
            )
            FAILED_FILE.add(
                {
                    int(i + 1): [
                        "{class_name}: {info}".format(
                            class_name=exception.__class__.__name__, info=str(exception)
                        ),
                        submissions[i],
                    ]
                }
            )

        except TypeInSkip:
            print()
            print(submissions[i]["CONTENTURL"])
            print("Skipping post...")

        except DomainInSkip:
            print()
            print(submissions[i]["CONTENTURL"])
            print("Skipping post...")

        except NoSuitablePost:
            print("No match found, skipping...")

        except FailedToDownload:
            print("Failed to download the posts, skipping...")
        except AlbumNotDownloadedCompletely:
            print("Album did not downloaded completely.")
            FAILED_FILE.add(
                {
                    int(i + 1): [
                        "{class_name}: {info}".format(
                            class_name=exc.__class__.__name__, info=str(exc)
                        ),
                        submissions[i],
                    ]
                }
            )

        except Exception as exc:
            print(
                "{class_name}: {info}\nSee CONSOLE_LOG.txt for more information".format(
                    class_name=exc.__class__.__name__, info=str(exc)
                )
            )

            logging.error(
                sys.exc_info()[0].__name__, exc_info=full_exc_info(sys.exc_info())
            )
            print(GLOBAL.log_stream.getvalue(), noPrint=True)

            FAILED_FILE.add(
                {
                    int(i + 1): [
                        "{class_name}: {info}".format(
                            class_name=exc.__class__.__name__, info=str(exc)
                        ),
                        submissions[i],
                    ]
                }
            )

    if duplicates:
        print(
            f"\nThere {'were' if duplicates > 1 else 'was'} "
            f"{duplicates} duplicate{'s' if duplicates > 1 else ''}"
        )

    if downloadedCount == 0:
        print("Nothing is downloaded :(")

    else:
        print(
            f"Total of {downloadedCount} "
            f"link{'s' if downloadedCount > 1 else ''} downloaded!"
        )

    arguments = Arguments.parse()
    #
    # if arguments.set_f_name:
    #     Config(GLOBAL.configdir).setCustomf_name()
    #     sys.exit()
    #
    # if arguments.set_folderpath:
    #     Config(GLOBAL.configdir).setCustomFolderPath()
    #     sys.exit()
    #
    # if arguments.set_default_dir:
    #     Config(GLOBAL.configdir).setDefaultdir()
    #     sys.exit()
    #
    # if arguments.set_default_options:
    #     Config(GLOBAL.configdir).setDefaultOptions()
    #     sys.exit()
    #
    # if arguments.use_local_config:
    #     JsonFile("config.json").add(GLOBAL.config)
    #     sys.exit()
    #
    # if arguments.dir:
    #     GLOBAL.dir = Path(arguments.dir.strip())
    # elif (
    #         "default_dir" in GLOBAL.config
    #         and GLOBAL.config["default_dir"] != ""
    # ):
    #     GLOBAL.dir = Path(
    #         GLOBAL.config["default_dir"].format(time=GLOBAL.RUN_TIME)
    #     )
    # else:
    #     GLOBAL.dir = Path(input("\ndownload dir: ").strip())
    #
    # if arguments.downloaded_posts:
    #     GLOBAL.downloadedPosts = Store(arguments.downloaded_posts)
    # else:
    #     GLOBAL.downloadedPosts = Store()
    #
    # printLogo()
    # print("\n", " ".join(sys.argv), "\n", noPrint=True)
    #
    # if arguments.log is not None:
    #     logDir = Path(arguments.log)
    #     download(parse_logs(logDir))
    #     sys.exit()
    #
    # programMode = ProgramMode(arguments).generate()
    #
    # try:
    #     posts = getPosts(programMode)
    # except Exception as exc:
    #     logging.error(
    #         sys.exc_info()[0].__name__, exc_info=full_exc_info(sys.exc_info())
    #     )
    #     print(GLOBAL.log_stream.getvalue(), noPrint=True)
    #     print(exc)
    #     sys.exit()
    #
    # if posts is None:
    #     print("I could not find any posts in that URL")
    #     sys.exit()
    #
    # if GLOBAL.arguments.no_download:
    #     pass
    # else:
    #     download(posts)
