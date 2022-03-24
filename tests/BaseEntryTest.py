from datetime import date

from entities.data.EntryData import EntryData
from entities.data.TrendData import TrendData
from entities.models.Entry import Entry
from entities.models.Trend import Trend
from tests.BaseRepositoryTest import BaseRepositoryTest, get_new_stub_entry_fiability
import gc
from entities.models.BaseModel import connect_to_db, close_db


# Enable automatic garbage collection
gc.enable()


def _insert_stub_entry_range_in_database(stub_entries_specs: list[EntryData]) -> list[int]:
    """
    Insert in the database the 5 entries created to test if getting the top 4 entries by search count
    returns the correct data and return the associated entry ID list.
    :param stub_entries_specs: stub entries to insert in the database
    :return: the inserted entry ID list
    """
    connect_to_db()
    created_stub_entries = [
        Entry.create(
            fiability=stub_entry_spec.fiability,
            source_id=stub_entry_spec.source_id,
            title=stub_entry_spec.title,
            search_count=stub_entry_spec.search_count
        ).id
        for stub_entry_spec in stub_entries_specs
    ]
    close_db()
    return created_stub_entries


def _insert_stub_trend_range_in_database(stub_trends_specs: list[TrendData]) -> list[int]:
    """
    Insert in the database the 5 trends associated to the 5 entries created to test if getting the top 4 entries
    by search count returns the correct data and return the associated entry ID list.
    :param stub_trends_specs: stub trends to insert in the database
    :return: the inserted trend ID list
    """
    connect_to_db()
    created_stub_trends = [
        Trend.create(
            trend_date=stub_trend_spec.trend_date,
            topic=stub_trend_spec.topic,
            entry_id=stub_trend_spec.entry_id
        ).id
        for stub_trend_spec in stub_trends_specs
    ]
    close_db()
    return created_stub_trends


class BaseEntryTest(BaseRepositoryTest):

    def _get_five_stub_entries_specs_by_decreasing_search_count(self, stub_source_id: int) -> list[EntryData]:
        """
        Return 5 entries created to test if getting the top 4 entries by search count
        returns the correct data.
        :param stub_source_id: source ID used to create all stub entries
        :return: a list containing the 5 created stub EntryData objects
        """
        max_search_count = 2147483647  # Max 32 bits integer value.
        new_stub_entry_title = super().get_new_stub_entry_title()
        connect_to_db()
        created_stub_entries = [
            EntryData(
                id=None,
                fiability=get_new_stub_entry_fiability(),
                title=f'{new_stub_entry_title}_{str(i)}',
                source_id=stub_source_id,
                search_count=max_search_count - i + 1  # Decrease the search count by 1 for each newly created stub entry
            )
            for i in range(1, 6)  # 5 entries created to test top 4 entries by search count
        ]
        close_db()
        return created_stub_entries

    def _get_five_stub_trends_specs_from_five_stub_entries(self, stub_entries_id_list: list[int]) -> list[TrendData]:
        """
        Return 5 trends associated to the 5 entries created to test if getting the top 4 entries by search count
        returns the correct data.
        :param stub_entries_id_list: associated stub entry ID list
        :return: a list containing the 5 created stub TrendData objects
        """
        stub_prefix = super().get_stub_prefix()
        connect_to_db()
        created_stub_trends = [
            TrendData(
                trend_date=date.today(),
                topic=f'{stub_prefix}_topic_{str(index + 1)}',
                entry_id=stub_entry_id
            )
            for index, stub_entry_id in enumerate(stub_entries_id_list)
        ]
        close_db()
        return created_stub_trends