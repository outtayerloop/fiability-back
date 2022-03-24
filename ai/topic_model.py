import timeit
import pandas as pd
import nltk
import numpy as np
import re
import pickle
import string
from itertools import chain
from langdetect import detect
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from gensim.models import Phrases
from gensim import corpora
from gensim import models
from services import constants_service as ct

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')
nltk.download('wordnet')

import gc


# Enable automatic garbage collection
gc.enable()

start = timeit.default_timer()
with open('ai/pickle/dictionary_LDA.pkl' , 'rb') as f:
    """
    Load the pickle-format serialized dictionary_LDA.
    """
    dictionary_LDA = pickle.load(f)

with open('ai/pickle/model_topic.pkl' , 'rb') as f:
    """
    Load the pickle-format serialized lda_model (topic).
    """
    lda_model = pickle.load(f)
    stop = timeit.default_timer()
    print('=> Pickle Loaded in: ', stop - start)


class TopicModel:

    def __init__(self):
        """
        Initialize a new TopicModel instance.
        :param text: user text entry
        """
        self.text = None
        self.output = None
        self.num_topics = 8
        self.num_words = 4

    def predict(self) -> str:
        """
        Return REAL if the user text entry was labeled as truthful, else return FAKE.
        :return: REAL if the user text entry was labeled as truthful, else return FAKE.
        """
        tokens = word_tokenize(self.text)
        topics = lda_model.show_topics(formatted=True, num_topics=self.num_topics, num_words=self.num_words)
        res = pd.DataFrame([(el[0], round(el[1],2), topics[el[0]][1]) for el in lda_model[dictionary_LDA.doc2bow(tokens)]], columns=['topic #', 'weight', 'words in topic'])
        self.output = self.postprocessing_resultat(res)
        return self.output

    def postprocessing_resultat(self, res):
        """
        Return the clean list of topics.
        :return: List of topics.
        """
        res = res.sort_values(by=['weight'],ascending=False)
        res_first = res.head(1)
        #if(res_first['weight'].iloc[0]) > 0.4:
        topic = res_first['words in topic'].iloc[0]

        character_banned = "'*.\""
        for char in character_banned:
            topic = topic.strip().replace(char, "")
        res = topic.split("+")
        pattern = '[0-9]'
        list_word = [re.sub(pattern, '', i).strip().capitalize() for i in res]
        return list_word[0:1]

    def set_text(self, text: str):
        """
        Set the model's text material.
        :param text: provided text to analyze
        """
        self.text = text
