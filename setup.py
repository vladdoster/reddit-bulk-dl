#!/usr/bin/env python3
from setuptools import setup

setup(
    name = "Bulk Downloader for Reddit",
    version = __version__,
    description = "Bulk Downloader for Reddit",
    author = "Ali Parlakci",
    author_email="parlakciali@gmail.com",
    url="https://github.com/aliparlakci/bulk-downloader-for-redit",
    classifiers=(
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
            "Natural Language :: English",
            "Environment :: Console",
            "Operating System :: OS Independent",
    ),
    entry_points = {
        'console_scripts': ['reddit_bulk_dl=cli:main'],
)

