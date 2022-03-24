from entities.models.BaseModel import BaseModel
from entities.models.Source import Source
from peewee import CharField, BooleanField, ForeignKeyField, IntegerField
import gc


# Enable automatic garbage collection
gc.enable()


# The model specifies its fields (or columns) declaratively, like Django.
# See : https://github.com/coleifer/peewee/blob/master/examples/twitter/app.py
class Entry(BaseModel):
    """
    Entries database table.
    """
    fiability = BooleanField()
    source = ForeignKeyField(Source, column_name='source_id')
    title = CharField(max_length=255)
    search_count = IntegerField()

    class Meta:
        table_name = 'entries'

        # Remember to add a trailing comma if your tuple of indexes contains only one item
        # https://docs.peewee-orm.com/en/latest/peewee/models.html
        indexes = (
            (('source_id', 'title'), True),  # Note the trailing comma!
        )