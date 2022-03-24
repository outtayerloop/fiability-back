import logging
from typing import Optional

from newspaper import Article, ArticleException
import gc


# Enable automatic garbage collection
gc.enable()


def get_article_by_url(url: str) -> Optional[Article]:
    """
    Return the parsed Article object from the provided URL if the provided URL is valid and if the article
    was correctly parsed, otherwise return None.
    :param url: The provided article URL.
    :return: the parsed Article object from the provided URL if the provided URL is valid and if the article
    was correctly parsed, otherwise return None.
    """
    try:
        article = Article(url)
        article.download()
        article.parse()
    except ArticleException as ex:
        logging.exception('Invalid provided URL {}. Raised ArticleException : {}'.format(url, ex))
        return None
    except Exception as ex:
        logging.exception('Error while downloading or parsing the article from url {}. '
                          'Raised Exception : {}'.format(url, ex))
        return None
    if not article.is_parsed:
        return None
    return article