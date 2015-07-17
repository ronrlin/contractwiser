#!/usr/bin/python
import os
import numpy as np
from sklearn import svm
from nltk.corpus.reader.plaintext import PlaintextCorpusReader
from sklearn.feature_extraction.text import CountVectorizer

BASE_PATH = "./"
CORPUS_PATH = os.path.join(BASE_PATH, "small-data/")

class AgreementClassifier(object):
	"""
	Agreement Classifier

	Parameters
	----------
		fileids : list of filenames

		target : list of categories corresponding to the filenames

	"""
	def __init__(self, fileids=[], target=[]):
		self.corpus = PlaintextCorpusReader(CORPUS_PATH, fileids)
		print("corpus loaded files: " + str(len(self.corpus.fileids())))
		self.vectorizer = CountVectorizer(input='content', stop_words=None, ngram_range=(1,2))
		textcomp = []
		for thisfile in self.corpus.fileids():
			text = self.corpus.words(thisfile)
			text = ' '.join(text)
			textcomp.append(text)

		train_vec = self.vectorizer.fit_transform(textcomp)
		self.cll = svm.LinearSVC(class_weight='auto')
		self.cll.fit(train_vec, target)
		print("fitted and ready!")

	def classify_file(self, filename):
		print('file read: ' + filename)
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

print("--------------------------------------------")
print("welcome to a program to id legal agreements.")

from helper import WiserDatabase
wd = WiserDatabase()

fileids = list()
cats = list()
# capture the list of all agreement types
categories = wd.get_category_names()
for category in categories:
	results = wd.fetch_by_category(category)
	for r in results:
		if r is not None:
			fileids.append(r['filename'])
			cats.append(r['category'])
	
print("number of files: " + str(len(fileids)))
print("number of categories: " + str(len(cats)))

a = AgreementClassifier(fileids=fileids, target=cats)
print(a.classify_file("data/a28b2f92979d4ac8ae1e31e7d1a91e8c9145074105d1254ea24565cb40c0328e"))
print(a.classify_file("data/8bdba28656fc9f92e5ff132f1c39bc85c28de36e8995cd8a958ceb5a184b05d6"))

print("end of program")
print("--------------------------------------------")
