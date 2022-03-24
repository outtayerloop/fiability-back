from entities.models.Entry import Entry
from entities.models.Source import Source
from entities.models.Trend import Trend
from entities.data.SourceData import SourceData
from entities.data.EntryData import EntryData
import gc
from entities.models.BaseModel import connect_to_db, close_db


# Enable automatic garbage collection
gc.enable()


def remove_newly_created_source_by_id(source_id: int):
    """
    Remove the previously test-purpose created stub source from the database by its ID.
    :param source_id: source to remove identifier
    """
    connect_to_db()
    Source.delete_by_id(source_id)
    close_db()


def remove_newly_created_entry_by_id(entry_id: int):
    """
    Remove the previously test-purpose created stub entry from the database by its ID.
    :param entry_id: entry to remove identifier
    """
    connect_to_db()
    Entry.delete_by_id(entry_id)
    close_db()


def remove_newly_created_trend_by_id(trend_id: int):
    """
    Remove the previously test-purpose created stub trend from the database by its ID.
    :param trend_id: trend to remove identifier
    """
    connect_to_db()
    Trend.delete_by_id(trend_id)
    close_db()


def get_new_stub_entry_fiability() -> bool:
    """
    Return the fiability used to create a new stub entry.
    :return: the fiability used to create a new stub entry
    """
    return True


def get_new_stub_entry_search_count() -> int:
    """
    Return the search count used to create a new stub entry.
    The search count equals 1 the first time this entry is inserted in the database.
    :return: the search count used to create a new stub entry
    """
    return 1


class BaseRepositoryTest:
    # Attribute specified declaratively because constructors are forbidden when working with pytest.
    stub_prefix = 'test_repository'

    def add_new_stub_entry(self, new_stub_source_id: int,
                           new_stub_entry_title=None,
                           new_stub_entry_search_count=None) -> EntryData:
        """
        Insert a new row in the entries database table
        and return the newly created entry.
        :param new_stub_source_id: the newly created source
        :param new_stub_entry_title: the newly created entry name
        :param new_stub_entry_search_count: the newly created entry search count
        :return: the newly created entry
        """
        connect_to_db()
        created_stub_entry = Entry.create(
            fiability=get_new_stub_entry_fiability(),
            source_id=new_stub_source_id,
            title=self.get_new_stub_entry_title() if new_stub_entry_title is None else new_stub_entry_title,
            search_count=get_new_stub_entry_search_count() if new_stub_entry_search_count is None else new_stub_entry_search_count
        )
        close_db()
        return EntryData(
            created_stub_entry.id,
            created_stub_entry.fiability,
            created_stub_entry.title,
            created_stub_entry.source.id,
            created_stub_entry.search_count
        )

    def add_new_stub_source(self, source_name: str = None) -> SourceData:
        """
        Insert a new row in the sources database table
        and return the newly created source.
        :param: the new source name
        :return: the newly created source
        """
        new_stub_source_name = self.get_new_stub_source_name() if source_name is None else source_name
        connect_to_db()
        created_stub_source = Source.create(name=new_stub_source_name)
        close_db()
        return SourceData(created_stub_source.id, created_stub_source.name)

    def get_stub_prefix(self) -> str:
        """
        Return the common prefix used to create stub entities.
        :return: the common prefix used to create stub entities
        """
        return self.stub_prefix

    def get_new_stub_source_name(self) -> str:
        """
        Return the name used to create a new stub source.
        :return: the name used to create a new stub source
        """
        return f'{self.stub_prefix}_source_name'

    def get_new_stub_entry_title(self) -> str:
        """
        Return the title used to create a new stub entry.
        :return: the title used to create a new stub entry
        """
        return f'{self.stub_prefix}_entry_title'