from ai.prediction_model import PredictionModel
from ai.topic_model import TopicModel
from repositories import source_repository as sr
from repositories import trend_repository as tr
from repositories import entry_repository as er
from entities.data.SourceData import SourceData
from entities.data.TrendData import TrendData
from entities.data.EntryData import EntryData
from services import constants_service as ct

from urllib.parse import urlparse
from datetime import date
import gc


# Enable automatic garbage collection
gc.enable()


# Model used to get truthfulness label from a provided text.
# Declared here to avoid using too much RAM by reallocating memory each time it will be instantiated
# because here it is called multiple times successively in a loop.
model = PredictionModel()

model_topic = TopicModel()

def check(text: str) -> float:
    """
    Return the extracted truthfulness percentage from the provided text
    :param text: provided text to check
    :return: the percentage of sentences labeled as truthful (sentences are here detected by splitting by ".").
    """
    sentences = text.split('.')
    labels = [_get_truthfulness_label(sentence) for sentence in sentences]
    truthfulness_percentage = labels.count(ct.get_truthfulness_label()) / len(labels)
    return truthfulness_percentage.__round__(2)  # 2 decimals


def _get_truthfulness_label(text: str) -> str:
    """
    Return the extracted truthfulness from the provided text
    :param text: provided text to check
    :return: REAL if the extracted article was labeled as truthful, FAKE on the contrary or None if the URL could not
    be parsed.
    """
    model.set_text(text)
    return model.predict()

def check_topic(text: str):
    """
    Extracted topics from the provided text
    :param text: provided text to check to extract topics
    :return: the list of topics extracted
    """
    topic_list = _get_topic_label(text)
    return topic_list

def _get_topic_label(text: str):
    """
    Return the extracted list of topics from the provided text
    :param text: provided text to check
    :return: the list of topics extracted
    be parsed.
    """
    model_topic.set_text(text)
    return model_topic.predict()

def add_source_by_url(url: str) -> int:
    """
    Check whether the given source already exists or not. If it does not already exists, insert a new row in the
    sources database table and return the new or found source id.
    :param url: source url
    :return: the new or found source id
    """
    source_name = urlparse(url).netloc
    found_source = sr.get_by_name(source_name)
    if found_source is None:
        new_source = SourceData(name=source_name)
        return sr.add(new_source)
    return found_source.id


def add_entry(source_id: int, title: str, fiability: bool) -> int:
    """
    Add a new entry to the entries database table and return the found or new entry id.
    If the entry already existed, increment its search count by 1.
    :param source_id: entry source id
    :param title: entry title
    :param fiability: entry extracted truthfulness
    :return: the found or new entry id
    """
    found_entry = er.get_by_index(source_id, title)
    if found_entry is None:
        new_entry = EntryData(fiability=fiability, title=title, source_id=source_id)
        return er.add(new_entry)
    else:
        er.update_search_count_by_id(found_entry.id)
    return found_entry.id


def add_trend(topics, entry_id: int):
    """
    Extract a topic from the given text and create a new trend row in the database table.
    :param entry_id: associated entry ID
    :param text: provided text from which to extract a topic which will constitute a trend
    """
    # We temporarily simulate topic extraction here by providing the trend with some mock topic.
    # We expect each new trend to have only 1 associated topic label (no same trend with 2 different topics).
    for topic in topics:
        new_trend = TrendData(trend_date=date.today(), topic=topic, entry_id=entry_id)
        tr.add(new_trend)