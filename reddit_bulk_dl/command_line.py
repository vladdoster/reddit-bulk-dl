#!/usr/bin/env python3

import argparse
import configparser
import sys
from utils import create_logger

logger = create_logger()


class RawTextArgumentDefaultsHelpFormatter(
    argparse.ArgumentDefaultsHelpFormatter, argparse.RawTextHelpFormatter
):
    pass


def cli():
    """Initialize argparse and add arguments"""

    parser = argparse.ArgumentParser(
        description="CLI for downloading media from various online sources.",
        formatter_class=RawTextArgumentDefaultsHelpFormatter,
        prog="reddit-bulk-dl",
    )

    verbosity_group = parser.add_mutually_exclusive_group(required=False)
    verbosity_levels = ["--verbose", "--quiet", "--debug"]
    for level in verbosity_levels:
        verbosity_group.add_argument(
            level,
            action="store_const",
            const=level,
            dest="verbosity",
        )

    parser.add_argument(
        "-d",
        "--dir",
        help="A filepath where save downloaded media",
        metavar="dir",
    )

    parser.add_argument("--link", "-l", help="Get posts from link", metavar="link")

    parser.add_argument(
        "--submitted",
        action="store_true",
        help="Download media for the current user",
    )

    parser.add_argument(
        "--subreddit",
        nargs="+",
        help="Triggers subreddit mode and takes subreddit's "
        'name without r/. use "frontpage" for frontpage',
        metavar="SUBREDDIT",
        type=str,
    )

    parser.add_argument(
        "--multireddit",
        help="Triggers multireddit mode and takes " "multireddit's name without m/",
        metavar="MULTIREDDIT",
        type=str,
    )

    parser.add_argument(
        "--user",
        help='reddit username if needed. use "me" for ' "current user",
        required="--multireddit" in sys.argv or "--submitted" in sys.argv,
        metavar="redditor",
        type=str,
    )

    parser.add_argument(
        "--search",
        help="Searches for given query in given subreddits",
        metavar="query",
        type=str,
    )

    parser.add_argument(
        "--sort",
        choices=["hot", "top", "new", "controversial", "rising", "relevance"],
        metavar="SORT TYPE",
        type=str,
    )

    parser.add_argument("--limit", help="default: unlimited", metavar="Limit", type=int)

    parser.add_argument(
        "--time",
        help="Either hour, day, week, month, year or all." " default: all",
        choices=["all", "hour", "day", "week", "month", "year"],
        metavar="TIME_LIMIT",
        type=str,
    )

    parser.add_argument(
        "--skip",
        nargs="+",
        help="Skip posts with given type",
        type=str,
        choices=["images", "videos", "gifs", "self"],
        default=[],
    )

    parser.add_argument(
        "--skip-domain",
        nargs="+",
        help="Skip posts with given domain",
        type=str,
        default=[],
    )

    parser.add_argument("--dl-dir", action="store_true", help="Set custom folder path")

    parser.add_argument(
        "--set-default-dir",
        action="store_true",
        help="Set a default dir to be used in case no dir is given",
    )

    parser.add_argument(
        "--set-default-options",
        action="store_true",
        help="Set default options to use everytime program runs",
    )

    parser.add_argument(
        "--use-local-config",
        action="store_true",
        help="Creates a config file in the program's dir and uses it. Useful for having multiple configs",
    )

    parser.add_argument(
        "--no-dupes",
        action="store_true",
        help="Do not download duplicate posts on different subreddits",
    )

    parser.add_argument(
        "--downloaded-posts",
        help="Use a hash file to keep track of downloaded files",
        type=str,
    )

    parser.add_argument(
        "--no-download",
        action="store_true",
        help="Just saved posts into a the POSTS.json file without downloading",
    )

    return parser


def welcome_msg():
    print("""
                      ,d"=≥,.,qOp,
                     ,7'  ''²$(  )
                    ,7'      '?q$7'
                 ..,$$,.
       ,.  .,,--***²""²***--,,.  .,
     ²   ,p²''              ''²q,   ²
    :  ,7'                      '7,  :
     ' $      ,db,      ,db,      $ '
      '$      ²$$²      ²$$²      $'    Welcome to Reddit Bulk Downloader
      '$                          $'
       '$.     .,        ,.     .$'
        'b,     '²«»«»«»²'     ,d'
         '²?bn,,          ,,nd?²'
           ,7$ ''²²²²²²²²'' $7,
         ,² ²$              $² ²,
         $  :$              $:  $
         $   $              $   $
         'b  q:            :p  d'
          '²«?$.          .$?»²'
             'b            d'
           ,²²'?,.      .,?'²²,
          ²==--≥²²==--==²²≤--==² """
    )


def main():
    try:
        config = configparser.ConfigParser()
        config.read("config.ini")
        logger.info(config.sections())
    except configparser.ParsingError as err:
        logger.error("Unable to parse configuration file: {0}".format(err))
        sys.exit(1)


if __name__ == "__main__":
    welcome_msg()
    main()
