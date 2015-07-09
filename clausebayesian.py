#!/usr/bin/python

# look in classify-full.csv, and grab just credit agreements

# create a corpus from the specific agreements

# train 
# classify

import nltk
import csv
import random
import os
from nltk.corpus.reader.plaintext import PlaintextCorpusReader
from nltk.corpus.reader import CategorizedCorpusReader
from nltk.corpus.reader.plaintext import CategorizedPlaintextCorpusReader

# NOTE: 
# install nltk 3.0.3
# install numpy with pip3

def getWordsFromDoc(filename):
    filename = './data/' + filename
    try: 
        f = open(filename, 'r')
        lines = f.read()
        f.close()
    except UnicodeDecodeError:
        print('File read error in %s ' % filename)

    return nltk.word_tokenize(lines)

corpusdir = './data/clauses' # Directory of corpus.

data = []
with open('classify-paras.csv', 'rt') as csvfile:
    filereader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in filereader:
        data.append(row)

d = {}
for row in data:
    d[row[0]] = [ row[1] ]

# consider using cat_pattern, cat_map seems to not be working
catcorpus = CategorizedPlaintextCorpusReader(corpusdir, '.*', cat_map=d)

texts = [(list(catcorpus.words(fileid)), category) for category in catcorpus.categories() for fileid in catcorpus.fileids(category)]

#augments texts
random.shuffle(texts)

strip_chars = '*_-. '

#converts to lowercase and calcultates fd
words_ds = nltk.FreqDist(words.lower().rstrip(strip_chars) for words in catcorpus.words())
#words_bigrams = nltk.bigrams(words.lower() for words in catcorpus.words())

# force into a list
words_bigrams = list(nltk.bigrams(words.lower().rstrip(strip_chars) for words in catcorpus.words()))
for t in words_bigrams:
    if (t[0] == 'credit'):
        print(': ' + t[0] + ' ' + t[1])
    elif (t[0] == 'convertible'):
        print('> ' + t[0] + ' ' + t[1])


#use words as features
word_features = list(words_ds)[:3000]
bigram_features = list(words_bigrams)[:3000]

#each word from a doc in checked if it has our features
def get_features(doc):
    doc_words = set(doc)

    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in doc_words)

    features['paragraph_count'] = doc.count('.')
    features['word_count'] = len(doc)

    return features

#def get_para_features():
#    features['paragraph_count(%s)' % para_count]
#    return features;

#save features for each doc in each class
featuresets = [(get_features(_doc), _class) for (_doc,_class) in texts]


#splits docs between our sets
train_set, test_set = featuresets[1:20], featuresets[21:30]
print ("# training dataset: ", len(train_set))
print ("# test dataset: ", len(test_set))

#give train set to classifier
classifier = nltk.NaiveBayesClassifier.train(train_set)

#print accuracy
print("Accuracy is: ")
print(nltk.classify.accuracy(classifier, test_set))
#prints some cool features
print(classifier.show_most_informative_features(20))

filename = "classify-full.csv"
f = open(filename, "w+")
f.close()

def write_row(info):
    import csv
    with open('classify-full.csv', 'a') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(info)

directory = './data/'
filenames = [ f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory,f)) ]   
for filename in filenames:
    cat = classifier.classify(get_features(getWordsFromDoc(filename)))
#    print('Filename %s is ' % filename + ' ' + cat)
    write_row([filename, cat])



