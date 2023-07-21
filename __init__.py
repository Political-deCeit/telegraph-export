name = 'telegraph_export'

from html_telegraph_poster import TelegraphPoster
from .article import _getArticle, isConfident

def _formaturl(url):
    if not url.strip():
        return ""
    if "://" not in url:
        return "https://" + url
    return url

def _trimUrl(url):
    if not "://" in url:
        return url
    loc = url.find("://")
    return url[loc + 3 :]

def getArticle(
    url,
    throw_exception=False,
    force_cache=False,
):
    try:
        return _getArticle(
            _formaturl(url),
            force_cache=force_cache,
        )
    except Exception as e:
        if throw_exception:
            raise e

def getAuthorField(author, noSourceLink):
    if author == "Source" and noSourceLink:
        return ""
    else:
        return author
    
def getAuthorUrl(article, url, noSourceLink):
    if noSourceLink:
        return ""
    else:
        return _formaturl(article.url or url)

def export(
    url,
    token,
    throw_exception=False,
    force=False,
    force_cache=False,
    noSourceLink=False,
):
    try:
        p = TelegraphPoster(access_token=token)
        article = getArticle(
            url,
            throw_exception,
            force_cache=force_cache,
        )
        if not article.text or not article.text.text.strip():
            article.text = "<div>TO BE ADDED</div>"
        try:
            r = p.post(
                title=article.title,
                author=getAuthorField(article.author, noSourceLink),
                author_url=getAuthorUrl(article, url, noSourceLink),
                text=str(article.text),
            )
        except Exception as e:
            if "ACCESS_TOKEN_INVALID" in str(e):
                r = TelegraphPoster().post(
                    title=article.title,
                    author=getAuthorField(article.author, noSourceLink),
                    author_url=getAuthorUrl(article, url, noSourceLink),
                    text=str(article.text),
                )
            else:
                raise e
        if force or isConfident(url, article.text):
            return _trimUrl(r["url"])
    except Exception as e:
        if throw_exception:
            raise e
