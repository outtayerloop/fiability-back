import gc


# Enable automatic garbage collection
gc.enable()


def get_checker_endpoint_url_prefix() -> str:
    """
    Return the checker endpoint url prefix
    :return: the checker endpoint url prefix
    """
    return 'checker'


def get_past_three_fake_news_prefix() -> str:
    """
    Return the checker endpoint url prefix
    :return: the checker endpoint url prefix
    """
    return 'past_three_fake_news'


def get_entries_endpoint_url_prefix() -> str:
    """
    Return the entries endpoint url prefix
    :return: the entries endpoint url prefix
    """
    return 'entries'


def get_topics_endpoint_url_prefix() -> str:
    """
    Return the topics endpoint url prefix
    :return: the topics endpoint url prefix
    """
    return 'topics'


def get_truthfulness_label() -> str:
    """
    Return the label corresponding to some news checked as real.
    :return: a string containing the word "REAL"
    """
    return 'REAL'


def get_wrongness_label() -> str:
    """
    Return the label corresponding to some news checked as fake.
    :return: a string containing the word "FAKE"
    """
    return 'FAKE'


def get_checker_endpoint_key() -> str:
    """
    Return the accepted input key of the checker endpoint
    :return: the accepted input key of the checker endpoint
    """
    return 'url'


def get_application_content_type() -> str:
    """
    Return the application accepted content type
    :return: the application accepted content type
    """
    return 'application/json'


def get_none_json_request_body_message() -> str:
    """
    Return the message associated with a missing content type headers 400 Bad Request response
    or None request body JSON.
    :return: the above described message
    """
    return f'Content-type {get_application_content_type()} manquant ou body de requête null/vide'


def get_missing_input_key_message() -> str:
    """
    Return the message associated with a missing input key 400 Bad Request response
    :return: the above described message
    """
    input_key = get_checker_endpoint_key()
    return f'Clé de body JSON "{input_key}" de la requête POST introuvable'


def get_none_input_key_message() -> str:
    """
    Return the message associated with a None input key 400 Bad Request response
    :return: the above described message
    """
    input_key = get_checker_endpoint_key()
    return f'Clé de body JSON "{input_key}" de la requête POST null'


def get_bad_url_parsing_message() -> str:
    """
    Return the message associated with a bad input URL parsing 400 Bad Request response
    :return: the above described message
    """
    return 'L\'URL fournie n\'a pas pu être analysée'


def get_too_big_input_length_message() -> str:
    """
    Return the message associated with a too big input length 400 Bad Request response
    :return: the above described message
    """
    max_input_length = str(get_max_input_length())
    return f'URL trop longue (max {max_input_length} caractères)'


def get_response_message_key() -> str:
    """
    Return the response message key associated with any Flask Response.
    :return: the response message key
    """
    return 'message'


def get_response_content_key() -> str:
    """
    Return the response content key associated with any Flask Response.
    :return: the response message key
    """
    return 'content'


def get_ok_response_message() -> str:
    """
    Return the value of the message associated with a 200 OK Flask Response.
    :return: the value of the message
    """
    return 'ok'


def get_title_key() -> str:
    """
    Return the title key used in a data dictionary.
    :return: the title key used in a data dictionary
    """
    return 'title'


def get_topic_key() -> str:
    """
    Return the topic key used in a data dictionary.
    :return: the topic key used in a data dictionary
    """
    return 'topic'


def get_max_input_length() -> int:
    """
    Return the max accepted length for URLs to be checked by the endpoint.
    :return: an int containing the value 255
    """
    return 255


def get_bad_provided_validity_exception_message() -> str:
    """
    Return the exception message returned when a bad validity was provided.
    :return: the exception message returned when a bad validity was provided
    """
    return 'An incorrect validity value was provided.'


def get_db_name_env_variable_label() -> str:
    """
    Return the label of the database name environment variable used by the base model.
    :return: the label of the database name environment variable used by the base model
    """
    return 'FIABILITY_DB_NAME'


def get_db_user_env_variable_label() -> str:
    """
    Return the label of the database username environment variable used by the base model.
    :return: the label of the database username environment variable used by the base model
    """
    return 'FIABILITY_DB_USER'


def get_db_password_env_variable_label() -> str:
    """
    Return the label of the database password environment variable used by the base model.
    :return: the label of the database password environment variable used by the base model
    """
    return 'FIABILITY_DB_PASSWORD'


def get_db_host_env_variable_label() -> str:
    """
    Return the label of the database host environment variable used by the base model.
    :return: the label of the database host environment variable used by the base model
    """
    return 'FIABILITY_DB_HOST'


def get_db_port_env_variable_label() -> str:
    """
    Return the label of the database port environment variable used by the base model.
    :return: the label of the database port environment variable used by the base model
    """
    return 'FIABILITY_DB_PORT'


def get_application_host_label() -> str:
    """
    Return the label of the host used to address requests (used by integration tests).
    :return: the label of the host used to address requests (used by integration tests)
    """
    return 'FIABILITY_HOST'


def get_truthfulness_percentage_threshold() -> float:
    """
    Return the percentage threshold from which a text can be labeled as truthful.
    :return: the threshold percentage (here a text will be considered truthful if it's at least 70% truthful)
    """
    return 0.7