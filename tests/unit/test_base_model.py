import os
from services import constants_service as ct
import gc


# Enable automatic garbage collection
gc.enable()


class TestBaseModel:

    def test_existing_db_name_env_variable_returns_value(self):
        """
        Test if the database name environment variable is not None.
        """
        db_name_env_variable_label = ct.get_db_name_env_variable_label()
        db_name = os.getenv(db_name_env_variable_label)
        assert db_name is not None

    def test_existing_db_user_env_variable_returns_value(self):
        """
        Test if the database username environment variable is not None.
        """
        db_user_env_variable_label = ct.get_db_user_env_variable_label()
        db_user = os.getenv(db_user_env_variable_label)
        assert db_user is not None

    def test_existing_db_password_env_variable_returns_value(self):
        """
        Test if the database password environment variable is not None.
        """
        db_password_env_variable_label = ct.get_db_password_env_variable_label()
        db_password = os.getenv(db_password_env_variable_label)
        assert db_password is not None

    def test_existing_db_host_env_variable_returns_value(self):
        """
        Test if the database password environment variable is not None.
        """
        db_host_env_variable_label = ct.get_db_host_env_variable_label()
        db_host = os.getenv(db_host_env_variable_label)
        assert db_host is not None

    def test_existing_db_port_env_variable_returns_value(self):
        """
        Test if the database password environment variable is not None.
        """
        db_port_env_variable_label = ct.get_db_port_env_variable_label()
        db_port = os.getenv(db_port_env_variable_label)
        assert db_port is not None