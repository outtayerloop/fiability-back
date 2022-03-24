from flask import Blueprint, Response, request
from services import entries_service as ent
from services import response_service as res
import gc


# Enable automatic garbage collection
gc.enable()

# Create the entries route
app_entries = Blueprint('entries', __name__)


@app_entries.route('/trends', methods=['GET'])
def get_trends() -> Response:
    """
    Return a 200 OK Flask Response containing a JSON array of objects,
    each containing an entry title and its associated topic (can be empty).
    :return: a JSON array of objects,
    each containing an entry title and its associated topic (can be empty)
    """
    top_four_titles = ent.get_trends()
    return res.get_200_response(top_four_titles)


@app_entries.route('/news/fake/latest', methods=['GET'])
def get_past_three_fake_news() -> Response:
    """
    Return past three fake news titles.
    """
    past_three_fake_news = ent.get_past_three_fake_news()
    return res.get_200_response(past_three_fake_news)


@app_entries.route('/news/real/suggestion', methods=['GET'])
def get_suggestion_sources() -> Response:
    """
    Return suggestion sources regarding theme provided
    """
    theme = request.args.get("theme")
    suggestion_sources = ent.get_suggestion_sources(theme)
    return res.get_200_response(suggestion_sources)
