#!/usr/bin/python
import os
import numpy as np
from sklearn import svm
from nltk.corpus.reader.plaintext import PlaintextCorpusReader
from sklearn.feature_extraction.text import CountVectorizer

BASE_PATH = "./"
CORPUS_PATH = os.path.join(BASE_PATH, "small-data/")

def bootstrap_data(query):
	from pymongo import MongoClient
	client = MongoClient('localhost', 27017)
	db = client['wiser_db']
	collection = db['classified']
	result = collection.find_one({'filename' : query})
	if (result is not None):
		return result
	else:
		return None

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

	def __init__(self):
		from os import listdir
		fileids = listdir(CORPUS_PATH)
		fileids = fileids
		print(fileids)
		self.corpus = PlaintextCorpusReader(CORPUS_PATH, fileids)
		print('corpus loaded..')
		print(len(self.corpus.fileids()))
		self.vectorizer = CountVectorizer(input='content', stop_words=None, ngram_range=(1,2))

		train_vec = np.array([])
		target = list()

		textcomp = []
		for thisfile in self.corpus.fileids():
			text = self.corpus.words(thisfile)
			text = ' '.join(text)
			textcomp.append(text)
			result = bootstrap_data(thisfile)
			if (result is not None):
				target.append(result['category'])
			else:
				print(thisfile + " not found!")
				target.append('UNKNOWN')

		train_vec = self.vectorizer.fit_transform(textcomp)
		self.cll = svm.LinearSVC(class_weight='auto')
		self.cll.fit(train_vec, target)
		print("fitted and ready.")

	def classify_file(self, filename):
		print('File read: ' + filename)
		fh = open(filename, 'r')
		x = fh.read()
		fh.close()
		dtm_test = self.vectorizer.transform([x])
		results = self.cll.predict(dtm_test)
		return results

	def get_stats(self):
		stats = {
			'sentence_count' : 0,
		}
		return stats

print("welcome to a program to id legal agreements.")
a = AgreementClassifier()
r = a.classify_file("data/a28b2f92979d4ac8ae1e31e7d1a91e8c9145074105d1254ea24565cb40c0328e")
print(r)
r = a.classify_file("data/8bdba28656fc9f92e5ff132f1c39bc85c28de36e8995cd8a958ceb5a184b05d6")
print(r)

from os import listdir
fileids = listdir(CORPUS_PATH)
for fs in fileids:
	print(a.classify_file(CORPUS_PATH + fs))

print("end of program")

