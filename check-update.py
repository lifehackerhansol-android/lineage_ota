#
# Copyright (C) 2023, lifehackerhansol
# SPDX-License-Identifier: Apache-2.0
#

#
# Helper script to scrape the SourceForge API
# argv[1] = project name
#

import json
import os
import sys
import urllib

import feedparser
import requests


def get_builds():
    return


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"usage: {sys.argv[0]} <project name>")
        sys.exit(1)

    with open("builds.json", "r") as f:
        files = json.load(f)

    filesToCheck = {
        "builds": {

        }
    }

    # Check the actual API file to see if it's already there
    # Don't parse it otherwise
    # If api dir doesn't exist, then it's a brand new repo, and
    # we check everything
    if not os.path.isdir("api") or not os.listdir("api"):
        filesToCheck = files
    else:
        for i in os.listdir("api"):
            with open(f"api/{i}") as f:
                ota_file = json.load(f)
            for device, filename in files["builds"].items():
                if filename != ota_file["response"][0]["filename"]:
                    filesToCheck["builds"][device] = filename

    # is there actually a new build?
    if not filesToCheck["builds"]:
        print("API up to date.")
        sys.exit(3)

    # get RSS feed
    with requests.get(f"https://sourceforge.net/projects/{sys.argv[1]}/rss") as r:
        if r.status_code != 200:
            print(f"Sourceforge RSS feed down with error {r.status_code}. Abort.")
            sys.exit(2)
        else:
            feed = feedparser.parse(r.text)

    filesToDownload = []

    # compare file names with existing
    # if it doesn't exist, then either SF hasn't enabled downloads yet, 
    # or something is wrong
    for device, filename in filesToCheck["builds"].items():
        for i in feed["entries"]:
            if f"{device}/{filename}" not in i["title"]:
                continue
            else:
                filesToDownload.append(i["link"].replace("/download", ""))

    if not filesToDownload:
        print("Sourceforge doesn't have downloads available. Abort.")
        sys.exit(4)

    with open("files_to_download.txt", "w") as f:
        for i in filesToDownload:
            f.write(f"{i}\n")
