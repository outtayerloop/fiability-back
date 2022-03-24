from newspaper import Article

from services import constants_service as ct
from tests.integration.BaseCheckerTest import BaseCheckerTest
from tests.BaseRepositoryTest import get_new_stub_entry_fiability
from datetime import date
from routes import checker_route as chkr
from BaseCheckerTest import _get_newly_created_source_by_name, _clean_checker_test, \
    _get_newly_created_entry_by_source_name, _get_newly_created_trends_by_source_name
import gc


# Enable automatic garbage collection
gc.enable()


class TestCheckerEndpointWorkflow(BaseCheckerTest):

    def test_checker_endpoint_method_with_valid_input_returns_truthfulness_percentage(self):
        """
        Test if providing the check method of the checker endpoint with a valid URL
        returns the extracted truthfulness percentage.
        """
        valid_content = {ct.get_checker_endpoint_key(): super().get_valid_url()}
        actual_body = super().get_checker_endpoint_response_body(valid_content, True)
        actual_truthfulness_percentage = actual_body[ct.get_response_content_key()]
        assert isinstance(actual_truthfulness_percentage, float)
        new_source_name = super().get_source_name()
        _clean_checker_test(new_source_name)

    def test_checker_endpoint_method_with_new_source_saves_source_data(self):
        """
        Test if providing the check method of the checker endpoint with a non already existing source URL
        saves the new source domain name in the database.
        """
        valid_content = {ct.get_checker_endpoint_key(): super().get_valid_url()}
        super().get_checker_endpoint_response_body(valid_content, True)  # Supposed to save extracted URL data as well
        new_source_name = super().get_source_name()
        actual_created_source = _get_newly_created_source_by_name(new_source_name)
        assert actual_created_source is not None  # We don't have to test the name as it was retrieved by name
        _clean_checker_test(new_source_name)

    def test_checker_endpoint_method_with_new_source_saves_entry_data(self):
        """
        Test if providing the check method of the checker endpoint with a non already existing source URL
        saves a new entry in the database.
        """
        valid_content = {ct.get_checker_endpoint_key(): super().get_valid_url()}
        super().get_checker_endpoint_response_body(valid_content, True)  # Supposed to save extracted URL data as well
        new_source_name = super().get_source_name()
        actual_created_entry = _get_newly_created_entry_by_source_name(new_source_name)
        assert actual_created_entry is not None
        _clean_checker_test(new_source_name)

    def test_checker_endpoint_method_with_new_source_has_correct_entry_title(self):
        """
        Test if providing the check method of the checker endpoint with a non already existing source URL
        saves a correct new entry title in the database.
        """
        valid_content = {ct.get_checker_endpoint_key(): super().get_valid_url()}
        super().get_checker_endpoint_response_body(valid_content, True)  # Supposed to save extracted URL data as well
        new_source_name = super().get_source_name()
        actual_created_entry = _get_newly_created_entry_by_source_name(new_source_name)
        assert actual_created_entry.title is not None and actual_created_entry.title.strip() != ''
        _clean_checker_test(new_source_name)

    def test_checker_endpoint_method_with_new_source_has_correct_entry_fiability(self):
        """
        Test if providing the check method of the checker endpoint with a non already existing source URL
        saves a correct new entry fiability in the database.
        """
        valid_content = {ct.get_checker_endpoint_key(): super().get_valid_url()}
        super().get_checker_endpoint_response_body(valid_content, True)  # Supposed to save extracted URL data as well
        new_source_name = super().get_source_name()
        actual_created_entry = _get_newly_created_entry_by_source_name(new_source_name)
        assert actual_created_entry.fiability is not None
        _clean_checker_test(new_source_name)

    def test_checker_endpoint_method_with_new_source_has_correct_entry_search_count(self):
        """
        Test if providing the check method of the checker endpoint with a non already existing source URL
        saves a correct new entry search count in the database.
        """
        expected_search_count = 1  # The search count equals 1 the first time this entry is inserted in the database.
        valid_content = {ct.get_checker_endpoint_key(): super().get_valid_url()}
        super().get_checker_endpoint_response_body(valid_content, True)  # Supposed to save extracted URL data as well
        new_source_name = super().get_source_name()
        actual_created_entry = _get_newly_created_entry_by_source_name(new_source_name)
        assert actual_created_entry.search_count == expected_search_count
        _clean_checker_test(new_source_name)

    def test_checker_endpoint_method_with_new_source_saves_trend_data(self):
        """
        Test if providing the check method of the checker endpoint with a non already existing source URL
        saves a new trend in the database.
        """
        valid_content = {ct.get_checker_endpoint_key(): super().get_valid_url()}
        super().get_checker_endpoint_response_body(valid_content, True)  # Supposed to save extracted URL data as well
        new_source_name = super().get_source_name()
        actual_created_trend = _get_newly_created_trends_by_source_name(new_source_name)[0]
        assert actual_created_trend is not None
        _clean_checker_test(new_source_name)

    def test_checker_endpoint_method_with_new_source_has_correct_trend_date(self):
        """
        Test if providing the check method of the checker endpoint with a non already existing source URL
        saves a correct new trend date in the database.
        """
        expected_trend_date = date.today()
        valid_content = {ct.get_checker_endpoint_key(): super().get_valid_url()}
        super().get_checker_endpoint_response_body(valid_content, True)  # Supposed to save extracted URL data as well
        new_source_name = super().get_source_name()
        actual_created_trend = _get_newly_created_trends_by_source_name(new_source_name)[0]
        assert actual_created_trend.trend_date == expected_trend_date
        _clean_checker_test(new_source_name)

    def test_checker_endpoint_method_with_new_source_has_correct_trend_topic(self):
        """
        Test if providing the check method of the checker endpoint with a non already existing source URL
        saves a correct new trend topic in the database.
        """
        valid_content = {ct.get_checker_endpoint_key(): super().get_valid_url()}
        super().get_checker_endpoint_response_body(valid_content, True)  # Supposed to save extracted URL data as well
        new_source_name = super().get_source_name()
        actual_created_trend = _get_newly_created_trends_by_source_name(new_source_name)[0]
        assert actual_created_trend.topic is not None and actual_created_trend.topic.strip() != ''
        _clean_checker_test(new_source_name)

    def test_checker_endpoint_method_with_already_existing_source_does_not_change_existing_source_id(self):
        """
        Test if providing the check method of the checker endpoint with an already existing source URL
        does not change the already saved source ID in the database.
        """
        new_source_name = super().get_source_name()
        valid_content = {ct.get_checker_endpoint_key(): super().get_valid_url()}
        super().get_checker_endpoint_response_body(valid_content, True)
        expected_retrieved_source_id = _get_newly_created_source_by_name(new_source_name).id
        super().get_checker_endpoint_response_body(valid_content, True)  # Already existing source in the database
        actual_retrieved_source_id = _get_newly_created_source_by_name(new_source_name).id
        assert actual_retrieved_source_id == expected_retrieved_source_id
        _clean_checker_test(new_source_name)

    def test_checker_endpoint_method_with_already_existing_source_does_not_change_existing_source_name(self):
        """
        Test if providing the check method of the checker endpoint with an already existing source URL
        does not change the already saved source domain name in the database.
        """
        new_source_name = super().get_source_name()
        valid_content = {ct.get_checker_endpoint_key(): super().get_valid_url()}
        super().get_checker_endpoint_response_body(valid_content, True)
        expected_retrieved_source_name = _get_newly_created_source_by_name(new_source_name).name
        super().get_checker_endpoint_response_body(valid_content, True)  # Already existing source in the database
        actual_retrieved_source_name = _get_newly_created_source_by_name(new_source_name).name
        assert actual_retrieved_source_name == expected_retrieved_source_name
        _clean_checker_test(new_source_name)

    def test_checker_endpoint_method_with_already_existing_entry_does_not_change_existing_entry_id(self):
        """
        Test if providing the check method of the checker endpoint with an already existing entry
        does not change the already saved associated entry in the database.
        """
        new_source_name = super().get_source_name()
        valid_content = {ct.get_checker_endpoint_key(): super().get_valid_url()}
        super().get_checker_endpoint_response_body(valid_content, True)
        expected_retrieved_entry_id = _get_newly_created_entry_by_source_name(new_source_name).id
        super().get_checker_endpoint_response_body(valid_content, True)  # Already existing entry in the database
        actual_retrieved_entry_id = _get_newly_created_entry_by_source_name(new_source_name).id
        assert actual_retrieved_entry_id == expected_retrieved_entry_id
        _clean_checker_test(new_source_name)

    def test_checker_endpoint_method_with_already_existing_entry_does_not_change_existing_entry_fiability(self):
        """
        Test if providing the check method of the checker endpoint with an already existing entry
        does not change the already saved associated entry fiability in the database.
        """
        new_source_name = super().get_source_name()
        valid_content = {ct.get_checker_endpoint_key(): super().get_valid_url()}
        super().get_checker_endpoint_response_body(valid_content, True)
        expected_retrieved_entry_fiability = _get_newly_created_entry_by_source_name(new_source_name).fiability
        super().get_checker_endpoint_response_body(valid_content, True)  # Already existing entry in the database
        actual_retrieved_entry_fiability = _get_newly_created_entry_by_source_name(new_source_name).fiability
        assert actual_retrieved_entry_fiability == expected_retrieved_entry_fiability
        _clean_checker_test(new_source_name)

    def test_checker_endpoint_method_with_already_existing_entry_does_not_change_existing_entry_title(self):
        """
        Test if providing the check method of the checker endpoint with an already existing entry
        does not change the already saved associated entry title in the database.
        """
        new_source_name = super().get_source_name()
        valid_content = {ct.get_checker_endpoint_key(): super().get_valid_url()}
        super().get_checker_endpoint_response_body(valid_content, True)
        expected_retrieved_entry_title = _get_newly_created_entry_by_source_name(new_source_name).title
        super().get_checker_endpoint_response_body(valid_content, True)  # Already existing entry in the database
        actual_retrieved_entry_title = _get_newly_created_entry_by_source_name(new_source_name).title
        assert actual_retrieved_entry_title == expected_retrieved_entry_title
        _clean_checker_test(new_source_name)

    def test_checker_endpoint_method_with_already_existing_entry_increments_entry_search_count(self):
        """
        Test if providing the check method of the checker endpoint with an already existing entry
        increments the already saved associated entry search count in the database.
        """
        new_source_name = super().get_source_name()
        valid_content = {ct.get_checker_endpoint_key(): super().get_valid_url()}
        super().get_checker_endpoint_response_body(valid_content, True)
        expected_retrieved_entry_search_count = _get_newly_created_entry_by_source_name(new_source_name).search_count + 1
        super().get_checker_endpoint_response_body(valid_content, True)  # Already existing entry in the database
        actual_retrieved_entry_search_count = _get_newly_created_entry_by_source_name(new_source_name).search_count
        assert actual_retrieved_entry_search_count == expected_retrieved_entry_search_count
        _clean_checker_test(new_source_name)

    def test_checker_endpoint_method_with_already_existing_trend_adds_new_trend(self):
        """
        Test if providing the check method of the checker endpoint with an already existing trend
        inserts the new provided trend in the database.
        """
        expected_trend_count = 2
        new_source_name = super().get_source_name()
        valid_content = {ct.get_checker_endpoint_key(): super().get_valid_url()}
        super().get_checker_endpoint_response_body(valid_content, True)
        super().get_checker_endpoint_response_body(valid_content, True)  # Already existing trend in the database
        actual_trend_count = len(_get_newly_created_trends_by_source_name(new_source_name))
        assert actual_trend_count == expected_trend_count
        _clean_checker_test(new_source_name)

    def test_checker_endpoint_method_with_already_existing_trend_has_same_topic(self):
        """
        Test if providing the check method of the checker endpoint with an already existing trend
        inserts the new provided trend in the database with the same already existing topic
        (no new topic for the same trend).
        """
        new_source_name = super().get_source_name()
        valid_content = {ct.get_checker_endpoint_key(): super().get_valid_url()}
        super().get_checker_endpoint_response_body(valid_content, True)
        expected_trend_topic = _get_newly_created_trends_by_source_name(new_source_name)[0].topic
        super().get_checker_endpoint_response_body(valid_content, True)  # Already existing trend in the database
        actual_trend_topic = _get_newly_created_trends_by_source_name(new_source_name)[-1].topic
        assert actual_trend_topic == expected_trend_topic
        _clean_checker_test(new_source_name)

    def test_save_user_input_data_with_new_source_saves_source_data(self):
        """
        Test if providing the user input save method of the checker endpoint with a non already existing source URL
        saves a new source in the database.
        """
        valid_url = super().get_valid_url()
        chkr._save_user_input_data(valid_url, self._get_valid_stub_article(), get_new_stub_entry_fiability())
        new_source_name = super().get_source_name()
        actual_created_source = _get_newly_created_source_by_name(new_source_name)
        assert actual_created_source is not None
        _clean_checker_test(new_source_name)

    def test_save_user_input_data_with_new_source_saves_entry_data(self):
        """
        Test if providing the user input save method of the checker endpoint with a non already existing entry URL
        saves a new entry in the database.
        """
        valid_url = super().get_valid_url()
        chkr._save_user_input_data(valid_url, self._get_valid_stub_article(), get_new_stub_entry_fiability())
        new_source_name = super().get_source_name()
        actual_created_entry = _get_newly_created_entry_by_source_name(new_source_name)
        assert actual_created_entry is not None
        _clean_checker_test(new_source_name)

    def test_save_user_input_data_with_new_source_has_correct_entry_title(self):
        """
        Test if providing the user input save method of the checker endpoint with a non already existing entry URL
        saves a new entry with the correct title in the database.
        """
        expected_entry_title = self._get_valid_stub_article().title
        valid_url = super().get_valid_url()
        chkr._save_user_input_data(valid_url, self._get_valid_stub_article(), get_new_stub_entry_fiability())
        new_source_name = super().get_source_name()
        actual_entry_title = _get_newly_created_entry_by_source_name(new_source_name).title
        assert actual_entry_title == expected_entry_title
        _clean_checker_test(new_source_name)

    def test_save_user_input_data_with_new_source_has_correct_entry_fiability(self):
        """
        Test if providing the user input save method of the checker endpoint with a non already existing entry URL
        saves a new entry with the correct fiability in the database.
        """
        expected_entry_fiability = get_new_stub_entry_fiability()
        valid_url = super().get_valid_url()
        chkr._save_user_input_data(valid_url, self._get_valid_stub_article(), get_new_stub_entry_fiability())
        new_source_name = super().get_source_name()
        actual_entry_fiability = _get_newly_created_entry_by_source_name(new_source_name).fiability
        assert actual_entry_fiability == expected_entry_fiability
        _clean_checker_test(new_source_name)

    def test_save_user_input_data_with_new_source_has_correct_entry_search_count(self):
        """
        Test if providing the user input save method of the checker endpoint with a non already existing entry URL
        saves a new entry with the correct search count in the database.
        """
        expected_entry_search_count = 1
        valid_url = super().get_valid_url()
        chkr._save_user_input_data(valid_url, self._get_valid_stub_article(), get_new_stub_entry_fiability())
        new_source_name = super().get_source_name()
        actual_entry_search_count = _get_newly_created_entry_by_source_name(new_source_name).search_count
        assert actual_entry_search_count == expected_entry_search_count
        _clean_checker_test(new_source_name)

    def test_save_user_input_data_with_new_source_has_correct_saves_trend_data(self):
        """
        Test if providing the user input save method of the checker endpoint with a non already existing trend URL
        saves a new trend in the database.
        """
        valid_url = super().get_valid_url()
        chkr._save_user_input_data(valid_url, self._get_valid_stub_article(), get_new_stub_entry_fiability())
        new_source_name = super().get_source_name()
        actual_created_trend = _get_newly_created_trends_by_source_name(new_source_name)[0]
        assert actual_created_trend is not None
        _clean_checker_test(new_source_name)

    def test_save_user_input_data_with_new_source_has_correct_trend_date(self):
        """
        Test if providing the user input save method of the checker endpoint with a non already existing trend URL
        saves a new trend with the correct date in the database.
        """
        expected_trend_date = date.today()
        valid_url = super().get_valid_url()
        chkr._save_user_input_data(valid_url, self._get_valid_stub_article(), get_new_stub_entry_fiability())
        new_source_name = super().get_source_name()
        actual_trend_date = _get_newly_created_trends_by_source_name(new_source_name)[0].trend_date
        assert actual_trend_date == expected_trend_date
        _clean_checker_test(new_source_name)

    def test_save_user_input_data_with_already_existing_source_does_not_change_existing_source_id(self):
        """
        Test if providing the user input save method of the checker endpoint with an already existing source URL
        does not change the already saved source ID in the database.
        """
        new_source_name = super().get_source_name()
        valid_url = super().get_valid_url()
        chkr._save_user_input_data(valid_url, self._get_valid_stub_article(), get_new_stub_entry_fiability())
        expected_retrieved_source_id = _get_newly_created_source_by_name(new_source_name).id
        chkr._save_user_input_data(valid_url, self._get_valid_stub_article(), get_new_stub_entry_fiability())
        actual_retrieved_source_id = _get_newly_created_source_by_name(new_source_name).id
        assert actual_retrieved_source_id == expected_retrieved_source_id
        _clean_checker_test(new_source_name)

    def test_save_user_input_data_with_already_existing_source_does_not_change_existing_source_name(self):
        """
        Test if providing the user input save method of the checker endpoint with an already existing source URL
        does not change the already saved source name in the database.
        """
        new_source_name = super().get_source_name()
        valid_url = super().get_valid_url()
        chkr._save_user_input_data(valid_url, self._get_valid_stub_article(), get_new_stub_entry_fiability())
        expected_retrieved_source_name = _get_newly_created_source_by_name(new_source_name).name
        chkr._save_user_input_data(valid_url, self._get_valid_stub_article(), get_new_stub_entry_fiability())
        actual_retrieved_source_name = _get_newly_created_source_by_name(new_source_name).name
        assert actual_retrieved_source_name == expected_retrieved_source_name
        _clean_checker_test(new_source_name)

    def test_save_user_input_data_with_already_existing_source_does_not_change_existing_entry_id(self):
        """
        Test if providing the user input save method of the checker endpoint with an already existing source URL
        does not change the already saved entry ID in the database.
        """
        new_source_name = super().get_source_name()
        valid_url = super().get_valid_url()
        chkr._save_user_input_data(valid_url, self._get_valid_stub_article(), get_new_stub_entry_fiability())
        expected_retrieved_entry_id = _get_newly_created_entry_by_source_name(new_source_name).id
        chkr._save_user_input_data(valid_url, self._get_valid_stub_article(), get_new_stub_entry_fiability())
        actual_retrieved_entry_id = _get_newly_created_entry_by_source_name(new_source_name).id
        assert actual_retrieved_entry_id == expected_retrieved_entry_id
        _clean_checker_test(new_source_name)

    def test_save_user_input_data_with_already_existing_source_does_not_change_existing_entry_fiability(self):
        """
        Test if providing the user input save method of the checker endpoint with an already existing source URL
        does not change the already saved entry fiability in the database.
        """
        new_source_name = super().get_source_name()
        valid_url = super().get_valid_url()
        chkr._save_user_input_data(valid_url, self._get_valid_stub_article(), get_new_stub_entry_fiability())
        expected_retrieved_entry_fiability = _get_newly_created_entry_by_source_name(new_source_name).fiability
        chkr._save_user_input_data(valid_url, self._get_valid_stub_article(), get_new_stub_entry_fiability())
        actual_retrieved_entry_fiability = _get_newly_created_entry_by_source_name(new_source_name).fiability
        assert actual_retrieved_entry_fiability == expected_retrieved_entry_fiability
        _clean_checker_test(new_source_name)

    def test_save_user_input_data_with_already_existing_source_does_not_change_existing_entry_title(self):
        """
        Test if providing the user input save method of the checker endpoint with an already existing source URL
        does not change the already saved entry title in the database.
        """
        new_source_name = super().get_source_name()
        valid_url = super().get_valid_url()
        chkr._save_user_input_data(valid_url, self._get_valid_stub_article(), get_new_stub_entry_fiability())
        expected_retrieved_entry_title = _get_newly_created_entry_by_source_name(new_source_name).title
        chkr._save_user_input_data(valid_url, self._get_valid_stub_article(), get_new_stub_entry_fiability())
        actual_retrieved_entry_title = _get_newly_created_entry_by_source_name(new_source_name).title
        assert actual_retrieved_entry_title == expected_retrieved_entry_title
        _clean_checker_test(new_source_name)

    def test_save_user_input_data_with_already_existing_source_increments_entry_search_count(self):
        """
        Test if providing the user input save method of the checker endpoint with an already existing source URL
        increments the already saved associated entry search count in the database.
        """
        new_source_name = super().get_source_name()
        valid_url = super().get_valid_url()
        chkr._save_user_input_data(valid_url, self._get_valid_stub_article(), get_new_stub_entry_fiability())
        expected_retrieved_entry_search_count = _get_newly_created_entry_by_source_name(new_source_name).search_count + 1
        chkr._save_user_input_data(valid_url, self._get_valid_stub_article(), get_new_stub_entry_fiability())
        actual_retrieved_entry_search_count = _get_newly_created_entry_by_source_name(new_source_name).search_count
        assert actual_retrieved_entry_search_count == expected_retrieved_entry_search_count
        _clean_checker_test(new_source_name)

    def test_save_user_input_data_with_already_existing_trend_adds_new_trend(self):
        """
        Test if providing the user input save method method of the checker endpoint with an already existing trend
        inserts the new provided trend in the database.
        """
        expected_trend_count = 2
        new_source_name = super().get_source_name()
        valid_url = super().get_valid_url()
        chkr._save_user_input_data(valid_url, self._get_valid_stub_article(), get_new_stub_entry_fiability())
        chkr._save_user_input_data(valid_url, self._get_valid_stub_article(), get_new_stub_entry_fiability())
        actual_trend_count = len(_get_newly_created_trends_by_source_name(new_source_name))
        assert actual_trend_count == expected_trend_count
        _clean_checker_test(new_source_name)

    def test_save_user_input_data_with_already_existing_trend_has_same_topic(self):
        """
        Test if providing the user input save method method of the checker endpoint with an already existing trend
        inserts the new provided trend in the database with the same already existing topic
        (no new topic for the same trend).
        """
        new_source_name = super().get_source_name()
        valid_url = super().get_valid_url()
        chkr._save_user_input_data(valid_url, self._get_valid_stub_article(), get_new_stub_entry_fiability())
        expected_trend_topic = _get_newly_created_trends_by_source_name(new_source_name)[0].topic
        chkr._save_user_input_data(valid_url, self._get_valid_stub_article(), get_new_stub_entry_fiability())
        actual_trend_topic = _get_newly_created_trends_by_source_name(new_source_name)[-1].topic
        assert actual_trend_topic == expected_trend_topic
        _clean_checker_test(new_source_name)

    def _get_valid_stub_article(self) -> Article:
        """
        Return a new valid stub Article object with the valid URL used by the parent class and stub title and text.
        :return: a new valid stub Article object with the valid URL used by the parent class and stub title and text
        """
        valid_url = super().get_valid_url()
        valid_title = 'valid_title'
        valid_text = 'valid_text'
        return Article(url=valid_url, title=valid_title, text=valid_text)