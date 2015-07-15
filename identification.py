#!/usr/bin/python
import os
import numpy as np
from sklearn import svm
from nltk.corpus.reader.plaintext import PlaintextCorpusReader

BASE_PATH = "./"
CORPUS_PATH = os.path.join(BASE_PATH, "small-data/")

class AgreementClassifier(object):
	"""Agreement Classifier

	Attributes:
		content: The unicode text of any legal agreement or contract.
		type: The human readable type of the legal agreement provided.
	"""
	UNKNOWN = 0
	CONVERTIBLE_AGREEMENT = 1
	CREDIT_AGREEMENT = 2

	TYPES = {
		UNKNOWN: 'unknown',
		CONVERTIBLE_AGREEMENT: 'convertible_debt',
		CREDIT_AGREEMENT: 'credit_agreement',
	}

	def __init__(self, content):
		from os import listdir
		fileids = listdir(CORPUS_PATH)
		print(fileids)
        self.corpus = PlaintextCorpusReader(BASE_PATH, fileids)
        print('corpus loaded..')
        print(len(self.corpus.fileids()))
        self.vectorizer = CountVectorizer(input='content', stop_words=stop_words, ngram_range=(1,1))

        train_vec = np.array()
        target = list()
        for thisfile in self.corpus.fileids():
        	train_vec.append(self.vectorizer.fit_transform(self.corpus.words(thisfile)))
        	# load a value in target that corresponds to the known category of thisfile agreement 

        self.cll = svm.LinearSVC(class_weight='auto')
        self.cll.fit(train_vec, target)
        print("fitted and ready.")

	
	def get_types(self):
		return(self.TYPES)

	def classify(self):
		return self.type

	def get_stats(self):
		stats = {
			'word_count' : len(self._content.split(' ')),
			'sentence_count' : 0,
		}
		return stats

print("welcome to a program to id legal agreements.")
a = AgreementClassifier("give a stream of text")
print(a.get_types())
print(a.get_stats())

print('Training files loaded...')


