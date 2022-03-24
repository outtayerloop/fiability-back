import gc


# Enable automatic garbage collection
gc.enable()


class SourceData:

    def __init__(self, id: int = None, name: str = None):
        """
        Initialize a new instance of SourceData.
        :param id: source identifier number
        :param name: source name
        """
        self.id = id
        self.name = name

    def get_id(self) -> int:
        """
        Return the source identifier number.
        :return: the source identifier number.
        """
        return self.id

    def get_name(self) -> str:
        """
        Return the source name.
        :return: the source name.
        """
        return self.name