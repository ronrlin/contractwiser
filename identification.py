#!/usr/bin/python
import os
import numpy as np
from sklearn import svm
from nltk.corpus.reader.plaintext import PlaintextCorpusReader
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

BASE_PATH = "./"
CORPUS_PATH = os.path.join(BASE_PATH, "small-data/")

COUNT_VECT = 1
TFIDF_VECT = 2

class AgreementClassifier(object):
	"""
	Agreement Classifier

	Parameters
	----------
		fileids : list of filenames from which to build a training corpus.

		target : list of categories corresponding to the filenames from which 
			to build a training corpus.
	"""
	def __init__(self, vectorizer=COUNT_VECT, fileids=[], target=[]):
		import time
		start_time = time.time()
		self.corpus = PlaintextCorpusReader(CORPUS_PATH, fileids)
		end_time = time.time()
		print("Corpus is loading %s files" % str(len(self.corpus.fileids())))
		print("Time to load Plaintext corpus is %s seconds" % (end_time - start_time))

		start_time = time.time()
		self.vector_type = vectorizer
		if (vectorizer == COUNT_VECT): 
			self.vectorizer = CountVectorizer(input='content', stop_words=None, ngram_range=(1,2))
		elif (vectorizer == TFIDF_VECT):
			self.vectorizer = TfidfVectorizer(input='content', stop_words=None, ngram_range=(1,2))

		end_time = time.time()
		print("Time to vectorize is %s seconds" % (end_time-start_time))

		start_time = time.time()
		textcomp2 = []
		for thisfile in self.corpus.fileids():
			text = self.corpus.raw(thisfile)
			text = ' '.join([text])
			textcomp2.append(text)
		end_time = time.time()
		textcomp=textcomp2
		print("Time to scroll through all raw fileids is %s seconds" % (end_time-start_time))

		start_time = time.time()
		train_vec = self.vectorizer.fit_transform(textcomp)
		end_time = time.time()
		print("Time to fit/transform matrix set is %s seconds" % (end_time-start_time))

		# Try to just do a transform
		start_time = time.time()
		train_vec2 = self.vectorizer.transform(textcomp)
		end_time = time.time()
		print("Time to transform matrix set is %s seconds" % (end_time-start_time))

		start_time = time.time()
		self.cll = svm.LinearSVC(class_weight='auto')
		self.cll.fit(train_vec, target)
		end_time = time.time()
		print("Time to fit model is %s seconds" % (end_time-start_time))

		print("Fitted and ready!")

	def classify_file(self, filename):
		"""
		Classify a given filename by its agreement type.

		:param filename: relative path to a file with filename

		return a list containing a string corresponding to the predicted 
			category of filename.

		"""
		fh = open(filename, 'r')
		x = fh.read()
		fh.close()
		dtm_test = self.vectorizer.transform([x])
		results = self.cll.predict(dtm_test)
		return results[0]

	def get_vectorizer_type():
		""" 
		Return human-readable vectorization method being used by the classifier. 

		Returns a string

		ie: CountVectorizer, TfidfVectorizer
		"""
		if (self.vector_type == COUNT_VECT):
			return "CountVectorizer"
		elif (self.vector_type == TFIDF_VECT):
			return "TfidfVectorizer"

	def id_party_counterparty(self):
		"""
		A function that figures out who the party and counterparties are in an agreement.
		"""
		pass

	def determine_geography(self):
		"""
		A function that determines the geospatial coordinates relevant to this agreement,
		usually a US state.  This is usually determined from the Governing Law and Jurisdiction
		provision.
		"""
		pass

	def get_stats(self):
		"""
		"""
		stats = {
			'sentence_count' : 0,
		}
		return stats

def binary_search(vectorizer=COUNT_VECT, search_target='CONVERTIBLE'):
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

	classifier = AgreementClassifier(vectorizer=vectorizer, fileids=fileids, target=cats)
	return classifier
	# check how many CONVERTIBLE DEBT agreements there are	
	# go into the data/ directory
	# grab a huge list of files
	# run predict
	# check manually

def main():
	"""	"""
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

	fileids = fileids[0:150]
	cats = cats[0:150]
	print("number of files: " + str(len(fileids)))
	print("number of categories: " + str(len(cats)))
	print("number of distinct categories: " + str(len(list(set(cats)))))

	a = AgreementClassifier(vectorizer=COUNT_VECT, fileids=fileids, target=cats)

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

def convertible_sampler(vectorizer=COUNT_VECT, limit=(0, 1000)):
	"""
	Uses a Binary classifier to compare CONVERTIBLE vs. any other agreements.
	Looks in the data/ directory and determines if agreements are CONVERTIBLE
	or OTHER.  

	return the classifier?

	returns a list of filenames that are CONVERTIBLE
	"""
	# binary classifier that looks for CONVERTIBLE docs
	classifier = binary_search(vectorizer=vectorizer, search_target='CONVERTIBLE')
	# look for test data set in the data/ directory
	data_path = os.path.join(BASE_PATH, "data/")
	filenames = os.listdir(data_path)
	ctype_filenames = []
	print("preparing to scan " + str(len(filenames)) + " files")
	filenames = filenames[limit[0]:limit[1]]
	print("trimmed down to " + str(len(filenames)) + " files")

	for f in filenames:
		ftype = classifier.classify_file(os.path.join(data_path, f))
		if (ftype == 'CONVERTIBLE'):
			ctype_filenames.append(f)
	return ctype_filenames

def testing():
	"""
	Test the loading times and vectorization times for CountVectorizer vs. TfidfVectorizer
	"""
	print("Measure the CountVectorizer")
	classifier = binary_search(vectorizer=COUNT_VECT, search_target='CONVERTIBLE')
	data_path = os.path.join(BASE_PATH, "data/")
	filenames = os.listdir(data_path)
	print("preparing to scan " + str(len(filenames)) + " files")
	filenames = filenames[0:1000]
	print("trimmed down to " + str(len(filenames)) + " files")

	print("\n\n")

	print("Measure the TfidfVectorizer")
	classifier = binary_search(vectorizer=TFIDF_VECT, search_target='CONVERTIBLE')
	data_path = os.path.join(BASE_PATH, "data/")
	filenames = os.listdir(data_path)
	print("preparing to scan " + str(len(filenames)) + " files")
	filenames = filenames[0:1000]
	print("trimmed down to " + str(len(filenames)) + " files")

"""

Measure the CountVectorizer
searching for agreements of type CONVERTIBLE
Corpus is loading 362 files
Time to load Plaintext corpus is 0.00012111663818359375 seconds
Time to vectorize is 2.0265579223632812e-05 seconds
Time to scroll through all raw fileids is 0.10050797462463379 seconds
Time to fit/transform matrix set is 41.66534876823425 seconds
Time to transform matrix set is 37.24678039550781 seconds
Time to fit model is 1.765761137008667 seconds
Fitted and ready!
preparing to scan 8189 files
trimmed down to 100 files



Measure the TfidfVectorizer
searching for agreements of type CONVERTIBLE
Corpus is loading 362 files
Time to load Plaintext corpus is 0.000110626220703125 seconds
Time to vectorize is 6.079673767089844e-05 seconds
Time to scroll through all raw fileids is 0.13658666610717773 seconds
Time to fit/transform matrix set is 41.894625186920166 seconds
Time to transform matrix set is 37.68284034729004 seconds
Time to fit model is 3.5915424823760986 seconds
Fitted and ready!
preparing to scan 8189 files
trimmed down to 100 files


Measure the CountVectorizer
searching for agreements of type CONVERTIBLE
Corpus is loading 362 files
Time to load Plaintext corpus is 0.00011706352233886719 seconds
Time to vectorize is 1.9788742065429688e-05 seconds
Time to scroll through all raw fileids is 0.13063859939575195 seconds
Time to fit/transform matrix set is 40.71795701980591 seconds
Time to transform matrix set is 36.724249839782715 seconds
Time to fit model is 1.7176897525787354 seconds
Fitted and ready!
preparing to scan 8189 files
trimmed down to 1000 files



Measure the TfidfVectorizer
searching for agreements of type CONVERTIBLE
Corpus is loading 362 files
Time to load Plaintext corpus is 0.00011491775512695312 seconds
Time to vectorize is 3.4809112548828125e-05 seconds
Time to scroll through all raw fileids is 0.10297536849975586 seconds
Time to fit/transform matrix set is 41.00924110412598 seconds
Time to transform matrix set is 37.14337658882141 seconds
Time to fit model is 3.275237560272217 seconds
Fitted and ready!
preparing to scan 8189 files
trimmed down to 1000 files

"""



class Agreement(object):
	def __init__(self, filename, agreement_type):
		self.filename = filename
		self.agreement_type = agreement_type

	def id_party_counterparty(self):
		""" Figures out who the party and counterparties are in an agreement """
		pass

	def determine_geography(self):
		""" 
		Function that determines the geospatial coordinates relevant to this agreement,
		usually a US state.  This is usually determined from the Governing Law and Jurisdiction
		provision.
		"""
		pass

	def get_stats(self):
		""" calculate some stats about the agreement """
		stats = {
			'sentence_count' : 0,
		}
		return stats	


"""
"""
if __name__ == "__main__":
    pass