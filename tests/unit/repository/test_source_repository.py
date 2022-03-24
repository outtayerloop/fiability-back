from tests.BaseRepositoryTest import BaseRepositoryTest, remove_newly_created_source_by_id
from repositories import source_repository as sr
from entities.data.SourceData import SourceData
from typing import Optional
from entities.models.Source import Source
import gc
from entities.models.BaseModel import connect_to_db, close_db


# Enable automatic garbage collection
gc.enable()


def _get_newly_created_source(source_id: int) -> Optional[SourceData]:
    """
    Return the found SourceData instance from the provided created source ID, otherwise return None if
    no source with the provided ID already exists in the database.
    :param source_id: the provided created source ID.
    :return: the found SourceData instance or None.
    """
    connect_to_db()
    created_source = Source.get_or_none(Source.id == source_id)
    close_db()
    if created_source is None:
        return None
    return SourceData(created_source.id, created_source.name)


class TestSourceRepository(BaseRepositoryTest):

    def test_get_nonexistent_source_by_name_returns_none(self):
        """
        Test if getting a non-existing source by its name
        returns None.
        """
        invalid_source_name = 'test_get_nonexistent_source_by_name_returns_none'
        actual_found_source = sr.get_by_name(invalid_source_name)
        assert actual_found_source is None

    def test_get_existing_source_by_name_returns_source(self):
        """
        Test if getting an existing source by its name
        effectively returns a data row from the trends database table.
        """
        new_stub_source = super().add_new_stub_source()
        actual_found_source = sr.get_by_name(new_stub_source.name)
        assert actual_found_source is not None
        remove_newly_created_source_by_id(new_stub_source.id)

    def test_get_existing_source_by_name_has_correct_name(self):
        """
        Test if getting an existing source by its name
        returns the correct source name.
        """
        new_stub_source = super().add_new_stub_source()
        expected_new_stub_source_name = new_stub_source.name
        actual_found_source = sr.get_by_name(new_stub_source.name)
        assert actual_found_source.name == expected_new_stub_source_name
        remove_newly_created_source_by_id(new_stub_source.id)

    def test_add_new_source_inserts_in_database(self):
        """
        Test if adding a new source
        effectively inserts a data row in the sources database table.
        """
        new_stub_source_name = super().get_new_stub_source_name()
        new_stub_source_specs = SourceData(name=new_stub_source_name)
        newly_created_source_id = sr.add(new_stub_source_specs)
        actual_created_source = _get_newly_created_source(newly_created_source_id)
        assert actual_created_source is not None
        remove_newly_created_source_by_id(newly_created_source_id)

    def test_add_new_source_has_correct_name(self):
        """
        Test if adding a new source
        and getting its name returns the correct name.
        """
        new_stub_source_name = super().get_new_stub_source_name()
        expected_created_source_name = new_stub_source_name
        new_stub_source_specs = SourceData(name=new_stub_source_name)
        newly_created_source_id = sr.add(new_stub_source_specs)
        actual_created_source = _get_newly_created_source(newly_created_source_id)
        assert actual_created_source.name == expected_created_source_name
        remove_newly_created_source_by_id(newly_created_source_id)