#!/usr/bin/python
from nltk.corpus.reader.plaintext import PlaintextCorpusReader
from nltk.corpus import stopwords
from nltk import sent_tokenize
import os
import csv

corpus_root = './data/'
credit_agreement_data = []
convert_agreement_data = []

with open('classify-full.csv', 'rt') as csvfile:
	filereader = csv.reader(csvfile, delimiter=',', quotechar='|')
	for row in filereader:
		if (row[1] == 'CREDIT'):
			credit_agreement_data.append(row)
		elif (row[1] == 'CONVERTIBLE'):
			convert_agreement_data.append(row)

def readFile(filename):
	f = open(corpus_root + filename, 'r')
	lines = f.read()
	f.close()
	return lines	

def createAndWriteFile(filename, text):
	f = open(filename, 'w')
	f.write(text)
	f.close

data = convert_agreement_data
filenames = [n[0] for n in data]
filenames = filenames[0:5]
print(filenames)

def CreateDocsFromParas(filenames):
	# create a data structure that corresponds to all the documents
	docs = {}
	for filename in filenames:
		contents = readFile(filename)
		clause_list = []

		# sanitize the text in each paragraph
		for s in sent_tokenize(contents):
			words = s.split()
			filtered_words = [word for word in words if word not in stopwords.words('english')]
			paragraph = " ".join(filtered_words)
			clause_list.append(paragraph)

		docs[filename] = clause_list

	directory = corpus_root + 'clauses'
	if not os.path.exists(directory):
	    os.makedirs(directory)

	for filename in docs.keys():
		for i, para in enumerate(docs[filename]):
			# create a separate file for each paragraph
			createAndWriteFile(directory + '/' + filename + '_' + str(i), para)

	print("Files for each paragraph has been created from all the files listed above.")
	return True

def write_row(info):
    import csv
    with open('classify-paras.csv', 'a') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(info)


CreateDocsFromParas(filenames)

import time

print("Prepare a file for training.")

timestr = time.strftime("%Y%m%d-%H%M%S")
filename = "paragraphs-by-category.csv"
f = open(filename, "w+")
f.close()

def write_row(info):
    import csv
    with open('paragraphs-by-category.csv', 'a') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(info)

files = [ f for f in os.listdir('data/clauses') if os.path.isfile(os.path.join('data/clauses',f)) ]	

for filename in files:
	write_row([ filename, 'EMPTY'])

print("Reached the end.")

