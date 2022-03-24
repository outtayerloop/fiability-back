import numpy as np
import pandas as pd
import nltk
from pandas import DataFrame
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import ShuffleSplit
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
import os
import warnings
import seaborn as sns
import re
import string

from sklearn.preprocessing import LabelEncoder
from termcolor import colored
from nltk import word_tokenize
import string
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.tokenize import WhitespaceTokenizer
from nltk.stem import WordNetLemmatizer
import nltk

nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('punkt')

from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score

warnings.filterwarnings('ignore')
from matplotlib.pyplot import *

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC

from sklearn.model_selection import train_test_split

from sklearn import preprocessing

from sklearn.metrics import classification_report, accuracy_score
from sklearn.metrics import confusion_matrix

from nltk.corpus import wordnet
from sklearn.feature_extraction.text import TfidfTransformer

seed = 12345
cv = ShuffleSplit(n_splits=5, test_size=0.2, random_state=seed)
encoder = preprocessing.LabelEncoder()


def get_wordnet_pos(pos_tag:str):
    """
    Return the position label associated with the provided word position tag.
    :param pos_tag: provided word position tag.
    :return:
    """
    if pos_tag.startswith('J'):
        return wordnet.ADJ
    elif pos_tag.startswith('V'):
        return wordnet.VERB
    elif pos_tag.startswith('N'):
        return wordnet.NOUN
    elif pos_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN


def preprocess(text: str) -> str:
    """
    Apply lower case, word filtering, tokenization, stop word removal and position tags to the provided text.
    """
    text = text.lower()  # lowercase the text
    text = [t for t in text.split(' ') if len(t) > 1]  # remove the words counting just one letter
    text = [word for word in text if not any(c.isdigit() for c in word)]  # remove the words that contain numbers
    text = [word.strip(string.punctuation) for word in text]  # tokenize the text and remove puncutation
    stop = stopwords.words('english')  # remove all stop words
    text = [x for x in text if x not in stop]
    text = [t for t in text if len(t) > 0]  # remove tokens that are empty
    pos_tags = pos_tag(text)  # pos tag the text
    text = [WordNetLemmatizer().lemmatize(t[0], get_wordnet_pos(t[1])) for t in pos_tags]
    return ' '.join(text)  # join all


def split_train_holdout_test(encoder: LabelEncoder, df: DataFrame, verbose: bool = True) -> tuple:
    """
    Apply label encoding to the text truthfulness label and train/test/holdout split the training DataFrame.
    Prints associated shapes if needed. Return the dataset split subsets.
    :param encoder: label encoder
    :param df: provided DataFrame
    :param verbose: determines whether to print shapes or not.
    :return: the label encoder and all the subsets from train, to test to holdout (X and y)
    """
    train = df[df['label'] != 'None']  # Re-split original train and test
    test = df[df['label'] == 'None']
    train['encoded_label'] = encoder.fit_transform(train.label.values)  # Encode Target
    # Take holdout from train
    train_cv, train_holdout, train_cv_label, train_holdout_label = train_test_split(train,
                                                                                    train.encoded_label,
                                                                                    test_size=0.33,
                                                                                    random_state=seed)
    if verbose:
        print('\nTrain dataset (Full)')
        print(train.shape)
        print('Train dataset cols')
        print(list(train.columns))
        print('\nTrain CV dataset (subset)')
        print(train_cv.shape)
        print('Train Holdout dataset (subset)')
        print(train_holdout.shape)
        print('\nTest dataset')
        print(test.shape)
        print('Test dataset cols')
        print(list(test.columns))
    return encoder, train, test, train_cv, train_holdout, train_cv_label, train_holdout_label


def run_model(encoder: LabelEncoder, train_vector, train_label, holdout_vector, holdout_label, type, name) -> list:
    """
    Given the current model type, apply cross-validation with grid search to find the best performing model from
    the tested hyper-parameters values.
    :param encoder: label encoder
    :param train_vector: document-term matrix used to train the current model
    :param train_label: truthfulness labels from train vector
    :param holdout_vector: document-term matrix used as holdout subset for the current model
    :param holdout_label: truthfulness labels from holdout vector
    :param type: current tested model type
    :param name: associated model hard-coded name
    :return: a list containing the hard-coded model name, the model params and its computed accuracy
    """
    global cv
    global seed
    if type == 'svc':
        classifier = SVC()
        grid = [
            {'C': [1, 10, 50, 100], 'kernel': ['linear']},
            {'C': [10, 100, 500, 1000], 'gamma': [0.0001], 'kernel': ['rbf']},
        ]
    if type == 'nb':
        classifier = MultinomialNB()
        grid = {}
    if type == 'maxEnt':
        classifier = LogisticRegression()
        grid = {'penalty': ['l1', 'l2'], 'C': [0.001, 0.01, 0.1, 1, 10, 100, 1000]}
    print(colored(name, 'red'))  # Model
    model = GridSearchCV(estimator=classifier, cv=cv, param_grid=grid)
    print(colored(model.fit(train_vector, train_label), 'yellow'))
    print(colored('\nCV-scores', 'blue'))  # Score
    means = model.cv_results_['mean_test_score']
    stds = model.cv_results_['std_test_score']
    for mean, std, params in sorted(zip(means, stds, model.cv_results_['params']), key=lambda x: -x[0]):
        print('Accuracy: %0.3f (+/-%0.03f) for params: %r' % (mean, std * 2, params))
    print()
    print(colored('\nBest Estimator Params', 'blue'))
    print(colored(model.best_estimator_, 'yellow'))
    print(colored('\nPredictions:', 'blue'))  # Predictions
    model_train_pred = encoder.inverse_transform(model.predict(holdout_vector))
    print(model_train_pred)
    cm = confusion_matrix(holdout_label, model_train_pred)  # Confusion Matrix
    cm_df = pd.DataFrame(cm,
                         index=['FAKE', 'REAL'],
                         columns=['FAKE', 'REAL'])  # Transform to df for easier plotting
    plt.figure(figsize=(5.5, 4))
    sns.heatmap(cm_df, annot=True, fmt='g')
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.show()
    acc = accuracy_score(holdout_label, model_train_pred)  # Accuracy
    print(colored('\nAccuracy:', 'blue'))
    print(colored(acc, 'green'))
    return [name, model, acc]


def pos_tag_words(text: str) -> str:
    """
    Apply position tags to each word of the user entry text.
    :return: the text with each word having a position tag
    """
    pos_text = nltk.pos_tag(nltk.word_tokenize(text))
    return ' '.join([pos + '-' + word for word, pos in pos_text])
