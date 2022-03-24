from tests.BaseRepositoryTest import BaseRepositoryTest, remove_newly_created_source_by_id, \
    remove_newly_created_entry_by_id, remove_newly_created_trend_by_id
from entities.data.TrendData import TrendData
from datetime import date
from entities.models.Trend import Trend
from repositories import trend_repository as tr
from typing import Optional
import gc
from entities.models.BaseModel import connect_to_db, close_db


# Enable automatic garbage collection
gc.enable()


def _get_newly_created_trend(trend_id: int) -> Optional[TrendData]:
    """
    Return the found TrendData instance from the provided trend ID, otherwise return None if
    no trend with the provided ID already exists in the database.
    :param trend_id: the provided trend ID.
    :return: the found TrendData instance or None.
    """
    connect_to_db()
    created_trend = Trend.get_or_none(Trend.id == trend_id)
    close_db()
    if created_trend is None:
        return None
    return TrendData(created_trend.id, created_trend.trend_date, created_trend.topic, created_trend.entry.id)


def _clean_trend_insertion_test(trend_specs: TrendData, source_id: int):
    """
    Remove the previously test-purpose created stub trend, stub entry and stub source from the database
    :param trend_specs: the previously created trend specifications.
    :param trend_specs: the previously created source identifier.
    """
    remove_newly_created_trend_by_id(trend_specs.id)
    remove_newly_created_entry_by_id(trend_specs.entry_id)
    remove_newly_created_source_by_id(source_id)


class TestTrendRepository(BaseRepositoryTest):

    def test_add_new_trend_inserts_in_database(self):
        """
        Test if adding a new trend
        effectively inserts a data row in the trends database table.
        """
        (new_stub_trend_specs, new_stub_source_id) = self._get_new_trend_specs()
        newly_created_trend_id = tr.add(new_stub_trend_specs)
        actual_created_trend = _get_newly_created_trend(newly_created_trend_id)
        assert actual_created_trend is not None
        _clean_trend_insertion_test(actual_created_trend, new_stub_source_id)

    def test_add_new_trend_has_correct_date(self):
        """
        Test if adding a new trend
        and getting its date returns the correct date.
        """
        (new_stub_trend_specs, new_stub_source_id) = self._get_new_trend_specs()
        expected_created_trend_date = new_stub_trend_specs.trend_date
        newly_created_trend_id = tr.add(new_stub_trend_specs)
        actual_created_trend = _get_newly_created_trend(newly_created_trend_id)
        assert actual_created_trend.trend_date == expected_created_trend_date
        _clean_trend_insertion_test(actual_created_trend, new_stub_source_id)

    def test_add_new_trend_has_correct_topic(self):
        """
        Test if adding a new trend
        and getting its topic returns the correct topic.
        """
        (new_stub_trend_specs, new_stub_source_id) = self._get_new_trend_specs()
        expected_created_trend_topic = new_stub_trend_specs.topic
        newly_created_trend_id = tr.add(new_stub_trend_specs)
        actual_created_trend = _get_newly_created_trend(newly_created_trend_id)
        assert actual_created_trend.topic == expected_created_trend_topic
        _clean_trend_insertion_test(actual_created_trend, new_stub_source_id)

    def test_add_new_trend_has_correct_entry_id(self):
        """
        Test if adding a new trend
        and getting its entry ID returns the correct entry ID.
        """
        (new_stub_trend_specs, new_stub_source_id) = self._get_new_trend_specs()
        expected_created_trend_entry_id = new_stub_trend_specs.entry_id
        newly_created_trend_id = tr.add(new_stub_trend_specs)
        actual_created_trend = _get_newly_created_trend(newly_created_trend_id)
        assert actual_created_trend.entry_id == expected_created_trend_entry_id
        _clean_trend_insertion_test(actual_created_trend, new_stub_source_id)

    def _get_new_trend_specs(self) -> tuple[TrendData, int]:
        """
        Return a tuple containing the trend to create data and the associated source ID.
        :return: a tuple containing the trend to create data and the associated source ID
        """
        new_stub_source_id = super().add_new_stub_source().id
        new_stub_entry_id = super().add_new_stub_entry(new_stub_source_id)
        new_stub_trend_specs = TrendData(
            trend_date=date.today(),
            topic=f'{super().get_stub_prefix()}_topic',
            entry_id=new_stub_entry_id.id
        )
        return new_stub_trend_specs, new_stub_source_id