#!/usr/bin/python
import os
import nltk
import inspect
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords

contracts_path = '/home/obironkenobi/Projects/ContractWiser/'
data_path = '/home/obironkenobi/Projects/ContractWiser/data'
tran_path = 'process'

def readFilenames():
	files = [ f for f in os.listdir(data_path) if os.path.isfile(os.path.join(data_path,f)) ]	
	return files

def readFile(filename):
	f = open(filename, 'r')
	lines = f.read()
	f.close()
	return lines

def writeSentences(data, filename):
	f = open(tran_path + '/' + filename + '.sent', 'w')
	for line in data:
		f.write(str(line) + '\n')
	f.close()

def remove_values_from_list(the_list, val):
   return [value for value in the_list if value != val]

def list_lengths(s):
	l = []
	for x in s:
		l.append(len(x))
	return l;

def write_row(info):
	import csv
	with open('classify.csv', 'a') as csvfile:
	    spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	    spamwriter.writerow(info)

filenames = readFilenames()
agreement_types = [];
error_counter = 0;
files_ctr = 0;
print("start a loop", end="\n")
for filename in filenames:
	try:
		filedata = readFile('./data/' + filename)
		sents = sent_tokenize(filedata)
		sents = sents[0:20]
		blocks = []
		for line in sents:
			words = word_tokenize(line)
			words = remove_values_from_list(words, ',')
			words = remove_values_from_list(words, '...')
			blocks.append(words) 

		agreement_types.append(blocks[0][0:15])

	except UnicodeDecodeError:
		error_counter += 1
		agreement_types.append(["error"])

	files_ctr += 1

print("---------output----------")
print("Files Analyzed: " + str(files_ctr))
print("Errors Reported: " + str(error_counter))
rate = 100.0 - float(error_counter)/files_ctr * 100
print("Success Rate: "  + format(rate, '.2f') + "%")
print("-------------------------")

for i, agree in enumerate(agreement_types):
	if agree != ['error']: 
		agree = remove_values_from_list(agree, '<')
		agree = remove_values_from_list(agree, 'PAGE')
		agree = remove_values_from_list(agree, '>')

filename = "classify.csv"
f = open(filename, "w+")
f.close()

analysis = []

for i, a in enumerate(agreement_types):
	b = " ".join(a)
	b = b.upper()
	
	CREDIT_COL = 0
	PURCHASE_COL = 1
	MERGER_COL = 2
	PROMIS_COL = 3
	CONVERT_COL = 4

	cnt = (b.count('CREDIT'), b.count('PURCHASE'), b.count('MERGER'), b.count('PROMISSORY'), b.count('CONVERTIBLE'), b.count('DEBT'), b.count('PAYMENT'))
	analysis.append(cnt)

	info = []

	if b == 'ERROR': 
		info = [i, filenames[i], "DECODE ERROR"]
	else:
		if cnt[CREDIT_COL] > 0:
			info = [i, filenames[i], "CREDIT AGREEMENT"]
		elif cnt[PURCHASE_COL] > 0: 
			info = [i, filenames[i], "PURCHASE AGREEMENT"]
		elif cnt[MERGER_COL] > 0:
			info = [i, filenames[i], "MERGER AGREEMENT"]
		elif cnt[PROMIS_COL] > 0: 
			info = [i, filenames[i], "CONVERTIBLE DEBT"]
		elif cnt[CONVERT_COL] > 0: 
			info = [i, filenames[i], "CONVERTIBLE DEBT"]
		else: 
			info = [i, filenames[i], "UNKNOWN"]

	write_row(info)

# read all the files
# get short "sentences", those are section headings
# transform them into blocks

# figure out what type of agreement they are
