from typing import Optional
from entities.data.EntryData import EntryData
from entities.models.Entry import Entry
from entities.models.Trend import Trend
from entities.models.Source import Source
from entities.models.BaseModel import connect_to_db, close_db
import gc


# Enable automatic garbage collection
gc.enable()


def get_by_index(source_id: int, title: str) -> Optional[Entry]:
    """
    Return the found Entry instance from the provided source id and title, otherwise return None if
    no entry with the provided data already exists in the database.
    :param source_id: searched entry source identifier number.
    :param title: searched source title.
    :return: the found Entry instance or None.
    """
    connect_to_db()
    found_entry = Entry.get_or_none((Entry.source == source_id) & (Entry.title == title))
    close_db()
    return found_entry


def add(new_entry: EntryData) -> int:
    """
    Insert a new row in the entries database table without checking if the entry source id and title
    already exist or not and return the new entry id.
    :param new_entry: new entry to add
    :return: the new entry id
    """
    fiability = new_entry.get_fiability()
    source_id = new_entry.get_source_id()
    title = new_entry.get_title()
    search_count = 1  # The search count equals 1 the first time this entry is inserted in the database.
    connect_to_db()
    new_entry_id = Entry.create(fiability=fiability, source_id=source_id, title=title, search_count=search_count).id
    close_db()
    return new_entry_id


def update_search_count_by_id(entry_id: int):
    """
    Increment the corresponding entry's search count by 1.
    :param entry_id: target entry identifier number
    """
    connect_to_db()
    Entry.update({Entry.search_count: Entry.search_count + 1}) \
        .where(Entry.id == entry_id) \
        .execute()
    close_db()


def get_top_four_by_search_count() -> list[tuple[str, str]]:
    """
    Return a list of tuples, each containing the title and the associated topic
    of one of the four most searched news (e.g the top four entries with the biggest search count).
    :return: a list of tuples, each containing the title and the associated topic
    """
    limit = 4
    connect_to_db()
    top_four_search_counts_rows = Entry.select(Entry.search_count)\
        .order_by(-Entry.search_count)\
        .limit(limit)  # We order by descending search count to get only the 4 more searched entries
    top_four_search_counts = [row.search_count for row in top_four_search_counts_rows]
    rows = Entry.select(Entry.title, Entry.search_count, Trend.topic) \
        .join(Trend, on=(Entry.id == Trend.entry_id)) \
        .having(Entry.search_count << top_four_search_counts) \
        .order_by(-Entry.search_count)\
        .namedtuples() \
        .execute()  # We search for entries which search counts belong to the top 4 search counts list
    close_db()
    return [(row.title, row.topic) for row in rows]


def get_past_three_fake_news() -> list[str]:
    """
    Retrieve the past three fake news titles from the database.
    :return: the past three fake news titles
    """
    limit = 3
    connect_to_db()
    rows = Entry.select()\
        .where(Entry.fiability == 0) \
        .order_by(-Entry.id)\
        .limit(limit)  # We order by descending entry ID to get only the 3 latest entries
    close_db()
    return [row.title for row in rows]


def get_suggestion_sources(theme) -> list[dict[str, str]]:
    """
    Retrieve suggestion sources from the database.
    :return: suggestion sources list
    """
    limit = 3
    connect_to_db()
    query = Entry.select(Entry.title, Source.name) \
        .join(Trend, on=(Entry.id == Trend.entry_id)) \
        .join_from(Entry, Source, on=(Entry.source_id == Source.id)) \
        .distinct() \
        .where((Entry.fiability == 1) & (Trend.topic == theme)) \
        .limit(limit) \
        .namedtuples() \
        .execute()
    close_db()
    return [{'article': row.title, 'website': row.name} for row in query]
