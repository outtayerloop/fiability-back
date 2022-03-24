from entities.models.BaseModel import BaseModel
from peewee import CharField
import gc


# Enable automatic garbage collection
gc.enable()


# The model specifies its fields (or columns) declaratively, like Django.
# See : https://github.com/coleifer/peewee/blob/master/examples/twitter/app.py
class Source(BaseModel):
    """
    Sources database table.
    """
    name = CharField(unique=True, column_name='name', max_length=500)

    class Meta:
        table_name = 'sources'