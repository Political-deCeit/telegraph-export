#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .common import _seemsValidText


def _seemsValidRawArticle(soup, text_limit=500):
    if not _seemsValidText(soup, limit=text_limit):
        return False
    return not not soup.find("img")


def getMatters(soup):
    main = soup.find("div", class_="u-content")
    try:
        item = main.parent.parent.parent.parent.findNext("p")
    except:
        return main
    while item:
        main.insert(len(main.contents), item)
        item = item.findNext("p")
    return main


def getUdn(soup):
    main = soup.find("main")
    try:
        item = main.parent.parent.parent.findNext()
    except:
        return main
    while item:
        if item.get("id") == "extension":
            return main
        main.insert(len(main.contents), item)
        item = item.findNext()
    return main


def _getInnerArticle_(soup, domain):
    applicators = [
        lambda x: x.find("article"),
        lambda x: x.find("article"),
        lambda x: x.find("main"),
        lambda x: x.find("div", {"id": "article_cont"}),
        lambda x: x.find("div", {"id": "js_content"}),
        lambda x: x.find("div", {"id": "bodyContent"}),
        lambda x: x.find("div", {"id": "content_JS"}),
        lambda x: x.find("div", class_="main-post"),
        lambda x: x.find("div", class_="article"),
        lambda x: x.find("div", class_="field-name-body"),
        lambda x: x.find("div", class_="content"),
        lambda x: x.find("div", class_="RichContent-inner"),
        lambda x: x.find("div", class_="entry-content"),
        lambda x: x.find("div", class_="pf-content"),
        lambda x: x.find("div", class_="pn-single-post-wrapper__content"),
        lambda x: x.find("div", class_="post-content"),
        lambda x: x.find("div", class_="inner_content"),
        lambda x: x.find("div", class_="content_wrapper"),
        lambda x: x.find("div", class_="story-body__inner"),
        lambda x: x.find("div", class_="answercell"),
        lambda x: x.find("div", class_="post-text"),
        lambda x: x.find("div", class_="post-body"),
        lambda x: x.find("div", class_="mainContent"),
        lambda x: x.find("div", class_="pane-node-body"),
        lambda x: x.find("div", class_="info-content"),
        lambda x: x.find("main", class_="info-content"),
        lambda x: x.find("div", class_="post__contentWrap"),
    ]
    domain_specific_applicators = {
        "": [lambda x: x.find("body")],
        "bbc.co.uk": [lambda x: x.find("div", {"dir": "ltr"})],
        "bbc.com": [lambda x: x.find("article"), lambda x: x.find("main")],
    }
    if "matters.news" in domain:
        return getMatters(soup)
    if "opinion.udn.com" in domain:
        return getUdn(soup)
    for applicator in applicators:
        candidate = applicator(soup)
        if _seemsValidRawArticle(candidate, text_limit=500):
            soup = candidate
    for d, applicators in domain_specific_applicators.items():
        if d in domain:
            for applicator in applicators:
                candidate = applicator(soup)
                if candidate:
                    soup = candidate
    return soup


def _getInnerArticle(soup, domain):
    all_content = str(soup)
    inner = _getInnerArticle_(soup, domain)
    index = all_content.find(str(inner))
    if index == -1:
        return inner, None
    return inner, all_content[:index]
