from typing import Optional

from flask import Blueprint, request, Response
from services import constants_service as ct
from services import checker_service as chk
from services import crawler_service as cwl
from services import request_service as req
from services import response_service as res
from services.request_service import CheckerRequestValidity
from newspaper import Article
import gc


# Enable automatic garbage collection
gc.enable()


# Create the checker route
app_checker = Blueprint('checker', __name__)


@app_checker.route('', methods=['POST'])
def check() -> Response:
    """
    Return a 200 OK Flask Response containing the extracted truthfulness string (with an "ok" message)
    from the request JSON "url" component if the provided input is valid and has been successfully parsed,
    otherwise return a 400 Bad Request with the associated error message.
    :return: the extracted truthfulness (between "REAL" and "FAKE") with an "ok" message, otherwise an error message.
    """
    request_validity = req.get_checker_request_validity(request.json)
    if req.is_invalid_request_json(request_validity):
        return _send_400_response(request_validity)
    url = request.json[ct.get_checker_endpoint_key()]
    article = cwl.get_article_by_url(url)
    if _is_valid_article(article):
        checker_response = chk.check(article.text)
        topic_response = chk.check_topic(article.text)
        _save_user_input_data(url, article, checker_response >= ct.get_truthfulness_percentage_threshold(), topic_response)
        return res.get_200_response(checker_response)
    else:
        return _send_400_response(CheckerRequestValidity.BAD_URL_PARSING)


def _is_valid_article(article: Optional[Article]) -> bool:
    """
    Return True if the given article is valid, otherwise return False.
    :param article: parsed article
    :return: True if the given article is valid, otherwise return False.
    """
    return article is not None \
           and article.text is not None \
           and article.text.strip() != '' \
           and article.title is not None \
           and article.title.strip() != ''


def _send_400_response(request_validity: CheckerRequestValidity) -> Response:
    """
    Return a 400 Bad Request Flask Response from the given request invalidity reason
    (must not be CheckerRequestValidity.VALID otherwise will raise ValueError).
    :param request_validity: the given request invalidity reason (must not be CheckerRequestValidity.VALID).
    :return: a 400 Bad Request Flask Response from the given request invalidity reason
    """
    if request_validity is CheckerRequestValidity.VALID:
        raise ValueError('The provided request_validity must not be CheckerRequestValidity.VALID.')
    error_message = req.get_checker_error_message_by_validity(request_validity)
    return res.get_400_response(error_message)


def _save_user_input_data(url: str, article: Article, fiability: bool, topic_response):
    """
    Save source, trend and entry from the provided user input.
    :param url: article URL
    :param article: parsed article from given URL
    :param fiability: entry extracted truthfulness
    """
    source_id = chk.add_source_by_url(url)
    entry_id = chk.add_entry(source_id, article.title, fiability)
    chk.add_trend(topic_response, entry_id)
