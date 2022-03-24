from entities.data.TrendData import TrendData
from entities.models.Trend import Trend
from entities.models.BaseModel import connect_to_db, close_db
import gc


# Enable automatic garbage collection
gc.enable()


def add(new_trend: TrendData) -> int:
    """
    Insert a new row in the trend database table
    and return the newly created trend ID.
    :param new_trend: new trend to add
    :return: the newly created trend ID
    """
    trend_date = new_trend.get_trend_date()
    topic = new_trend.get_topic()
    entry_id = new_trend.get_entry_id()
    connect_to_db()
    new_trend_id = Trend.create(trend_date=trend_date, topic=topic, entry_id=entry_id).id
    close_db()
    return new_trend_id


def get_all_topics() -> list[str]:
    """
    Return all the existing topics (removing duplicates)
    :return: all the existing topics (removing duplicates)
    """
    connect_to_db()
    topic_only_trends = Trend.select(Trend.topic)\
        .distinct()\
        .execute()
    close_db()
    return [trend.topic for trend in topic_only_trends]