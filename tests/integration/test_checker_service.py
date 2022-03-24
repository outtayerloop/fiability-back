from tests.integration.BaseCheckerTest import BaseCheckerTest
from services import checker_service as chk
from services import constants_service as ct
from BaseCheckerTest import _get_newly_created_source_by_name, _clean_checker_test, \
    _get_newly_created_entry_by_source_name, _get_newly_created_trends_by_source_name
from tests.BaseRepositoryTest import BaseRepositoryTest, get_new_stub_entry_fiability
import gc


# Enable automatic garbage collection
gc.enable()


class TestCheckerService(BaseCheckerTest, BaseRepositoryTest):

    def test_check_text_returns_truthfulness_label(self):
        """
        Test if checking a text returns its truthfulness label.
        """
        expected_truthfulness_labels = [ct.get_truthfulness_label(), ct.get_wrongness_label()]
        valid_text = 'valid_text'
        actual_truthfulness_label = chk._get_truthfulness_label(valid_text)
        assert actual_truthfulness_label in expected_truthfulness_labels

    def test_add_source_by_url_with_new_source_saves_source_data(self):
        """
        Test if providing the source add method of the checker service with a non already existing source URL
        saves the new source domain name in the database.
        """
        valid_url = super().get_valid_url()
        new_source_name = super().get_source_name()
        chk.add_source_by_url(valid_url)
        actual_created_source = _get_newly_created_source_by_name(new_source_name)
        assert actual_created_source is not None
        _clean_checker_test(new_source_name)

    def test_add_source_by_url_with_new_source_returns_correct_id(self):
        """
        Test if providing the source add method of the checker service with a non already existing source URL
        returns the correct ID.
        """
        valid_url = super().get_valid_url()
        new_source_name = super().get_source_name()
        actual_source_id = chk.add_source_by_url(valid_url)
        expected_source_id = _get_newly_created_source_by_name(new_source_name).id
        assert actual_source_id == expected_source_id
        _clean_checker_test(new_source_name)

    def test_add_entry_with_new_entry_saves_entry_data(self):
        """
        Test if providing the entry add method of the checker service with a non already existing entry
        saves the new entry in the database.
        """
        valid_title = 'valid_title'
        new_source_name = super().get_source_name()
        new_stub_source = super().add_new_stub_source(new_source_name)
        chk.add_entry(new_stub_source.id, valid_title, get_new_stub_entry_fiability())
        actual_created_entry = _get_newly_created_entry_by_source_name(new_source_name)
        assert actual_created_entry is not None
        _clean_checker_test(new_source_name)

    def test_add_entry_with_new_entry_returns_correct_id(self):
        """
        Test if providing the entry add method of the checker service with a non already existing entry
        returns the correct ID.
        """
        valid_title = 'valid_title'
        new_source_name = super().get_source_name()
        new_stub_source = super().add_new_stub_source(new_source_name)
        actual_entry_id = chk.add_entry(new_stub_source.id, valid_title, get_new_stub_entry_fiability())
        expected_entry_id = _get_newly_created_entry_by_source_name(new_source_name).id
        assert actual_entry_id == expected_entry_id
        _clean_checker_test(new_source_name)

    def test_add_entry_with_existing_entry_increments_search_count(self):
        """
        Test if providing the entry add method of the checker service with an already existing entry
        increments the entry search count.
        """
        expected_entry_search_count = 2
        valid_title = 'valid_title'
        new_source_name = super().get_source_name()
        new_stub_source = super().add_new_stub_source(new_source_name)
        chk.add_entry(new_stub_source.id, valid_title, get_new_stub_entry_fiability())
        chk.add_entry(new_stub_source.id, valid_title, get_new_stub_entry_fiability())
        actual_entry_search_count = _get_newly_created_entry_by_source_name(new_source_name).search_count
        assert actual_entry_search_count == expected_entry_search_count
        _clean_checker_test(new_source_name)

    def test_add_trend_with_new_trend_saves_trend_data(self):
        """
        Test if providing the entry add method of the checker service with a non already existing trend
        saves the new trend in the database.
        """
        valid_title = 'valid_title'
        valid_text = 'valid_text'
        new_source_name = super().get_source_name()
        new_stub_source = super().add_new_stub_source(new_source_name)
        new_stub_entry = super().add_new_stub_entry(new_stub_source.id, valid_title)
        chk.add_trend(valid_text, new_stub_entry.id)
        actual_created_trend = _get_newly_created_trends_by_source_name(new_source_name)
        assert actual_created_trend is not None and len(actual_created_trend) == 1
        _clean_checker_test(new_source_name)

    def test_add_trend_with_existing_trend_adds_trend_data(self):
        """
        Test if providing the entry add method of the checker service with an already existing trend
        saves the new trend in the database.
        """
        expected_trend_count = 2
        valid_title = 'valid_title'
        valid_text = 'valid_text'
        new_source_name = super().get_source_name()
        new_stub_source = super().add_new_stub_source(new_source_name)
        new_stub_entry = super().add_new_stub_entry(new_stub_source.id, valid_title)
        chk.add_trend(valid_text, new_stub_entry.id)
        chk.add_trend(valid_text, new_stub_entry.id)
        actual_created_trend_count = len(_get_newly_created_trends_by_source_name(new_source_name))
        assert actual_created_trend_count == expected_trend_count
        _clean_checker_test(new_source_name)