import timeit
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.corpus import wordnet
import pickle
import string
from services import constants_service as ct
import nltk
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('punkt')
import gc


# Enable automatic garbage collection
gc.enable()

start = timeit.default_timer()

with open('ai/pickle/pipeline.pkl', 'rb') as f:
    """
    Load the pickle-format serialized model.
    """
    pipeline = pickle.load(f)
    stop = timeit.default_timer()
    print('=> Pickle Loaded in: ', stop - start)


class PredictionModel:

    def __init__(self):
        """
        Initialize a new PredictionModel instance.
        :param text: user text entry
        """
        self.text = None
        self.output = None

    def predict(self) -> str:
        """
        Return REAL if the user text entry was labeled as truthful, else return FAKE.
        :return: REAL if the user text entry was labeled as truthful, else return FAKE.
        """
        self.output = {'original': self.text}
        clean_and_pos_tagged_text = self.get_clean_and_pos_tagged_text()
        self.output['prediction'] = \
            ct.get_wrongness_label() if pipeline.predict([clean_and_pos_tagged_text])[0] == 0 \
                else ct.get_truthfulness_label()
        return self.output['prediction']

    def get_clean_and_pos_tagged_text(self) -> str:
        """
        Return the pre-processed user text entry with stop word removal, lemmatization and position tags.
        """
        self.preprocess()
        self.pos_tag_words()
        clean_and_pos_tagged_text = self.output['preprocessed'] + ' ' + self.output['pos_tagged'] # Merge text
        return clean_and_pos_tagged_text

    def preprocess(self):
        """
        Apply lower case, word filtering, tokenization, stop word removal and position tags to the user entry text.
        """
        text = str(self.output['original']).lower() # lowercase the text
        text = [t for t in text.split(' ') if len(t) > 1] # remove the words counting just one letter
        text = [word for word in text if not any(c.isdigit() for c in word)] # remove the words that contain numbers
        text = [word.strip(string.punctuation) for word in text] # tokenize the text and remove puncutation
        stop = stopwords.words('english') # remove all stop words
        text = [x for x in text if x not in stop]
        text = [t for t in text if len(t) > 0] # remove tokens that are empty
        pos_tags = pos_tag(text) # pos tag the text
        text = [WordNetLemmatizer().lemmatize(t[0], self.get_wordnet_pos(t[1])) for t in pos_tags]
        self.output['preprocessed'] = ' '.join(text) # join all

    def get_wordnet_pos(self, pos_tag:str) -> str:
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

    def pos_tag_words(self):
        """
        Apply position tags to each word of the user entry text.
        """
        pos_text = nltk.pos_tag(nltk.word_tokenize(self.output['preprocessed']))
        self.output['pos_tagged'] = ' '.join(
            [pos + '-' + word for word, pos in pos_text])

    def set_text(self, text: str):
        """
        Set the model's text material from which to extract truthfulness label.
        :param text: provided text to analyze
        """
        self.text = text