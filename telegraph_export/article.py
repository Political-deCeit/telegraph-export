#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from readability.readability import Document
from .title import _findTitle
from .author import _findAuthor
from .cached_url import get, getFilePath, getFileName
from telegram_util import AlbumResult, cutCaptionHtml
from .gphoto_2_album import get as gphoto_2_album_get
from PIL import Image
import os

from .content import _findMain


class _Article(object):
    def __init__(self, title, author, text, url=None):
        self.title = title
        self.author = author
        self.text = text
        self.url = url


def _findUrl(url, soup):
    if "telegra.ph" not in url:
        return
    address = soup.find("address")
    if not address:
        return
    link = address.find("a")
    return link and link.get("href")


def _trimWebpage(raw):
    for anchor in ["<!-- detail_toolbox -->", "<!--article_adlist"]:
        index = raw.find(anchor)
        if index != -1:
            raw = raw[:index]
    return raw


def getContentFromAlbum(r, noText=False):
    result = []
    for url in r.imgs:
        result.append('<img src="%s" />' % url)
    if noText:
        return "<div><title>%s</title>%s</div>" % (r.title, "".join(result))
    return "<div><title>%s</title>%s%s</div>" % (r.title, r.cap_html, "".join(result))


def getContent(url, force_cache=False):
    if "photos.google.com/share" in url:
        return getContentFromAlbum(gphoto_2_album_get(url), noText=True)
    else:
        return get(url, force_cache=force_cache)


def getTitle(url, force_cache=True, toSimplified=False, noAutoConvert=False):
    try:
        content = getContent(url, force_cache=force_cache)
        soup = BeautifulSoup(_trimWebpage(content), "html.parser")
        doc = Document(content)
        title = _findTitle(soup, doc)
        return title
    except:
        return "No Title"


def getAuthor(url, force_cache=True):
    content = getContent(url, force_cache=force_cache)
    soup = BeautifulSoup(_trimWebpage(content), "html.parser")
    return _findAuthor(soup)


def _getArticle(
    url=None, content=None, force_cache=False
):
    content = content or getContent(url, force_cache=force_cache)
    soup = BeautifulSoup(_trimWebpage(content), "html.parser")
    article_url = _findUrl(url, soup)
    document = Document(content)
    title = _findTitle(soup, document)
    article = _Article(
        title,
        _findAuthor(soup),
        _findMain(soup, document, url),
        article_url,
    )
    return article


def getAlbumImg(url, inner_content):
    content = BeautifulSoup(get(url, force_cache=True), "html.parser")
    for item in inner_content.findAll("img") + content.findAll(
        "meta", property="og:image"
    ):
        path = item.get("src") or item.get("content")
        if not path:
            continue
        try:
            get(path, mode="b", force_cache=True)
            img = Image.open(getFilePath(path))
        except:
            continue
        w, h = img.size
        file_size = os.stat(getFilePath(path)).st_size
        # Interface Culture Header
        if 36000 < file_size < 36200 and w == 1080 and h == 1080:  # 界面文化题头
            continue
        # marketplace of ideas
        if 27000 < file_size < 27300 and w == 640 and h == 640:  # 思想市场
            continue
        # Interface Culture Header
        if w == 750 and h == 234:  # 界面文化题头
            continue
        if 6000 < file_size < 9000 and w == 347 and h == 347:  # 界面文化题头
            continue
        # American Chinese Miscellaneous Topics
        if 87000 < file_size < 91000 and w == 900 and h == 500:  # 美国华人杂谈题头
            continue
        # wechat foot
        if 53000 < file_size < 56000 and w == 795 and h == 504:  # 微信foot
            continue
        # short history title
        if 57000 < file_size < 61000 and w == 1011 and h == 282:  # 短史记题头
            continue
        # 1) what
        if "s1.reutersmedia.net/resources_v2/images/rcom-default.png" in path:
            continue
        if w * 0.25 < h < w * 4 and min(w, h) > 100 and max(w, h) > 300:
            return [path]
    return []


def getAlbum(
    url,
    force_cache=True,
    word_limit=200,
    paragraph_limit=3,
    append_source=False,
    append_url=True,
):
    content = _getArticle(url, force_cache=force_cache).text
    album = AlbumResult()
    album.imgs = getAlbumImg(url, content)
    for tag in ["img", "br"]:
        for item in content.findAll(tag):
            item.replace_with("\n\n")
    for item in content.findAll("p"):
        item.append("\n\n")
    title = "【%s】\n\n" % getTitle(url)
    lines = content.text.split("\n")
    lines = [line.strip() for line in lines]
    lines = [line for line in lines if isGoodLine(line)]
    if paragraph_limit < 5:
        lines = [line for line in lines if not line or len(line) > 20]
    lines = cutCaptionHtml("\n".join(lines), word_limit).strip().strip("\ufeff").strip()
    lines = lines.split("\n")
    lines = lines[: paragraph_limit * 2]
    album.cap_html_v2 = title + "\n".join(lines).strip()
    if append_url:
        album.cap_html_v2 += "\n\n" + url
    if append_source:
        album.url = url
    return album
