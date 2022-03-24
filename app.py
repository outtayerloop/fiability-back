from dotenv import load_dotenv
from flask import Flask, Response
from flask_cors import CORS

from services import constants_service as ct
from routes.checker_route import app_checker
from routes.entries_route import app_entries
from routes.topics_route import app_topics
import gc


# Enable automatic garbage collection
gc.enable()


# Take environment variables from .env file (must be ignored by version control for security purposes).
load_dotenv()

# Create the Flask app
app = Flask(__name__)

# Add CORS handling
cors = CORS(app)

# Log the server's activity
app.debug = True

# Register the routes
app.register_blueprint(app_checker, url_prefix=f'/{ct.get_checker_endpoint_url_prefix()}')
app.register_blueprint(app_entries, url_prefix=f'/{ct.get_entries_endpoint_url_prefix()}')
app.register_blueprint(app_topics, url_prefix=f'/{ct.get_topics_endpoint_url_prefix()}')


@app.after_request
def set_response_headers(response: Response) -> Response:
    """
    Handle the application's CORS policy
    :param response: response returned to a client
    :return: the response with access control headers
    """
    response.headers.remove('Access-Control-Allow-Origin')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST')
    return response