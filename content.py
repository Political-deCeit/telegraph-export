#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from .domain import _findDomain
from .images import _cleanupImages
from .inner_article import _getInnerArticle
from .link import _replaceOfftopicLink
from .offtopic import _decomposeOfftopic
from .tag_replace import _tagReplace

def _findMainFromSoup(soup, url, args={}):
    domain = _findDomain(soup, url)
    soup = _replaceOfftopicLink(soup, args)
    soup = _decomposeOfftopic(soup, url, args)
    soup = _cleanupImages(soup, domain)
    soup, _ = _getInnerArticle(soup, domain)
    soup = _tagReplace(soup)
    return soup


def _findMain(soup, doc, url, args={}):
    result = _findMainFromSoup(soup, url, args)
    if result and result.text and result.text.strip():
        return result
    result = _findMainFromSoup(
        BeautifulSoup(str(doc.content), features="html.parser"), url, args
    )
    if result and result.text and result.text.strip():
        return result
    return doc.content()
