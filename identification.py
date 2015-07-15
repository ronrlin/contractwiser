#!/usr/bin/python
import os
import zipfile
import numpy as np

from pymongo import MongoClient
from sklearn import svm

from nltk.corpus.reader.plaintext import PlaintextCorpusReader

BASE_PATH = "/home/obironkenobi/Projects/ContractWiser/"
TRAIN_PATH = os.path.join(BASE_PATH, "train/")

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
		CONVERTIBLE_AGREEMENT: 'convertible debt',
		CREDIT_AGREEMENT: 'credit agreement',
	}

	def __init__(self, content):
		self._content = content
		self.type = "unknown"
		
		
	
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

a = AgreementClassifier("give a stream of text")
print(a.get_types())
print(a.get_stats())

print('Training files loaded...')
