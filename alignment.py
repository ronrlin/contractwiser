#!/usr/bin/python
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus.reader.plaintext import PlaintextCorpusReader
from sklearn import svm

import os
from identification import AgreementClassifier

BASE_PATH = "./"
COUNT_VECT = 1
TFIDF_VECT = 2

"""
Alignment describes the process by which agreements of the same kind of are compared
to one another in a way that "aligns" the provisions within them.  Aligning agreements
is critical to being able to calculate relatively frequency of certain provisions.  

"""
class Alignment(object):

    CLAUSE_TYPE = {
        'interest_rate' : 'train/train_interest_rate',
        'principal_amount' : 'train/train_principal_amount',
        'notices' : 'train/train_notices_and_notifications',
        'registration_rights' : 'train/train_registration_rights',
    } 

    """
    Constructor

    Attributes:
    """
    def __init__(self, vectorizer=COUNT_VECT, stop_words=None):
        import time
        start_time = time.time()
        self.training_corpus = PlaintextCorpusReader(BASE_PATH, list(self.CLAUSE_TYPE.values()))
        end_time = time.time()
        print("Corpus is loading %s files" % str(len(self.training_corpus.fileids())))
        print("Time to load Plaintext corpus is %s seconds" % (end_time - start_time))

        if (vectorizer == COUNT_VECT): 
            self.vectorizer = CountVectorizer(input='content', stop_words=None, ngram_range=(1,1))
        elif (vectorizer == TFIDF_VECT):
            self.vectorizer = TfidfVectorizer(input='content', stop_words=None, ngram_range=(1,1))

        start_time = time.time()
        train_sents = list(' '.join(s) for s in self.training_corpus.sents())
        end_time = time.time()
        print("Time to load join on sentences of training texts is %s seconds" % (end_time - start_time))

        start_time = time.time()
        train_vec = self.vectorizer.fit_transform(train_sents)
        end_time = time.time()
        print("Time to fit/transform vector is %s seconds" % (end_time - start_time))

        start_time = time.time()
        target = list()
        for tfile in self.training_corpus.fileids():
            for tpara in self.training_corpus.sents(tfile):  
                target.append(tfile)
        end_time = time.time()
        print("Time to assemble a target vector is %s seconds" % (end_time - start_time))

        start_time = time.time()
        self.cll = svm.LinearSVC(class_weight='auto')
        self.cll.fit(train_vec, target)
        end_time = time.time()
        print("Time to build classifier and fit is %s seconds" % (end_time - start_time))

        print("Ready for provision alignment.")

    """
    Function aligns or classifies sentences passed to the function.

    Parameters
    ----------
    content : a list of strings

    """
    def align(self, content):
        test_vec = self.vectorizer.transform(content)
        results = self.cll.predict(test_vec)
        return results

    """
    Returns content with markup to identify provisions within agreement
    """
    def get_markup(self):
        return self._content


"""
Code is an example.
"""
def example():
    # This is my arbitrary list of stopwords that I noticed were in features.
    # TODO: consider using regex to eliminate numbers and certain words?
    my_stops = [ 'ii', 'iii', 'iv', 'vi', 'vii', 'viii', 'ix', 'xi', 'xii', 'xiii', 'january', 
        'february', 'march', 'april', 'may', 'june', 'july', 'august', 
        'september', 'october', 'november', 'december', '00', '000', '10', 
        '11', '12', '13', '14', '15', '16', '17', '18', '180', '19', '1933', 
        '1996', '20', '2001', '2002', '2003', '2004', '2009', '2006', '21', '25', 
        '250', '30', '31', '360', '365', '50', '500', '60', '90', '_________', 
        '_________________', '______________________', 'goodrich', 'american', 
        'whom', 'corporation', 'company' ]

    a = Alignment(stop_words=my_stops)
    testset = [
        "The interest rate is 11%% and growing in New York City",
        "The principal amount of the note is $10,000, purchased herein."
    ]
    result = a.align(testset)
    print(result)

    """ example of some simple chunking """ 
    for sent in testset: 
        for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
            if hasattr(chunk, 'label'):
                print(chunk.label(), ' '.join(c[0] for c in chunk.leaves()))

"""
Bypass main
"""
if __name__ == "__main__":
    pass