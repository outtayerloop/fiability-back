from repositories import entry_repository as er
from services import constants_service as ct
import gc


# Enable automatic garbage collection
gc.enable()


def get_trends() -> list[dict[str, str]]:
    """
    Return a list of data dictionary objects, each containing an entry title and its associated topic.
    :return: a list of data dictionary objects, each containing an entry title and its associated topic
    """
    entry_tuples = er.get_top_four_by_search_count()
    return [_get_title_topic_dict(entry_tuple[0], entry_tuple[1]) for entry_tuple in entry_tuples]


def _get_title_topic_dict(entry_title: str, trend_topic: str) -> dict[str, str]:
    """
    Return a data dictionary containing an entry title and its associated topic.
    :param entry_title: the entry title
    :param trend_topic: the entry associated trend topic
    :return: a data dictionary containing an entry title and its associated topic
    """
    return {
        ct.get_title_key(): entry_title,
        ct.get_topic_key(): trend_topic
    }


def get_past_three_fake_news():
    """
    Ask repository to retrieve past three fake news titles from database and return them.
    :return: past three fake news titles
    """
    return er.get_past_three_fake_news()


def get_suggestion_sources(theme):
    """
    Ask repository to retrieve suggestion sources related to a specific theme
    :return: suggestion sources
    @:param theme on which sources will be based
    """
    return er.get_suggestion_sources(theme)
