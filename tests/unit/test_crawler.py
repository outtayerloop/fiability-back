from services import crawler_service as cwl
from newspaper import Article
import gc


# Enable automatic garbage collection
gc.enable()


class TestCrawler:

    # Attribute specified declaratively because constructors are forbidden when working with pytest.
    valid_url = 'https://www.foxnews.com/politics/' \
                'sanders-cruz-resist-pressure-after-ny-losses-vow-to-fight-to-conventions'

    def test_get_article_from_valid_url_returns_filled_article(self):
        """
        Test if getting article from valid URL
        returns an Article which is not None.
        """
        actual_article = cwl.get_article_by_url(self.valid_url)
        assert actual_article is not None

    def test_get_article_from_valid_url_returns_article_instance(self):
        """
        Test if getting article from valid URL
        returns an object of type Article.
        """
        actual_article = cwl.get_article_by_url(self.valid_url)
        assert isinstance(actual_article, Article)

    def test_get_article_from_valid_url_has_title(self):
        """
        Test if getting article from valid URL
        returns an Article with a title.
        """
        actual_article = cwl.get_article_by_url(self.valid_url)
        assert actual_article.title is not None
        assert actual_article.title.strip() != ''

    def test_get_article_from_valid_url_has_text(self):
        """
        Test if getting article from valid URL
        returns an Article with a text.
        """
        actual_article = cwl.get_article_by_url(self.valid_url)
        assert actual_article.text is not None
        assert actual_article.text.strip() != ''

    def test_get_article_from_empty_url_returns_none(self):
        """
        Test if getting article from an empty URL
        returns None.
        """
        invalid_url = ''
        actual_article = cwl.get_article_by_url(invalid_url)
        assert actual_article is None

    def test_get_article_from_rubbish_url_returns_none(self):
        """
        Test if getting article from a malformed URL
        returns None.
        """
        invalid_url = 'x'
        actual_article = cwl.get_article_by_url(invalid_url)
        assert actual_article is None