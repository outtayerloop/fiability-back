from entities.models.BaseModel import BaseModel
from entities.models.Entry import Entry
from peewee import DateField, CharField, ForeignKeyField
import gc


# Enable automatic garbage collection
gc.enable()


# The model specifies its fields (or columns) declaratively, like Django.
# See : https://github.com/coleifer/peewee/blob/master/examples/twitter/app.py
class Trend(BaseModel):
    """
    Trends database table.
    """
    trend_date = DateField()
    topic = CharField(max_length=255)
    entry = ForeignKeyField(Entry, column_name='entry_id')

    class Meta:
        table_name = 'trends'