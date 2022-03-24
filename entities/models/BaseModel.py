import os
from peewee import MySQLDatabase, Model
from services import constants_service as ct
from dotenv import load_dotenv
import gc


# Enable automatic garbage collection
gc.enable()


# Take environment variables from .env file (must be ignored by version control for security purposes).
load_dotenv()

# Database name environment variable
db_name = os.getenv(ct.get_db_name_env_variable_label())

# Database user name environment variable
db_user = os.getenv(ct.get_db_user_env_variable_label())

# Database password environment variable
db_password = os.getenv(ct.get_db_password_env_variable_label())

# Database host environment variable
db_host = os.getenv(ct.get_db_host_env_variable_label())

# Database port environment variable
db_port = int(os.getenv(ct.get_db_port_env_variable_label()))


# Model definitions -- the standard "pattern" is to define a base model class
# that specifies which database to use.  then, any subclasses will automatically
# use the correct storage. for more information, see:
# https://charlesleifer.com/docs/peewee/peewee/models.html#model-api-smells-like-django
class BaseModel(Model):

    class Meta:
        database = MySQLDatabase(db_name, user=db_user, password=db_password, host=db_host, port=db_port)

    db = Meta.database


db_connection = BaseModel.db


def connect_to_db():
    """
    Open new connection to the database if it was not already connected.
    """
    if db_connection.close() is False:  # Return False if already closed.
        db_connection.connect(reuse_if_open=True)


def close_db():
    """
    Close existing connection to the database (is supposed to never crash).
    """
    db_connection.close()