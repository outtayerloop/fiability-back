from services import request_service as req
from services.request_service import CheckerRequestValidity
from services import constants_service as ct
import pytest
import gc


# Enable automatic garbage collection
gc.enable()


class TestCheckerInputValidity:

    def test_none_request_json_returns_none_json_request_body_validity(self):
        """
        Test if the CheckerRequestValidity value returned by the corresponding method of the request validity service
        is NONE_JSON_REQUEST_BODY when the provided input is None.
        """
        expected_validity = CheckerRequestValidity.NONE_JSON_REQUEST_BODY
        invalid_request_json = None
        actual_validity = req.get_checker_request_validity(invalid_request_json)
        assert actual_validity is expected_validity

    def test_no_request_json_input_key_returns_missing_input_key(self):
        """
        Test if the CheckerRequestValidity value returned by the corresponding method of the request validity service
        is MISSING_INPUT_KEY when the provided JSON input is empty.
        """
        expected_validity = CheckerRequestValidity.MISSING_INPUT_KEY
        invalid_request_json = {}
        actual_validity = req.get_checker_request_validity(invalid_request_json)
        assert actual_validity is expected_validity

    def test_none_request_json_input_value_returns_none_input_key(self):
        """
        Test if the CheckerRequestValidity value returned by the corresponding method of the request validity service
        is NONE_INPUT_KEY when the provided input key is None.
        """
        expected_validity = CheckerRequestValidity.NONE_INPUT_KEY
        input_key = ct.get_checker_endpoint_key()
        invalid_request_json = {input_key: None}
        actual_validity = req.get_checker_request_validity(invalid_request_json)
        assert actual_validity is expected_validity

    def test_bad_url_json_input_returns_bad_url_parsing(self):
        """
        Test if the CheckerRequestValidity value returned by the corresponding method of the request validity service
        is BAD_URL_PARSING when the provided url input key is a bad URL.
        """
        expected_validity = CheckerRequestValidity.BAD_URL_PARSING
        input_key = ct.get_checker_endpoint_key()
        invalid_url = 'x'
        invalid_request_json = {input_key: invalid_url}
        actual_validity = req.get_checker_request_validity(invalid_request_json)
        assert actual_validity is expected_validity

    def test_too_big_input_returns_too_big_input(self):
        """
        Test if the CheckerRequestValidity value returned by the corresponding method of the request validity service
        is TOO_BIG_INPUT when the provided input is too big.
        """
        expected_validity = CheckerRequestValidity.TOO_BIG_INPUT
        input_key = ct.get_checker_endpoint_key()
        valid_protocol_prefix = 'https'
        valid_subdomain_suffix = 'com'
        valid_domain_length = ct.get_max_input_length() - len(f'{valid_protocol_prefix}://.{valid_subdomain_suffix}')
        too_big_domain = 'x' * (valid_domain_length + 1)
        too_big_url = f'{valid_protocol_prefix}://{too_big_domain}.{valid_subdomain_suffix}'
        invalid_request_json = {input_key: too_big_url}
        actual_validity = req.get_checker_request_validity(invalid_request_json)
        assert actual_validity is expected_validity

    def test_valid_input_returns_valid(self):
        """
        Test if the CheckerRequestValidity value returned by the corresponding method of the request validity service
        is VALID when the provided input is valid.
        """
        expected_validity = CheckerRequestValidity.VALID
        input_key = ct.get_checker_endpoint_key()
        valid_protocol_prefix = 'https'
        valid_subdomain_suffix = 'com'
        valid_domain_length = ct.get_max_input_length() - len(f'{valid_protocol_prefix}://.{valid_subdomain_suffix}')
        valid_domain = 'x' * valid_domain_length
        valid_url = f'{valid_protocol_prefix}://{valid_domain}.{valid_subdomain_suffix}'
        valid_request_json = {input_key: valid_url}
        actual_validity = req.get_checker_request_validity(valid_request_json)
        assert actual_validity is expected_validity

    def test_none_json_request_body_validity_returns_none_json_request_body_message(self):
        """
        Test if the message associated with missing headers or None request body JSON is the expected one.
        """
        expected_message = ct.get_none_json_request_body_message()
        actual_message = req.get_checker_error_message_by_validity(CheckerRequestValidity.NONE_JSON_REQUEST_BODY)
        assert actual_message == expected_message

    def test_missing_request_json_input_key_returns_missing_input_key_message(self):
        """
        Test if the message associated with missing input key is the expected one.
        """
        expected_message = ct.get_missing_input_key_message()
        actual_message = req.get_checker_error_message_by_validity(CheckerRequestValidity.MISSING_INPUT_KEY)
        assert actual_message == expected_message

    def test_none_request_json_input_key_returns_none_input_key_message(self):
        """
        Test if the message associated with None input key is the expected one.
        """
        expected_message = ct.get_none_input_key_message()
        actual_message = req.get_checker_error_message_by_validity(CheckerRequestValidity.NONE_INPUT_KEY)
        assert actual_message == expected_message

    def test_bad_url_json_input_returns_bad_url_parsing_message(self):
        """
        Test if the message associated with bad URL input is the expected one.
        """
        expected_message = ct.get_bad_url_parsing_message()
        actual_message = req.get_checker_error_message_by_validity(CheckerRequestValidity.BAD_URL_PARSING)
        assert actual_message == expected_message

    def test_valid_input_to_error_message_returns_exception_message(self):
        """
        Test if the message associated with a too big input length is the expected one.
        """
        expected_message = ct.get_bad_provided_validity_exception_message()
        with pytest.raises(ValueError, match=expected_message):
            req.get_checker_error_message_by_validity(CheckerRequestValidity.VALID)

    def test_valid_validity_value_against_invalidity_check_returns_false(self):
        """
        Test if checking for an invalid status on a VALID CheckerRequestValidity input value
        returns False.
        :return:
        """
        expected_check_result = False
        actual_check_result = req.is_invalid_request_json(CheckerRequestValidity.VALID)
        return actual_check_result == expected_check_result

    def test_none_json_request_body_validity_value_against_invalidity_check_returns_true(self):
        """
        Test if checking for an invalid status on a NONE_JSON_REQUEST_BODY CheckerRequestValidity input value
        returns True.
        """
        expected_check_result = True
        actual_check_result = req.is_invalid_request_json(CheckerRequestValidity.NONE_JSON_REQUEST_BODY)
        return actual_check_result == expected_check_result

    def test_missing_input_key_validity_value_against_invalidity_check_returns_true(self):
        """
        Test if checking for an invalid status on a MISSING_INPUT_KEY CheckerRequestValidity input value
        returns True.
        """
        expected_check_result = True
        actual_check_result = req.is_invalid_request_json(CheckerRequestValidity.MISSING_INPUT_KEY)
        return actual_check_result == expected_check_result

    def test_none_input_key_validity_value_against_invalidity_check_returns_true(self):
        """
        Test if checking for an invalid status on a NONE_INPUT_KEY CheckerRequestValidity input value
        returns True.
        """
        expected_check_result = True
        actual_check_result = req.is_invalid_request_json(CheckerRequestValidity.NONE_INPUT_KEY)
        return actual_check_result == expected_check_result

    def test_bad_url_parsing_validity_value_against_invalidity_check_returns_true(self):
        """
        Test if checking for an invalid status on a BAD_URL_PARSING CheckerRequestValidity input value
        returns True.
        """
        expected_check_result = True
        actual_check_result = req.is_invalid_request_json(CheckerRequestValidity.BAD_URL_PARSING)
        return actual_check_result == expected_check_result

    def test_too_big_input_validity_value_against_invalidity_check_returns_true(self):
        """
        Test if checking for an invalid status on a TOO_BIG_INPUT CheckerRequestValidity input value
        returns True.
        """
        expected_check_result = True
        actual_check_result = req.is_invalid_request_json(CheckerRequestValidity.TOO_BIG_INPUT)
        return actual_check_result == expected_check_result