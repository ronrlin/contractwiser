#!/usr/bin/python
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus.reader.plaintext import PlaintextCorpusReader
from sklearn import svm

import os
from identification import AgreementClassifier

BASE_PATH = "./"

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
    def __init__(self, stop_words=None):
        self.training_corpus = PlaintextCorpusReader(BASE_PATH, list(self.CLAUSE_TYPE.values()))
        print('training files loaded...' + str(len(self.training_corpus.fileids())))
        print(self.training_corpus.fileids())
        self.vectorizer = CountVectorizer(input='content', stop_words=stop_words, ngram_range=(1,1))
        train_sents = list(' '.join(s) for s in self.training_corpus.sents())
        train_vec = self.vectorizer.fit_transform(train_sents)

        target = list()
        for tfile in self.training_corpus.fileids():
            for tpara in self.training_corpus.sents(tfile):  
                target.append(tfile)

        self.cll = svm.LinearSVC(class_weight='auto')
        self.cll.fit(train_vec, target)
        print("ready for alignment.")

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
Code below runs tests.
"""
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
    "The interest rate is 11%% and growing",
    "The principal amount of the note is $10,000, purchased herein."
]
a.align(testset)
