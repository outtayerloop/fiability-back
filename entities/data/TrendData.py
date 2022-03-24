from datetime import date
import gc


# Enable automatic garbage collection
gc.enable()


class TrendData:

    def __init__(self, id: int = None, trend_date: date = None, topic: str = None, entry_id: int = None):
        """
        Initialize a new instance of TrendData.
        :param id: trend identifier number
        :param trend_date: trend date (date of extraction from a given user entry)
        """
        self.id = id
        self.trend_date = trend_date
        self.topic = topic
        self.entry_id = entry_id

    def get_id(self) -> int:
        """
        Return the trend identifier number.
        :return: the trend identifier number.
        """
        return self.id

    def get_trend_date(self) -> date:
        """
        Return the trend date of extraction.
        :return: the trend date of extraction.
        """
        return self.trend_date

    def get_topic(self) -> str:
        """
        Return the trend extracted topic.
        :return: the trend extracted topic.
        """
        return self.topic

    def get_entry_id(self) -> int:
        """
        Return the trend entry id.
        :return: the trend entry id.
        """
        return self.entry_id