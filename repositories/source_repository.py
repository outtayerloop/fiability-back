from entities.data.SourceData import SourceData
from entities.models.Source import Source
from typing import Optional
from entities.models.BaseModel import connect_to_db, close_db
import gc


# Enable automatic garbage collection
gc.enable()


def get_by_name(source_name: str) -> Optional[Source]:
    """
    Return the found Source instance from the provided source name, otherwise return None if
    no source with the provided name already exists in the database.
    :param source_name: searched source name.
    :return: the found Source instance or None.
    """
    connect_to_db()
    found_source = Source.get_or_none(Source.name == source_name)
    close_db()
    return found_source


def add(new_source: SourceData) -> int:
    """
    Insert a new row in the sources database table without checking if the source name already exists or not and
    return the associated id.
    :param new_source: new source to add
    :return: the new source id
    """
    connect_to_db()
    new_source_id = Source.create(name=new_source.get_name()).id
    close_db()
    return new_source_id