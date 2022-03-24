from services import constants_service as ct
from tests.integration.BaseCheckerTest import BaseCheckerTest
import gc


# Enable automatic garbage collection
gc.enable()


class TestCheckerEndpoint(BaseCheckerTest):

    def test_none_json_body_returns_400_none_json_request_body_message(self):
        """
        Test if sending a request with None JSON body to the checker endpoint route
        results in the expected 400 Bad Request response message.
        """
        expected_response_message = ct.get_none_json_request_body_message()
        expected_body = {ct.get_response_message_key(): expected_response_message}
        invalid_content = None
        actual_body = super().get_checker_endpoint_response_body(invalid_content, True)
        assert actual_body == expected_body

    def test_missing_json_content_type_headers_returns_400_none_json_request_body_message(self):
        """
        Test if sending a request with a valid JSON body
        and missing content type application/json headers to the checker endpoint route
        results in the expected 400 Bad Request response message.
        """
        expected_response_message = ct.get_none_json_request_body_message()
        expected_body = {ct.get_response_message_key(): expected_response_message}
        valid_content = {ct.get_checker_endpoint_key(): self.valid_url}
        actual_body = super().get_checker_endpoint_response_body(valid_content, False)
        assert actual_body == expected_body

    def test_empty_json_body_returns_400_missing_input_key_body_message(self):
        """
        Test if sending a request with empty JSON body to the checker endpoint route
        results in the expected 400 Bad Request response message.
        """
        expected_response_message = ct.get_missing_input_key_message()
        expected_body = {ct.get_response_message_key(): expected_response_message}
        invalid_content = {}
        actual_body = super().get_checker_endpoint_response_body(invalid_content, True)
        assert actual_body == expected_body

    def test_invalid_json_key_returns_400_missing_input_key_body_message(self):
        """
        Test if sending a request with missing "input" key to the checker endpoint route
        results in the expected 400 Bad Request response message.
        """
        expected_response_message = ct.get_missing_input_key_message()
        expected_body = {ct.get_response_message_key(): expected_response_message}
        invalid_content = {'invalid_key': self.valid_url}
        actual_body = super().get_checker_endpoint_response_body(invalid_content, True)
        assert actual_body == expected_body

    def test_none_json_input_key_returns_400_none_input_key_body_message(self):
        """
        Test if sending a request with None "input" key to the checker endpoint route
        results in the expected 400 Bad Request response message.
        """
        expected_response_message = ct.get_none_input_key_message()
        expected_body = {ct.get_response_message_key(): expected_response_message}
        invalid_content = {ct.get_checker_endpoint_key(): None}
        actual_body = super().get_checker_endpoint_response_body(invalid_content, True)
        assert actual_body == expected_body

    def test_whitespace_json_input_key_returns_400_none_input_key_body_message(self):
        """
        Test if sending a request with full whitespace "input" key to the checker endpoint route
        results in the expected 400 Bad Request response message.
        """
        expected_response_message = ct.get_none_input_key_message()
        expected_body = {ct.get_response_message_key(): expected_response_message}
        invalid_content = {ct.get_checker_endpoint_key(): ' '}
        actual_body = super().get_checker_endpoint_response_body(invalid_content, True)
        assert actual_body == expected_body

    def test_empty_json_input_key_returns_400_none_input_key_body_message(self):
        """
        Test if sending a request with an empty "input" key to the checker endpoint route
        results in the expected 400 Bad Request response message.
        """
        expected_response_message = ct.get_none_input_key_message()
        expected_body = {ct.get_response_message_key(): expected_response_message}
        invalid_content = {ct.get_checker_endpoint_key(): ''}
        actual_body = super().get_checker_endpoint_response_body(invalid_content, True)
        assert actual_body == expected_body

    def test_too_big_json_input_returns_400_too_big_input_length_body_message(self):
        """
        Test if sending a request with too big "input" key to the checker endpoint route
        results in the expected 400 Bad Request response message.
        """
        expected_response_message = ct.get_too_big_input_length_message()
        expected_body = {ct.get_response_message_key(): expected_response_message}
        invalid_content = {ct.get_checker_endpoint_key(): 'x' * (ct.get_max_input_length() + 1)}
        actual_body = super().get_checker_endpoint_response_body(invalid_content, True)
        assert actual_body == expected_body

    def test_invalid_url_protocol_json_input_returns_400_bad_url_parsing_body_message(self):
        """
        Test if sending a request with bad url protocol "input" key to the checker endpoint route
        results in the expected 400 Bad Request response message.
        """
        expected_response_message = ct.get_bad_url_parsing_message()
        expected_body = {ct.get_response_message_key(): expected_response_message}
        invalid_protocol_prefix = 'ftp'
        valid_subdomain_suffix = 'com'
        valid_domain_length = ct.get_max_input_length() - len(f'{invalid_protocol_prefix}://.{valid_subdomain_suffix}')
        valid_domain = 'x' * valid_domain_length
        invalid_url = f'{invalid_protocol_prefix}://{valid_domain}.{valid_subdomain_suffix}'
        invalid_content = {ct.get_checker_endpoint_key(): invalid_url}
        actual_body = super().get_checker_endpoint_response_body(invalid_content, True)
        assert actual_body == expected_body

    def test_missing_subdomain_suffix_dot_json_input_returns_400_bad_url_parsing_body_message(self):
        """
        Test if sending a request with missing subdomain suffix dot "input" key to the checker endpoint route
        results in the expected 400 Bad Request response message.
        """
        expected_response_message = ct.get_bad_url_parsing_message()
        expected_body = {ct.get_response_message_key(): expected_response_message}
        valid_protocol_prefix = 'https'
        valid_subdomain_suffix = 'com'
        valid_domain_length = ct.get_max_input_length() - len(f'{valid_protocol_prefix}://{valid_subdomain_suffix}')
        valid_domain = 'x' * valid_domain_length
        invalid_url = f'{valid_protocol_prefix}://{valid_domain}{valid_subdomain_suffix}'
        invalid_content = {ct.get_checker_endpoint_key(): invalid_url}
        actual_body = super().get_checker_endpoint_response_body(invalid_content, True)
        assert actual_body == expected_body

    def test_missing_protocol_label_json_input_returns_400_bad_url_parsing_body_message(self):
        """
        Test if sending a request with missing protocol label "input" key to the checker endpoint route
        results in the expected 400 Bad Request response message.
        """
        expected_response_message = ct.get_bad_url_parsing_message()
        expected_body = {ct.get_response_message_key(): expected_response_message}
        valid_subdomain_suffix = 'com'
        valid_domain_length = ct.get_max_input_length() - len(f'://.{valid_subdomain_suffix}')
        valid_domain = 'x' * valid_domain_length
        invalid_url = f'://{valid_domain}.{valid_subdomain_suffix}'
        invalid_content = {ct.get_checker_endpoint_key(): invalid_url}
        actual_body = super().get_checker_endpoint_response_body(invalid_content, True)
        assert actual_body == expected_body

    def test_missing_protocol_separator_json_input_returns_400_bad_url_parsing_body_message(self):
        """
        Test if sending a request with missing protocol separator "input" key to the checker endpoint route
        results in the expected 400 Bad Request response message.
        """
        expected_response_message = ct.get_bad_url_parsing_message()
        expected_body = {ct.get_response_message_key(): expected_response_message}
        valid_protocol_prefix = 'https'
        valid_subdomain_suffix = 'com'
        valid_domain_length = ct.get_max_input_length() - len(f'{valid_protocol_prefix}.{valid_subdomain_suffix}')
        valid_domain = 'x' * valid_domain_length
        invalid_url = f'{valid_protocol_prefix}{valid_domain}.{valid_subdomain_suffix}'
        invalid_content = {ct.get_checker_endpoint_key(): invalid_url}
        actual_body = super().get_checker_endpoint_response_body(invalid_content, True)
        assert actual_body == expected_body

    def test__rubbish_url_json_input_returns_400_bad_url_parsing_body_message(self):
        """
        Test if sending a request with a rubbish URL "input" key to the checker endpoint route
        results in the expected 400 Bad Request response message.
        """
        expected_response_message = ct.get_bad_url_parsing_message()
        expected_body = {ct.get_response_message_key(): expected_response_message}
        invalid_url = 'x' * ct.get_max_input_length()
        invalid_content = {ct.get_checker_endpoint_key(): invalid_url}
        actual_body = super().get_checker_endpoint_response_body(invalid_content, True)
        assert actual_body == expected_body