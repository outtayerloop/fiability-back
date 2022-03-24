from newspaper.article import Article

from services import request_service as req
from services import constants_service as ct
from routes import checker_route as chkr
import gc


# Enable automatic garbage collection
gc.enable()


class TestUrlValidity:

    valid_full_url = 'https://example.com'
    valid_article_title = 'valid_article_title'
    valid_article_text = 'valid_article_text'

    def test_basic_valid_https_dns_url_without_www_returns_true(self):
        """
        Test if a valid HTTPS DNS URL value without www prefix against the URL validator without query strings
        returns True.
        """
        expected_url_validity = True
        valid_url = 'https://example.com/'
        actual_url_validity = req._is_valid_url(valid_url)
        assert actual_url_validity == expected_url_validity

    def test_basic_valid_https_dns_url_with_www_returns_true(self):
        """
        Test if a valid HTTPS DNS URL value with www prefix against the URL validator without query strings
        returns True.
        """
        expected_url_validity = True
        valid_url = 'https://www.example.com/'
        actual_url_validity = req._is_valid_url(valid_url)
        assert actual_url_validity == expected_url_validity

    def test_basic_valid_http_dns_url_without_www_returns_true(self):
        """
        Test if a valid HTTP DNS URL value without www prefix against the URL validator without query strings
        returns True.
        """
        expected_url_validity = True
        valid_url = 'http://example.com/'
        actual_url_validity = req._is_valid_url(valid_url)
        assert actual_url_validity == expected_url_validity

    def test_basic_valid_http_dns_url_with_www_returns_true(self):
        """
        Test if a valid HTTP DNS URL value with www prefix against the URL validator without query strings
        returns True.
        """
        expected_url_validity = True
        valid_url = 'http://www.example.com/'
        actual_url_validity = req._is_valid_url(valid_url)
        assert actual_url_validity == expected_url_validity

    def test_basic_valid_https_ip_url_returns_true(self):
        """
        Test if a valid HTTPS IP URL value against the URL validator without query strings
        returns True.
        """
        expected_url_validity = True
        valid_url = 'https://1.1.1.1/'
        actual_url_validity = req._is_valid_url(valid_url)
        assert actual_url_validity == expected_url_validity

    def test_basic_valid_http_ip_url_returns_true(self):
        """
        Test if a valid HTTP IP URL value against the URL validator without query strings
        returns True.
        """
        expected_url_validity = True
        valid_url = 'http://1.1.1.1/'
        actual_url_validity = req._is_valid_url(valid_url)
        assert actual_url_validity == expected_url_validity

    def test_valid_url_with_query_strings_returns_true(self):
        """
        Test if a valid URL value without www prefix against the URL validator with query strings
        returns True.
        """
        expected_url_validity = True
        valid_url = 'https://example.com?q1=x1&q2=x2/'
        actual_url_validity = req._is_valid_url(valid_url)
        assert actual_url_validity == expected_url_validity

    def test_valid_url_with_query_strings_and_symbols_returns_true(self):
        """
        Test if a valid URL value without www prefix against the URL validator with query strings and symbols
        returns True.
        """
        expected_url_validity = True
        valid_url = 'https://example.com?q1=x1&q2=x2/#y'
        actual_url_validity = req._is_valid_url(valid_url)
        assert actual_url_validity == expected_url_validity

    def test_empty_url_returns_false(self):
        """
        Test if an empty URL value against the URL validator returns False.
        """
        expected_url_validity = False
        invalid_url = ''
        actual_url_validity = req._is_valid_url(invalid_url)
        assert actual_url_validity == expected_url_validity

    def test_invalid_url_protocol_returns_false(self):
        """
        Test if an URL with an application unsupported protocol value against the URL validator returns False.
        """
        expected_url_validity = False
        invalid_protocol_prefix = 'ftp'
        valid_subdomain_suffix = 'com'
        valid_domain_length = ct.get_max_input_length() - len(f'{invalid_protocol_prefix}://.{valid_subdomain_suffix}')
        valid_domain = 'x' * valid_domain_length
        invalid_url = f'{invalid_protocol_prefix}://{valid_domain}.{valid_subdomain_suffix}'
        actual_url_validity = req._is_valid_url(invalid_url)
        assert actual_url_validity == expected_url_validity

    def test_missing_subdomain_suffix_dot_returns_false(self):
        """
        Test if an URL without a subdomain suffix dot against the URL validator returns False.
        """
        expected_url_validity = False
        valid_protocol_prefix = 'https'
        valid_subdomain_suffix = 'com'
        valid_domain_length = ct.get_max_input_length() - len(f'{valid_protocol_prefix}://{valid_subdomain_suffix}')
        valid_domain = 'x' * valid_domain_length
        invalid_url = f'{valid_protocol_prefix}://{valid_domain}{valid_subdomain_suffix}'
        actual_url_validity = req._is_valid_url(invalid_url)
        assert actual_url_validity == expected_url_validity

    def test_missing_protocol_label_returns_false(self):
        """
        Test if an URL without a protocol label against the URL validator returns False.
        """
        expected_url_validity = False
        valid_subdomain_suffix = 'com'
        valid_domain_length = ct.get_max_input_length() - len(f'://.{valid_subdomain_suffix}')
        valid_domain = 'x' * valid_domain_length
        invalid_url = f'://{valid_domain}.{valid_subdomain_suffix}'
        actual_url_validity = req._is_valid_url(invalid_url)
        assert actual_url_validity == expected_url_validity

    def test_missing_protocol_separator_returns_false(self):
        """
        Test if an URL without a protocol separator against the URL validator returns False.
        """
        expected_url_validity = False
        valid_protocol_prefix = 'https'
        valid_subdomain_suffix = 'com'
        valid_domain_length = ct.get_max_input_length() - len(f'{valid_protocol_prefix}.{valid_subdomain_suffix}')
        valid_domain = 'x' * valid_domain_length
        invalid_url = f'{valid_protocol_prefix}{valid_domain}.{valid_subdomain_suffix}'
        actual_url_validity = req._is_valid_url(invalid_url)
        assert actual_url_validity == expected_url_validity

    def test_rubbish_url_returns_false(self):
        """
        Test if a simple text without any URL structure against the URL validator returns False.
        """
        expected_url_validity = False
        invalid_url = 'x'
        actual_url_validity = req._is_valid_url(invalid_url)
        assert actual_url_validity == expected_url_validity

    def test_http_protocol_validity_returns_true(self):
        """
        Test if the HTTP protocol is effectively labeled as valid by the protocol checker.
        """
        expected_protocol_validity = True
        valid_protocol = 'HTTP'
        actual_protocol_validity = req._is_valid_url_protocol(valid_protocol)
        assert actual_protocol_validity == expected_protocol_validity

    def test_https_protocol_validity_returns_true(self):
        """
        Test if the HTTPS protocol is effectively labeled as valid by the protocol checker.
        """
        expected_protocol_validity = True
        valid_protocol = 'HTTPS'
        actual_protocol_validity = req._is_valid_url_protocol(valid_protocol)
        assert actual_protocol_validity == expected_protocol_validity

    def test_invalid_protocol_validity_returns_false(self):
        """
        Test if a protocol other than HTTP and HTTPS is effectively labeled as invalid by the protocol checker.
        """
        expected_protocol_validity = False
        valid_protocol = 'FTP'
        actual_protocol_validity = req._is_valid_url_protocol(valid_protocol)
        assert actual_protocol_validity == expected_protocol_validity

    def test_none_article_returns_false(self):
        """
        Test if a None Article object is labeled as invalid by the article text checker.
        """
        expected_article_validity = False
        invalid_article = None
        actual_article_validity = chkr._is_valid_article(invalid_article)
        assert actual_article_validity == expected_article_validity

    def test_none_article_text_returns_false(self):
        """
        Test if an Article object with a None text is labeled as invalid by the article text checker.
        """
        expected_article_validity = False
        invalid_article = Article(url=self.valid_full_url)  # Prevent ArticleException to be raised from invalid url.
        invalid_article.title = self.valid_article_title
        invalid_article_text = None
        invalid_article.text = invalid_article_text
        actual_article_validity = chkr._is_valid_article(invalid_article)
        assert actual_article_validity == expected_article_validity

    def test_whitespace_article_text_returns_false(self):
        """
        Test if an Article object with a full whitespace text is labeled as invalid by the article text checker.
        """
        expected_article_validity = False
        invalid_article = Article(url=self.valid_full_url)  # Prevent ArticleException to be raised from invalid url.
        invalid_article.title = self.valid_article_title
        invalid_article_text = ' '
        invalid_article.text = invalid_article_text
        actual_article_validity = chkr._is_valid_article(invalid_article)
        assert actual_article_validity == expected_article_validity

    def test_empty_article_text_returns_false(self):
        """
        Test if an Article object with an empty text is labeled as invalid by the article text checker.
        """
        expected_article_validity = False
        invalid_article = Article(url=self.valid_full_url)  # Prevent ArticleException to be raised from invalid url.
        invalid_article.title = self.valid_article_title
        invalid_article_text = ''
        invalid_article.text = invalid_article_text
        actual_article_validity = chkr._is_valid_article(invalid_article)
        assert actual_article_validity == expected_article_validity

    def test_none_article_title_returns_false(self):
        """
        Test if an Article object with a none title is labeled as invalid by the article text checker.
        """
        expected_article_validity = False
        invalid_article = Article(url=self.valid_full_url)  # Prevent ArticleException to be raised from invalid url.
        invalid_article_title = None
        invalid_article.title = invalid_article_title
        invalid_article.text = self.valid_article_text
        actual_article_validity = chkr._is_valid_article(invalid_article)
        assert actual_article_validity == expected_article_validity

    def test_whitespace_article_title_returns_false(self):
        """
        Test if an Article object with a full whitespace title is labeled as invalid by the article text checker.
        """
        expected_article_validity = False
        invalid_article = Article(url=self.valid_full_url)  # Prevent ArticleException to be raised from invalid url.
        invalid_article_title = ' '
        invalid_article.title = invalid_article_title
        invalid_article.text = self.valid_article_text
        actual_article_validity = chkr._is_valid_article(invalid_article)
        assert actual_article_validity == expected_article_validity

    def test_empty_article_title_returns_false(self):
        """
        Test if an Article object with an empty title is labeled as invalid by the article text checker.
        """
        expected_article_validity = False
        invalid_article = Article(url=self.valid_full_url)  # Prevent ArticleException to be raised from invalid url.
        invalid_article_title = ''
        invalid_article.title = invalid_article_title
        invalid_article.text = self.valid_article_text
        actual_article_validity = chkr._is_valid_article(invalid_article)
        assert actual_article_validity == expected_article_validity

    def test_valid_article_title_returns_true(self):
        """
        Test if a valid Article object is labeled as valid by the article text checker.
        """
        expected_article_validity = True
        valid_article = Article(url=self.valid_full_url)
        valid_article.title = self.valid_article_title
        valid_article.text = self.valid_article_text
        actual_article_validity = chkr._is_valid_article(valid_article)
        assert actual_article_validity == expected_article_validity