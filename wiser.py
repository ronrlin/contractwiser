#!/usr/bin/python
import nltk

print('hello, wiser.')

filename = '5349cea14e798a309bbf4db09dc53fc9d478ac7e8bae7bc95ad6ee0da51ebeac';
directory = 'data/'

import os
from nltk.corpus.reader.plaintext import PlaintextCorpusReader

corpusdir = './small-data/' # Directory of corpus.
credit_agreements = './data/credit'
merger_agreements = './data/merger'
newcorpus = PlaintextCorpusReader(corpusdir, '.*')
print(newcorpus.words())
print(newcorpus.fileids())
print(newcorpus.sents())

l = []
for sents in newcorpus.sents():
	l.append(len(sents))

sum_l = sum(l)
print(sum(l)/len(l))

x = FreqDist(newcorpus.words())
mc = x.most_common()
mcp = [i for i in mc if i[1] > 5]

f = open('./data/' + filename, 'r')
lines = f.read()
f.close()

tokens = nltk.word_tokenize(lines)
ff = nltk.Text(tokens)

#nltk.Text(newcorpus)

# To access pargraphs of a specific fileid.
#print newcorpus.paras(newcorpus.fileids()[0])

# Access sentences in the corpus. (list of list of strings)
# NOTE: That the texts are flattened into sentences that contains tokens.
#print newcorpus.sents()
#print 'blah\n'

# To access sentences of a specific fileid.
#print newcorpus.sents(newcorpus.fileids()[0])

# Access just tokens/words in the corpus. (list of strings)
#print newcorpus.words()

# To access tokens of a specific fileid.
#print newcorpus.words(newcorpus.fileids()[0])