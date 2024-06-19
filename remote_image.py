#!/bin/python

import os
import sys
import requests
import time
import platform
import errno
from tempfile import NamedTemporaryFile

# To prevent arbirtrary code execution through a forged
# 'Content-Type' in a HTTP header
legitimate_formats = [
    "png", "jpg", "jpeg", "gif"
]


def download_remote_image(url):
    response = requests.get(sys.argv[1])
    if response.status_code != 200:
        print(f"Error: Failed to download image from `{
              url}`, status code = {response.status_code}")
        exit(2)

    # For example: "Content-Type: image/png"
    format = response.headers['Content-Type'].split("/")[1].lower()
    if format not in legitimate_formats:
        print(f"Error: Unsupported file type `{format}`")
        exit(3)

    suffix = "." + format
    image_file = NamedTemporaryFile("wb", suffix=suffix, delete=False)
    image_file.write(response.content)
    image_file.close()

    return image_file.name


def open_image(path):
    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Linux":
        os.system(f"xdg-open '{path}'")
    else:
        os.system(f"open '{path}'")


if __name__ == "__main__":
    logfile = open("/tmp/remote_image.log", "a")
    logfile.write(" ".join(sys.argv))

    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} [image_url]")
        exit(1)

    image_path = download_remote_image(sys.argv[1])
    open_image(image_path)
