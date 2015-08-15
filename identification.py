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
		fileids : list of filenames from which to build a training corpus.

		target : list of categories corresponding to the filenames from which 
			to build a training corpus.

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

	"""
	Parameters
	----------
		filename : relative path to a file with filename

		return a list containing a string corresponding to the predicted 
			category of filename.

	"""
	def classify_file(self, filename):
		fh = open(filename, 'r')
		x = fh.read()
		fh.close()
		dtm_test = self.vectorizer.transform([x])
		results = self.cll.predict(dtm_test)
		return results[0]

	"""
	A function that figures out who the party and counterparties are in an agreement.
	"""
	def id_party_counterparty(self):
		pass

	"""
	A function that determines the geospatial coordinates relevant to this agreement,
	usually a US state.  This is usually determined from the Governing Law and Jurisdiction
	provision.
	"""
	def determine_geography(self):
		pass

	"""
	"""
	def get_stats(self):
		stats = {
			'sentence_count' : 0,
		}
		return stats

"""
Function performs a binary search to identify agreements of type 
specified by search_type.  This classifier works by training on 
one type of agreement, and treats agreements of any other type as 
OTHER.  The classifier therefore works by asking if a given
agreement is of a certain type.  If not, it classifies it generally
as simply OTHER.

Parameters
----------
search_target : string representing a category of agreements
"""
def binary_search(search_target='CONVERTIBLE'):
	from helper import WiserDatabase
	wd = WiserDatabase()

	fileids = list()
	cats = list()

	print("searching for agreements of type " + search_target)
	categories = [search_target]
	for category in categories:
		results = wd.fetch_by_category(category)
		for r in results:
			if r is not None:
				fileids.append(r['filename'])
				cats.append(r['category'])

	categories = wd.get_category_names()
	categories.remove('CONVERTIBLE')
	for category in categories:
		results = wd.fetch_by_category(category)
		for r in results:
			if r is not None:
				fileids.append(r['filename'])
				cats.append("OTHER")

	classifier = AgreementClassifier(fileids=fileids, target=cats)
	return classifier
	# check how many CONVERTIBLE DEBT agreements there are	
	# go into the data/ directory
	# grab a huge list of files
	# run predict
	# check manually

"""
"""
def main():
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
	print("number of distinct categories: " + str(len(list(set(cats)))))

	a = AgreementClassifier(fileids=fileids, target=cats)
	print(a.classify_file("data/a28b2f92979d4ac8ae1e31e7d1a91e8c9145074105d1254ea24565cb40c0328e"))
	print(a.classify_file("data/8bdba28656fc9f92e5ff132f1c39bc85c28de36e8995cd8a958ceb5a184b05d6"))
	print(a.classify_file("data/b59ae6f6b7ff76061a1e08b5090ff40068b8e8e396051cb10e12cc231a6ff652"))
	print(a.classify_file("data/b5a16c05b974363c6d276fccd313d8aef10987dd72a52921253428418dd49910"))
	print(a.classify_file("data/b5a452e5928045014deb9214a0eb7e1d2e496ed8576f106b2951d97c0fce3bbf"))
	print(a.classify_file("data/b5a5bb2a6b48749ef5a9c93c5cb2531f1593678ced2b810a051d4ab9fe8d153d"))
	print(a.classify_file("data/b5ac330271e7e20d438c25b1e8b8b2cba36e6c350c7de639a19a754021ce3f50"))
	print(a.classify_file("data/b5b13612a96b77698928a110c97e10226d8e838703d8aa96acda049695c99674"))
	print(a.classify_file("data/b5b9b3eb269573177e4d29531bacc5ad6e91baf9445729b98b5ca0c5d0433494"))
	print(a.classify_file("data/b5d7d7016ecc47763f543d74ad35aafddb1d585ea8f07572ec1fd2b4338f8244"))
	print(a.classify_file("data/b5dc59b6a8603900470f3d6014e1d1e5d30e200384e71b52805e531b882f4bb2"))
	print(a.classify_file("data/b5dca2c0b34f914c3765dc74502722153b4bda0c26afc0ebe108881d548611db"))
	print(a.classify_file("data/b5dcfb751a7e709e579974611b099980189a0fe664113860dcd8d5925268a673"))
	print(a.classify_file("data/b5dd8d196780d4b77bf98fa5dc2e4792f28d9928203c9a9db74435c5ca89c09b"))
	print(a.classify_file("data/b5ef4c83d384a362f7241df06ddef241d7eda65c8defc8cce70902fed6bd0db3"))
	print(a.classify_file("data/b5f1ac36eb8316a3dde14b0a5413ea2b2f2a014e0ec16886300463a51f9577ae"))
	print(a.classify_file("data/b5fa49b32c6350d0f5091041f4f104d3a3ee33ff6a5bfa284b9a146cee01da7a"))
	print(a.classify_file("data/b6043efd4e362c34a1214da5bc04ec317307ff7bb808e75fb532c138872a4c09"))
	print(a.classify_file("data/b6082a878fcf6997973f69f07056e74be8645ae088f3f301942a6ed10adac719"))
	print(a.classify_file("data/b612c3b4bb97242c729a2f809957a8a365ce5eec929ebb7be4969e9434e2248c"))
	print(a.classify_file("data/b61aeea63460b2f195092cadc0e72a0e9626c218d18a05845b9d79ff6490ff95"))
	print(a.classify_file("data/b61f21621542f419bab26e894da15e484fe62e0c5c9af68cbc5938fef02cdd52"))
	print(a.classify_file("data/b623e765b94c3d500fea66ae95ba9735bbbefc43a7cec8ba30262e804181c7f0"))
	print(a.classify_file("data/b625c796e102aa344390b1f7e714c9dc6c63dc6f2194523c67f67e08232a7680"))
	print(a.classify_file("data/b627907e7750928f87ccd458f3a89c47551a441dd35f02cad8356b52de6fcac7"))
	print(a.classify_file("data/b632abce8604cfe548ae927562eb28bd2066fbd52d79eae836eda5a070816beb"))
	print(a.classify_file("data/b639b8643881695149d8e2a3224e5680cf8e811245a6b7b2d2c502de8191c40b"))
	print(a.classify_file("data/b64ad3fdebb752134599fdea5477e97608f0024a1b747d33b7616f61bf1bee87"))
	print(a.classify_file("data/b655f37d1d260cd1526629ec3aa58e619a39f0e3c4ee30a6cb79fcf52f72d20d"))
	print(a.classify_file("data/b657342c915ec7405af1bd3c47093081268fb5e1828f113a56a29f59388a9d2b"))

	print("end of program")
	print("--------------------------------------------")

"""
Uses a Binary classifier to compare CONVERTIBLE vs. any other agreements.
Looks in the data/ directory and determines if agreements are CONVERTIBLE
or OTHER.  

return the classifier?

returns a list of filenames that are CONVERTIBLE
"""
def convertible_sampler(limit=(0, 1000)):
	# binary classifier that looks for CONVERTIBLE docs
	classifier = binary_search('CONVERTIBLE')
	# look for test data set in the data/ directory
	data_path = os.path.join(BASE_PATH, "data/")
	filenames = os.listdir(data_path)
	ctype_filenames = []
	print("preparing to scan " + str(len(filenames)) + " files")

	filenames = filenames[limit[0]:limit[1]]

	for f in filenames:
		ftype = classifier.classify_file(os.path.join(data_path, f))
		if (ftype == 'CONVERTIBLE'):
			ctype_filenames.append(f)
	return ctype_filenames

"""
"""
if __name__ == "__main__":
    main()