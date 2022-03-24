from services import checker_service as chk

import pandas as pd
from sklearn.metrics import accuracy_score
import gc


# Enable automatic garbage collection
gc.enable()


class TestAccuracy:

    def test_min_80_percent_accuracy(self):
        """
        Test whether the model accuracy on the test dataset is superior or equal to 80 percent.
        """
        accuracy_threshold = 0.8
        df = pd.read_csv('./tests/unit/data/accuracy_test_data.csv')
        expected_labels = df['label']
        news = df['text']
        actual_labels = news.apply(lambda text: chk._get_truthfulness_label(text))
        accuracy = accuracy_score(expected_labels, actual_labels)
        assert accuracy >= accuracy_threshold