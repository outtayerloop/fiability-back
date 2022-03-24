from flask import Response, make_response, jsonify
from services import constants_service as ct
import gc


# Enable automatic garbage collection
gc.enable()


def get_200_response(content=None) -> Response:
    """
    Return a 200 OK Flask Response with the given content.
    :param content: response content. If None, a message-only response will be returned.
    :return: a 200 OK Flask Response with the given content
    """
    if content is not None:
        response_dict = _get_content_response_dict(content)
    else:
        message = ct.get_ok_response_message()
        response_dict = _get_message_only_response_dict(message)
    return make_response(jsonify(response_dict))


def get_400_response(error_message: str) -> Response:
    """
    Return a 400 Bad Request Flask Response with the given error message (no content).
    :param error_message: the provided error message
    :return: a 400 Bad Request Flask Response with the given error message (no content).
    """
    response_dict = _get_message_only_response_dict(error_message)
    response = make_response(jsonify(response_dict))
    response.status_code = 400
    return response


def _get_content_response_dict(content) -> dict[str, any]:
    """
    Return a dictionary representing a 200 OK Flask Response with a message and some content.
    :param content: response content
    :return: a dictionary representing a 200 OK Flask Response with a message and some content.
    """
    response_message_key = ct.get_response_message_key()
    response_content_key = ct.get_response_content_key()
    message = ct.get_ok_response_message()
    return {
        response_message_key: message,
        response_content_key: content
    }


def _get_message_only_response_dict(message: str) -> dict[str, str]:
    """
    Return a dictionary representing any Flask Response with a message only (no content).
    :return: a dictionary representing any Flask Response with a message only (no content).
    """
    response_message_key = ct.get_response_message_key()
    return {
        response_message_key: message
    }