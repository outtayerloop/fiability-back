import json
import os
from urllib.parse import urlparse
import requests
from dotenv import load_dotenv
from entities.models.Entry import Entry
from entities.models.Source import Source
from entities.models.Trend import Trend
from services import constants_service as ct
from typing import Optional, Union
from tests.BaseRepositoryTest import remove_newly_created_trend_by_id, remove_newly_created_entry_by_id
import gc
from entities.models.BaseModel import connect_to_db, close_db


# Enable automatic garbage collection
gc.enable()


# Take environment variables from .env file (must be ignored by version control for security purposes).
load_dotenv()

# Get current application host
host = os.getenv(ct.get_application_host_label())

# Get current Flask app port
port = str(os.getenv('FLASK_RUN_PORT'))

# Get checker endpoint URL prefix
url_prefix = ct.get_checker_endpoint_url_prefix()


def _get_newly_created_source_by_name(source_name: str) -> Optional[Source]:
    """
    Get the previously test-induced created source from the database by its name.
    :param source_name: source to get name
    :return: a Source object containing the searched source if it was correctly created, else None
    """
    connect_to_db()
    found_source = Source.get_or_none(Source.name == source_name)
    close_db()
    return found_source


def _clean_checker_test(new_source_name: str):
    """
    Remove the previously test-induced or test-purpose created trend, entry and source from the database
    :param new_source_name: created source name
    """
    _remove_newly_created_trends_by_source_name(new_source_name)
    _remove_newly_created_entry_by_source_name(new_source_name)
    _remove_newly_created_source_by_name(new_source_name)


def _remove_newly_created_trends_by_source_name(source_name: str):
    """
    Remove the previously test-induced created trend from the database by its source name.
    :param source_name: trend to remove source name
    """
    trends = _get_newly_created_trends_by_source_name(source_name)
    if trends is not None:
        for trend in trends:
            remove_newly_created_trend_by_id(trend.id)


def _remove_newly_created_entry_by_source_name(source_name: str):
    """
    Remove the previously test-induced created entry from the database by its source name.
    :param source_name: entry to remove source name
    """
    found_entry = _get_newly_created_entry_by_source_name(source_name)
    if found_entry is not None:
        entry_id = found_entry.id
        remove_newly_created_entry_by_id(entry_id)


def _get_newly_created_entry_by_source_name(source_name: str) -> Optional[Entry]:
    """
    Get the previously test-induced created entry from the database by its source name.
    :param source_name: entry to get source name
    :return: an Entry object if it was correctly created, else None
    """
    connect_to_db()
    found_entry = Entry.select() \
        .join(Source, on=(Entry.source_id == Source.id)) \
        .where(Source.name == source_name) \
        .execute()
    close_db()
    if found_entry is None or len(found_entry) == 0:
        return None
    return found_entry[0]


def _get_newly_created_trends_by_source_name(source_name: str) -> Optional[list[Trend]]:
    """
    Get the previously test-induced created trend from the database by its source name.
    :param source_name: trend to get source name
    :return: a list of Trend object if it was correctly created, else None
    """
    connect_to_db()
    found_trend = Trend.select()\
        .join(Entry, on=(Trend.entry_id == Entry.id))\
        .join(Source, on=(Entry.source_id == Source.id))\
        .where(Source.name == source_name)\
        .execute()
    close_db()
    if found_trend is None or len(found_trend) == 0:
        return None
    return found_trend


def _remove_newly_created_source_by_name(source_name: str):
    """
    Remove the previously test-induced created source from the database by its name.
    :param source_name: source to remove name
    """
    connect_to_db()
    Source.delete()\
        .where(Source.name == source_name)\
        .execute()
    close_db()


class BaseCheckerTest:

    checker_endpoint_base_url = f'http://{host}:{port}/{url_prefix}'

    # Supposedly non already existing valid source (as only 1 database is available currently)
    valid_url = 'https://arxiv.org/abs/2201.11134'

    def get_checker_endpoint_response_body(self, content_dict: Optional[dict[str, str]], has_headers: bool) \
            -> dict[str, Union[str, float]]:
        """
        Return the checker endpoint response body from the provided input content
        :param content_dict: dictionary content to be jsonified and sent to the checker endpoint
        :param has_headers: determines whether or not application content headers should be set
        :return: a dictionary object obtained from a POST request issued from the requests module
        """
        json_content = json.dumps(content_dict)
        content_type = ct.get_application_content_type()
        headers = {'content-type': content_type} if has_headers is True else None
        response = requests.post(self.checker_endpoint_base_url, data=json_content, headers=headers)
        return json.loads(response.content.decode('utf-8'))

    def get_valid_url(self) -> str:
        """
        Return the valid URL tested against the checker endpoint.
        :return: the valid URL tested against the checker endpoint
        """
        return self.valid_url

    def get_source_name(self) -> str:
        """
        Return the source name used by the valid URL tested against the checker endpoint.
        :return: the source name used
        """
        return urlparse(self.valid_url).netloc