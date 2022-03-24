import json
import os
import requests
from dotenv import load_dotenv

from entities.data.EntryData import EntryData
from entities.data.TrendData import TrendData
from tests.BaseEntryTest import BaseEntryTest, _insert_stub_entry_range_in_database, \
    _insert_stub_trend_range_in_database
from tests.BaseRepositoryTest import remove_newly_created_trend_by_id, \
    remove_newly_created_entry_by_id, remove_newly_created_source_by_id, get_new_stub_entry_search_count
from services import constants_service as ct
import gc


# Enable automatic garbage collection
gc.enable()


# Take environment variables from .env file (must be ignored by version control for security purposes).
load_dotenv()

# Get current application host
host = os.getenv(ct.get_application_host_label())

# Get current Flask app port
port = str(os.getenv('FLASK_RUN_PORT'))

# Get entries endpoint URL prefix
url_prefix = ct.get_entries_endpoint_url_prefix()


def _get_expected_top_four_result(stub_entries_specs: list[EntryData], stub_trends_specs: list[TrendData]) \
        -> list[dict[str, str]]:
    """
    Return the expected top four searched entries list
    :param stub_entries_specs: newly created entries specifications
    :param stub_trends_specs: newly created trends specifications
    :return: a list containing each entry title and its associated topic
    """
    stub_specs_zip = zip(stub_entries_specs[:-1], stub_trends_specs[:-1])  # Take only the first 4 entities
    return [
        {
            ct.get_title_key(): str(stub_entry.title),
            ct.get_topic_key(): str(stub_trend.topic)  # Cast to str here to compare str instead of Optional[str]
        }
        for stub_entry, stub_trend in stub_specs_zip
    ]


def _get_entries_endpoint_response_body_content(endpoint: str):
    """
    Return the entries endpoint response body content key
    :param endpoint: target endpoint
    :return: either a dictionary or a list object obtained from a GET request to the endpoint route
    """
    response = requests.get(endpoint)
    body = json.loads(response.content.decode('utf-8'))
    return body[ct.get_response_content_key()]


class TestEntriesEndpoint(BaseEntryTest):

    entries_endpoint_base_url = f'http://{host}:{port}/{url_prefix}'

    def test_get_trends_returns_top_four_entries_by_search_count(self):
        """
        Test if getting trends from the entries endpoint
        returns a list with the titles and the topics of the 4 max searched entries.
        """
        stub_source_id = super().add_new_stub_source().id
        stub_entries_specs = super()._get_five_stub_entries_specs_by_decreasing_search_count(stub_source_id)
        stub_entries_id_list = _insert_stub_entry_range_in_database(stub_entries_specs)
        stub_trends_specs = super()._get_five_stub_trends_specs_from_five_stub_entries(stub_entries_id_list)
        stub_trends_id_list = _insert_stub_trend_range_in_database(stub_trends_specs)
        expected_top_four_result = _get_expected_top_four_result(stub_entries_specs, stub_trends_specs)
        endpoint = f'{self.entries_endpoint_base_url}/trends'
        actual_top_four_result = _get_entries_endpoint_response_body_content(endpoint)
        assert expected_top_four_result == actual_top_four_result
        stub_id_list_zip = zip(stub_entries_id_list, stub_trends_id_list)
        for stub_entry_id, stub_trend_id in stub_id_list_zip:
            remove_newly_created_trend_by_id(stub_trend_id)
            remove_newly_created_entry_by_id(stub_entry_id)
        remove_newly_created_source_by_id(stub_source_id)

    def test_past_three_fake_news_returns_last_three(self):
        """
        Test if getting the latest 3 entries which have been labeled as wrong
        returns a list with the titles of the 3 latest fake news entries.
        """
        stub_source_id = super().add_new_stub_source().id
        new_stub_entry_title = super().get_new_stub_entry_title()
        stub_entries_specs = [
            EntryData(
                id=None,
                fiability=False if i <= 4 else True,
                title=f'{new_stub_entry_title}_{str(i)}',
                source_id=stub_source_id,
                search_count=get_new_stub_entry_search_count()
            )
            for i in range(1, 6)  # 5 entries created with first 4 fake and last one truthful
        ]
        stub_entries_id_list = _insert_stub_entry_range_in_database(stub_entries_specs)
        # Cast to str here to compare str instead of Optional[str]
        expected_latest_three_result = [str(stub_entry.title) for stub_entry in stub_entries_specs[1:4]]
        expected_latest_three_result.reverse()
        endpoint = f'{self.entries_endpoint_base_url}/news/fake/latest'
        actual_latest_three_result = _get_entries_endpoint_response_body_content(endpoint)
        assert actual_latest_three_result == expected_latest_three_result
        for stub_entry_id in stub_entries_id_list:
            remove_newly_created_entry_by_id(stub_entry_id)
        remove_newly_created_source_by_id(stub_source_id)