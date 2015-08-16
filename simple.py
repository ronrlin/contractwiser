#!/usr/bin/python
import os
import zipfile

from sklearn import svm
import numpy as np

from sklearn import cross_validation

train_sentences = [
	'The dog goes to the park.',
	'The cat is a miserable animal in the park.',
	'The dog barks and is happy.',
	'Cats have claws.',
	'The cat is so cute.',
]

#train_sentences = ['The', 'dog', 'goes', 'to', 'the', 'park.']
#	'The cat is a miserable animal in the park.',
#	'The dog barks and is happy.',
#	'Cats have claws.',
#	'The cat is so cute.',
#	]



target = ['dog', 'cat', 'dog', 'cat', 'cat']

from sklearn.feature_extraction.text import CountVectorizer
contentvec = CountVectorizer(input='content', ngram_range=(1,1))

dtm = contentvec.fit_transform(train_sentences)
search_terms = contentvec.get_feature_names()
print(search_terms)

class_weight = dict()
for i, s in enumerate(search_terms):
	if (s == 'dog'):
		class_weight[i] = 0.
	elif (s == 'park'):
		class_weight[i] = 1.
	elif (s == 'happy'):
		class_weight[i] = 0.65
	else:
		class_weight[i] = 2

print(class_weight)

# Flatten the sentences from the test set into a list of strings
testsents = ['The cat in the hat.',
	'Let us play with the dog',
	'Cats are so cute.'
	]

dtm_test = contentvec.transform(testsents)

cll = svm.LinearSVC(class_weight='auto')
cll.fit(dtm, target)
svcresults = cll.predict(dtm_test)

from sklearn.linear_model import SGDClassifier
cld = SGDClassifier(n_iter=100, alpha=0.01)
cld.fit(dtm, target)
sdgresults = cld.predict(dtm_test)

from sklearn.linear_model import SGDClassifier
cld = SGDClassifier(n_iter=100, alpha=0.01)
cld.fit(dtm, target)
sdgresults = cld.predict(dtm_test)

