from enum import Enum
from services import constants_service as ct
from typing import Optional
from validators.url import url
import gc


# Enable automatic garbage collection
gc.enable()


# Checker request validity enumerator
class CheckerRequestValidity(Enum):
    VALID = 1
    NONE_JSON_REQUEST_BODY = 2
    MISSING_INPUT_KEY = 3
    NONE_INPUT_KEY = 4
    BAD_URL_PARSING = 5
    TOO_BIG_INPUT = 6


def get_checker_request_validity(request_json: Optional[dict[str, str]]) -> CheckerRequestValidity:
    """
    Return whether the provided json input is None
    or has no "url" input key
    or has a None input key
    or is too big
    or is valid.
    :param request_json: the user input provided from the JSON request object
    :return: a RequestValidity enumerator object with the associated validity value of the request JSON input.
    """
    input_key = ct.get_checker_endpoint_key()
    if request_json is None:
        return CheckerRequestValidity.NONE_JSON_REQUEST_BODY
    elif input_key not in request_json:
        return CheckerRequestValidity.MISSING_INPUT_KEY
    elif request_json[input_key] is None or request_json[input_key].strip(' ') == '':
        return CheckerRequestValidity.NONE_INPUT_KEY
    elif len(request_json[input_key]) > ct.get_max_input_length():
        return CheckerRequestValidity.TOO_BIG_INPUT
    elif not _is_valid_url(request_json[input_key]):
        return CheckerRequestValidity.BAD_URL_PARSING
    else:
        return CheckerRequestValidity.VALID


def is_invalid_request_json(request_validity: CheckerRequestValidity) -> bool:
    """
    Return True if the provided validity enumerator contains the value VALID,
    otherwise return False.
    :param request_validity: the user input provided from the JSON request object
    :return: True if the input is invalid, else False
    """
    return request_validity is not CheckerRequestValidity.VALID


def get_checker_error_message_by_validity(request_validity: CheckerRequestValidity) -> str:
    """
    Return the error message associated to the provided request validity
    (must not be CheckerRequestValidity.VALID and must be implemented, otherwise will raise ValueError)
    for each identified issue.
    :param request_validity: The input request JSON
    :return: the dictionary containing the relevant error message
    """
    if request_validity is CheckerRequestValidity.NONE_JSON_REQUEST_BODY:
        error_message = ct.get_none_json_request_body_message()
    elif request_validity is CheckerRequestValidity.MISSING_INPUT_KEY:
        error_message = ct.get_missing_input_key_message()
    elif request_validity is CheckerRequestValidity.NONE_INPUT_KEY:
        error_message = ct.get_none_input_key_message()
    elif request_validity is CheckerRequestValidity.TOO_BIG_INPUT:
        error_message = ct.get_too_big_input_length_message()
    elif request_validity is CheckerRequestValidity.BAD_URL_PARSING:
        error_message = ct.get_bad_url_parsing_message()
    else:
        # Either lack of implementation or a CheckerRequestValidity.VALID validity was provided when forbidden.
        raise ValueError(ct.get_bad_provided_validity_exception_message())
    return error_message


def _is_valid_url(url_to_check: str) -> bool:
    """
    Return whether or not given URL value is a valid URL.
    :param url_to_check: URL to check
    :return: True if the provided URL was labeled as valid, otherwise return False
    """
    if url(url_to_check) is True:
        protocol = url_to_check.split('://')[0]
        return _is_valid_url_protocol(protocol)
    else:
        return False


def _is_valid_url_protocol(protocol: str) -> bool:
    """
    Return True if the provided protocol is http or https.
    :param protocol: the provided protocol
    :return: True if the provided protocol is http or https
    """
    return protocol.lower() == 'http' or protocol.lower() == 'https'