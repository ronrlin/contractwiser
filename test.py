#!/usr/bin/python
import os
import zipfile

from sklearn import svm
import numpy as np

from sklearn import cross_validation

BASE_PATH = "/home/obironkenobi/Projects/ContractWiser/"

# train_interest_rate.txt
# train_maturity_date.txt
# train_principal_amount.txt
# train_change_in_control.txt
# train_dilution.txt
# train_conversion_to_equity.txt
# train_accredited_investors.txt
# train_security_law_compliance.txt
# train_repayment_schedule.txt
# train_notices_and_notifications.txt
# train_registration_rights.txt

train_files = [ 
	'train/train_interest_rate',
	'train/train_principal_amount',
	'train/train_notices_and_notifications',
	'train/train_registration_rights',
	'train/train_prepayment',
	'train/train_events_of_default'
]

# Read in a corpus from the train/ path
from nltk.corpus.reader.plaintext import PlaintextCorpusReader
TRAIN_PATH = os.path.join(BASE_PATH, "train/")
training_corpus = PlaintextCorpusReader(BASE_PATH, train_files)
print('Training files loaded...')
print(len(training_corpus.fileids()))

"""
Scroll through the training set files and collect the classifications of the 
training set files. The classifications are determined by the folder they are in.
"""
target_names = []
target = []
for tfile in training_corpus.fileids():
	for tpara in training_corpus.sents(tfile):	
		target_names.append(tfile)
		target.append(train_files.index(tfile))

"""
CountVectorizer is used to extract features from training set. 
Consider treating data to remove numbers, dates and names.  
- Use token_pattern to remove numbers
"""

my_stops = [ 'ii', 'iii', 'iv', 'vi', 'vii', 'viii', 'ix', 'xi', 'xii', 'xiii', 'january', 
	'february', 'march', 'april', 'may', 'june', 'july', 'august', 
	'september', 'october', 'november', 'december', '00', '000', '10', 
	'11', '12', '13', '14', '15', '16', '17', '18', '180', '19', '1933', 
	'1996', '20', '2001', '2002', '2003', '2004', '2009', '2006', '21', '25', 
	'250', '30', '31', '360', '365', '50', '500', '60', '90', '_________', 
	'_________________', '______________________', 'goodrich', 'american', 
	'whom', 'corporation', 'company' ]

from sklearn.feature_extraction.text import CountVectorizer
contentvec = CountVectorizer(input='content', stop_words=my_stops, ngram_range=(1,2))

# Flatten the sentences into a list of strings
testp = list(' '.join(s) for s in training_corpus.sents())

dtm = contentvec.fit_transform(testp)
search_terms = contentvec.get_feature_names()
# print(search_terms)

# create the 'target' which specifies what classification to associate with each para
conv_fileids = ['891daf5deebf3e31b7bb1c2970ac1c507d50818aa4db2dfd0b7e9b344a340202',
	'a28b2f92979d4ac8ae1e31e7d1a91e8c9145074105d1254ea24565cb40c0328e', 
	'27ec7f0412b4973261c2e64ad11b2f379cf61dcf73e03d623ad1e3648904f312', ]

TEST_PATH = os.path.join(BASE_PATH, "small-data/")
test_corpus = PlaintextCorpusReader(TEST_PATH, conv_fileids)

print('Test files loaded...')
print(len(test_corpus.fileids()))

# Flatten the sentences from the test set into a list of strings
fileid = conv_fileids[2]
print('File read: ' + fileid)
testsents = list(' '.join(s) for s in test_corpus.sents(fileid))
dtm_test = contentvec.transform(testsents)

print('-------------------------------')
print('Linear Classififer')
cll = svm.LinearSVC(class_weight='auto')
cll.fit(dtm, target)
linear_results = cll.predict(dtm_test)
lhumanreadable = [train_files[i] for i in linear_results]

import numpy as np
provisions_cnt = np.zeros(len(train_files))
for i, l in enumerate(linear_results.tolist()):
	provisions_cnt[int(l)] += 1
print(provisions_cnt)

scores = cross_validation.cross_val_score(cll, dtm, np.array(target), cv=5)
print('cross validation')
print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

print('-------------------------------')
print('SDG Classifier')
from sklearn.linear_model import SGDClassifier
cld = SGDClassifier(n_iter=100, alpha=0.01)
cld.fit(dtm, target)
dlinear_results = cld.predict(dtm_test)

provisions_cnt = np.zeros(len(train_files))
for i, l in enumerate(dlinear_results.tolist()):
	provisions_cnt[int(l)] += 1

print(provisions_cnt)
scores = cross_validation.cross_val_score(cld, dtm, np.array(target), cv=5)
print('cross validation')
print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

print('-------------------------------')
print("list of the categories")
print(train_files)

"""
print_provisos is a utility function that prints all provisions matching type ntype.
"""
def print_provisos(ntype):
	for i, l in enumerate(linear_results.tolist()):
		if (l == ntype):
			print(str(i) + ' : ' + testsents[i])

"""
This is a utility to input paragraphs of text to test the classifier.

Parameters
----------

para : list of strings

returns numpy array with classifier
"""
def classify_paragraph(para):
	this_dtm = contentvec.transform(para)
	r = cld.predict(this_dtm)
	for i in r:
		print(train_files[i])
	return r
