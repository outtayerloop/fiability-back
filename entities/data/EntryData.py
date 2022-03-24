import gc


# Enable automatic garbage collection
gc.enable()


class EntryData:

    def __init__(self, id: int = None, fiability: bool = None, title: str = None,
                 source_id: int = None, search_count: int = None):
        """
        Initialize a new instance of TrendData.
        :param id: entry identifier number
        :param fiability: whether the entry has been labeled as truthful or not
        :param title: entry title
        :param source_id: entry source id
        :param search_count: entry search count (number of times it was searched by users)
        """
        self.id = id
        self.fiability = fiability
        self.title = title
        self.source_id = source_id
        self.search_count = search_count

    def get_id(self) -> int:
        """
        Return the entry identifier number.
        :return: the entry identifier number.
        """
        return self.id

    def get_fiability(self) -> bool:
        """
        Return the entry fiability.
        :return: the entry fiability
        """
        return self.fiability

    def get_title(self) -> str:
        """
        Return the entry title.
        :return: the entry title
        """
        return self.title

    def get_source_id(self) -> int:
        """
        Return the entry source id.
        :return: the entry source id
        """
        return self.source_id

    def get_search_count(self) -> int:
        """
        Return the entry search count (number of times it was searched by users).
        :return: the entry search count (number of times it was searched by users)
        """
        return self.search_count