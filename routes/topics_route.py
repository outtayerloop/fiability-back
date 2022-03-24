from flask import Blueprint, Response
from repositories import trend_repository as tr
from services import response_service as res
import gc


# Enable automatic garbage collection
gc.enable()

# Create the topics route
app_topics = Blueprint('topics', __name__)


@app_topics.route('', methods=['GET'])
def get_topics() -> Response:
    """
    Return a 200 OK Flask Response containing a JSON array of topic labels.
    :return: a JSON array of topic labels
    """
    existing_topics = tr.get_all_topics()
    return res.get_200_response(existing_topics)