#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .cached_url import get as cached_url_get
from bs4 import BeautifulSoup
from telegram_util import AlbumResult as Result

pivot = 'href="./share/'
end = '"><img'

img_pivot = "https://lh3.googleusercontent.com/"
img_end = '"'


def getImage(content):
    for parts in content.split(img_pivot)[1:]:
        link = parts.split(img_end)[0]
        return img_pivot + link


def getImages(content):
    for parts in content.split(pivot):
        link = parts.split(end)[0]
        if "?key=" not in link[:160]:
            continue
        yield getImage(
            cached_url_get("https://photos.google.com/share/" + link, force_cache=True)
        )


def get(url):
    r = Result()
    r.url = url
    content = cached_url_get(url, force_cache=True)
    soup = BeautifulSoup(content, "html.parser")
    r.title = soup.find("meta", {"property": "og:title"})["content"]
    r.cap_html = r.title
    r.imgs = list(getImages(content))
    return r
