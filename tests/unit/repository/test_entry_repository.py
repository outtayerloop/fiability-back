from entities.data.TrendData import TrendData
from tests.BaseEntryTest import BaseEntryTest, _insert_stub_entry_range_in_database, \
    _insert_stub_trend_range_in_database
from tests.BaseRepositoryTest import remove_newly_created_source_by_id, \
    remove_newly_created_entry_by_id, get_new_stub_entry_fiability, \
    get_new_stub_entry_search_count, remove_newly_created_trend_by_id
from repositories import entry_repository as er
from entities.data.EntryData import EntryData
from entities.models.Entry import Entry
from typing import Optional
import gc
from entities.models.BaseModel import connect_to_db, close_db


# Enable automatic garbage collection
gc.enable()


def _get_newly_created_entry(entry_id: int) -> Optional[EntryData]:
    """
    Return the found EntryData instance from the provided created entry ID, otherwise return None if
    no entry with the provided ID already exists in the database.
    :param entry_id: the provided created entry ID.
    :return: the found EntryData instance or None.
    """
    connect_to_db()
    created_entry = Entry.get_or_none(Entry.id == entry_id)
    close_db()
    if created_entry is None:
        return None
    return EntryData(
        created_entry.id,
        created_entry.fiability,
        created_entry.title,
        created_entry.source.id,
        created_entry.search_count
    )


def _get_expected_top_four_result(stub_entries_specs: list[EntryData], stub_trends_specs: list[TrendData]) \
        -> list[tuple[str, str]]:
    """
    Return the expected top four searched entries list
    :param stub_entries_specs: newly created entries specifications
    :param stub_trends_specs: newly created trends specifications
    :return: a list containing each entry title and its associated topic
    """
    stub_specs_zip = zip(stub_entries_specs[:-1], stub_trends_specs[:-1])  # Take only the first 4 entities
    return [
        (str(stub_entry.title), str(stub_trend.topic))  # Cast to str here to compare str instead of Optional[str]
        for stub_entry, stub_trend in stub_specs_zip
    ]


class TestEntryRepository(BaseEntryTest):

    def test_get_nonexistent_entry_by_index_returns_none(self):
        """
        Test if getting a non-existing entry by its index
        returns None.
        """
        invalid_entry_source_id = -1
        invalid_entry_title = 'test_get_nonexistent_entry_by_index_returns_none'
        actual_found_entry = er.get_by_index(invalid_entry_source_id, invalid_entry_title)
        assert actual_found_entry is None

    def test_get_existing_entry_by_index_returns_entry(self):
        """
        Test if getting an existing entry by its index
        effectively returns a data row from the entries database table.
        """
        new_stub_source_id = super().add_new_stub_source().id
        new_stub_entry = super().add_new_stub_entry(new_stub_source_id)
        actual_found_entry = er.get_by_index(new_stub_source_id, new_stub_entry.title)
        assert actual_found_entry is not None
        remove_newly_created_source_by_id(new_stub_source_id)
        remove_newly_created_entry_by_id(new_stub_entry.id)

    def test_get_existing_entry_by_index_has_correct_fiability(self):
        """
        Test if getting an existing entry by its index
        returns the correct entry fiability.
        """
        new_stub_source_id = super().add_new_stub_source().id
        new_stub_entry = super().add_new_stub_entry(new_stub_source_id)
        expected_new_stub_entry_fiability = new_stub_entry.fiability
        actual_found_entry = er.get_by_index(new_stub_source_id, new_stub_entry.title)
        assert actual_found_entry.fiability == expected_new_stub_entry_fiability
        remove_newly_created_source_by_id(new_stub_source_id)
        remove_newly_created_entry_by_id(new_stub_entry.id)

    def test_get_existing_entry_by_index_has_correct_source_id(self):
        """
        Test if getting an existing entry by its index
        returns the correct entry source ID.
        """
        new_stub_source_id = super().add_new_stub_source().id
        new_stub_entry = super().add_new_stub_entry(new_stub_source_id)
        expected_new_stub_entry_source_id = new_stub_entry.source_id
        actual_found_entry = er.get_by_index(new_stub_source_id, new_stub_entry.title)
        assert actual_found_entry.source.id == expected_new_stub_entry_source_id
        remove_newly_created_source_by_id(new_stub_source_id)
        remove_newly_created_entry_by_id(new_stub_entry.id)

    def test_get_existing_entry_by_index_has_correct_title(self):
        """
        Test if getting an existing entry by its index
        returns the correct entry title.
        """
        new_stub_source_id = super().add_new_stub_source().id
        new_stub_entry = super().add_new_stub_entry(new_stub_source_id)
        expected_new_stub_entry_title = new_stub_entry.title
        actual_found_entry = er.get_by_index(new_stub_source_id, new_stub_entry.title)
        assert actual_found_entry.title == expected_new_stub_entry_title
        remove_newly_created_source_by_id(new_stub_source_id)
        remove_newly_created_entry_by_id(new_stub_entry.id)

    def test_get_existing_entry_by_index_has_correct_search_count(self):
        """
        Test if getting an existing entry by its index
        returns the correct entry search count.
        """
        new_stub_source_id = super().add_new_stub_source().id
        new_stub_entry = super().add_new_stub_entry(new_stub_source_id)
        expected_new_stub_entry_search_count = new_stub_entry.search_count
        actual_found_entry = er.get_by_index(new_stub_source_id, new_stub_entry.title)
        assert actual_found_entry.search_count == expected_new_stub_entry_search_count
        remove_newly_created_source_by_id(new_stub_source_id)
        remove_newly_created_entry_by_id(new_stub_entry.id)

    def test_add_new_entry_inserts_in_database(self):
        """
        Test if adding a new entry
        effectively inserts a data row in the entries database table.
        """
        (new_stub_entry_specs, new_stub_source_id) = self._get_new_entry_specs()
        newly_created_entry_id = er.add(new_stub_entry_specs)
        actual_created_entry = _get_newly_created_entry(newly_created_entry_id)
        assert actual_created_entry is not None
        remove_newly_created_source_by_id(new_stub_source_id)
        remove_newly_created_entry_by_id(newly_created_entry_id)

    def test_add_new_entry_has_correct_fiability(self):
        """
        Test if adding a new entry
        and getting its fiability returns the correct fiability.
        """
        (new_stub_entry_specs, new_stub_source_id) = self._get_new_entry_specs()
        expected_new_stub_fiability = new_stub_entry_specs.fiability
        newly_created_entry_id = er.add(new_stub_entry_specs)
        actual_created_entry = _get_newly_created_entry(newly_created_entry_id)
        assert actual_created_entry.fiability == expected_new_stub_fiability
        remove_newly_created_source_by_id(new_stub_source_id)
        remove_newly_created_entry_by_id(newly_created_entry_id)

    def test_add_new_entry_has_correct_source_id(self):
        """
        Test if adding a new entry
        and getting its source ID returns the correct source ID.
        """
        (new_stub_entry_specs, new_stub_source_id) = self._get_new_entry_specs()
        expected_new_stub_source_id = new_stub_entry_specs.source_id
        newly_created_entry_id = er.add(new_stub_entry_specs)
        actual_created_entry = _get_newly_created_entry(newly_created_entry_id)
        assert actual_created_entry.source_id == expected_new_stub_source_id
        remove_newly_created_source_by_id(new_stub_source_id)
        remove_newly_created_entry_by_id(newly_created_entry_id)

    def test_add_new_entry_has_correct_title(self):
        """
        Test if adding a new entry
        and getting its title returns the correct title.
        """
        (new_stub_entry_specs, new_stub_source_id) = self._get_new_entry_specs()
        expected_new_stub_title = new_stub_entry_specs.title
        newly_created_entry_id = er.add(new_stub_entry_specs)
        actual_created_entry = _get_newly_created_entry(newly_created_entry_id)
        assert actual_created_entry.title == expected_new_stub_title
        remove_newly_created_source_by_id(new_stub_source_id)
        remove_newly_created_entry_by_id(newly_created_entry_id)

    def test_add_new_entry_has_correct_search_count(self):
        """
        Test if adding a new entry
        and getting its search count returns the correct search count.
        """
        (new_stub_entry_specs, new_stub_source_id) = self._get_new_entry_specs()
        expected_new_stub_search_count = new_stub_entry_specs.search_count
        newly_created_entry_id = er.add(new_stub_entry_specs)
        actual_created_entry = _get_newly_created_entry(newly_created_entry_id)
        assert actual_created_entry.search_count == expected_new_stub_search_count
        remove_newly_created_source_by_id(new_stub_source_id)
        remove_newly_created_entry_by_id(newly_created_entry_id)

    def test_update_existing_entry_search_count_has_correct_search_count(self):
        """
        Test if getting an existing entry by its index
        returns the correct entry search count.
        """
        new_stub_source_id = super().add_new_stub_source().id
        new_stub_entry = super().add_new_stub_entry(new_stub_source_id)
        expected_updated_entry_search_count = new_stub_entry.search_count + 1
        er.update_search_count_by_id(new_stub_entry.id)
        actual_updated_entry = _get_newly_created_entry(new_stub_entry.id)
        assert actual_updated_entry.search_count == expected_updated_entry_search_count
        remove_newly_created_source_by_id(new_stub_source_id)
        remove_newly_created_entry_by_id(new_stub_entry.id)

    def test_get_top_four_entries_by_search_count_returns_top_four(self):
        """
        Test if getting the top 4 entries with the max search count
        returns a list with the titles and the topics of the 4 max searched entries.
        """
        stub_source_id = super().add_new_stub_source().id
        stub_entries_specs = super()._get_five_stub_entries_specs_by_decreasing_search_count(stub_source_id)
        stub_entries_id_list = _insert_stub_entry_range_in_database(stub_entries_specs)
        stub_trends_specs = super()._get_five_stub_trends_specs_from_five_stub_entries(stub_entries_id_list)
        stub_trends_id_list = _insert_stub_trend_range_in_database(stub_trends_specs)
        expected_top_four_result = _get_expected_top_four_result(stub_entries_specs, stub_trends_specs)
        actual_top_four_result = er.get_top_four_by_search_count()
        assert expected_top_four_result == actual_top_four_result
        stub_id_list_zip = zip(stub_entries_id_list, stub_trends_id_list)
        for stub_entry_id, stub_trend_id in stub_id_list_zip:
            remove_newly_created_trend_by_id(stub_trend_id)
            remove_newly_created_entry_by_id(stub_entry_id)
        remove_newly_created_source_by_id(stub_source_id)

    def test_get_three_latest_fake_news_returns_last_three(self):
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
        actual_latest_three_result = er.get_past_three_fake_news()
        assert actual_latest_three_result == expected_latest_three_result
        for stub_entry_id in stub_entries_id_list:
            remove_newly_created_entry_by_id(stub_entry_id)
        remove_newly_created_source_by_id(stub_source_id)

    def _get_new_entry_specs(self) -> tuple[EntryData, int]:
        """
        Return a tuple containing the entry to create data and the associated source ID.
        :return: a tuple containing the entry to create data and the associated source ID
        """
        new_stub_source_id = super().add_new_stub_source().id
        new_stub_entry_specs = EntryData(
            fiability=get_new_stub_entry_fiability(),
            title=super().get_new_stub_entry_title(),
            source_id=new_stub_source_id,
            search_count=get_new_stub_entry_search_count()
        )
        return new_stub_entry_specs, new_stub_source_id