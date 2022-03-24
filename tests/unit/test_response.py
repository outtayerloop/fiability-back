from typing import Dict

from services import constants_service as ct
from services import response_service as res
import gc


# Enable automatic garbage collection
gc.enable()


class TestResponse:

    # Attribute specified declaratively because constructors are forbidden when working with pytest.
    given_content = 'x'

    def test_getting_content_response_returns_a_dict(self):
        """
        Test if getting a content response
        returns a dictionary.
        """
        actual_content_response_dict = res._get_content_response_dict(self.given_content)
        assert isinstance(actual_content_response_dict, Dict)

    def test_getting_content_response_contains_message_key(self):
        """
        Test if getting a content response
        returns a dictionary with the expected message key.
        """
        expected_response_message_key = ct.get_response_message_key()
        actual_content_response_dict = res._get_content_response_dict(self.given_content)
        assert expected_response_message_key in actual_content_response_dict

    def test_getting_content_response_contains_content_key(self):
        """
        Test if getting a content response
        returns a dictionary with the expected content key.
        """
        expected_response_content_key = ct.get_response_content_key()
        actual_content_response_dict = res._get_content_response_dict(self.given_content)
        assert expected_response_content_key in actual_content_response_dict

    def test_getting_content_response_contains_expected_message_value(self):
        """
        Test if getting a content response
        returns a dictionary with the expected message value.
        """
        expected_response_message_key = ct.get_response_message_key()
        expected_response_message_value = ct.get_ok_response_message()
        actual_content_response_dict = res._get_content_response_dict(self.given_content)
        actual_response_message_value = actual_content_response_dict[expected_response_message_key]
        assert actual_response_message_value == expected_response_message_value

    def test_getting_content_response_contains_expected_content_value(self):
        """
        Test if getting a content response
        returns a dictionary with the expected content value.
        """
        expected_response_content_key = ct.get_response_content_key()
        expected_response_content_value = self.given_content
        actual_content_response_dict = res._get_content_response_dict(self.given_content)
        actual_response_content_value = actual_content_response_dict[expected_response_content_key]
        assert actual_response_content_value == expected_response_content_value