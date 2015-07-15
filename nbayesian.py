#!/usr/bin/python
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

corpusdir = './small-data/' # Directory of corpus.

# Use classify-temp as the classifications of record for training set
data = []
with open('classify-temp.csv', 'rt') as csvfile:
    filereader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in filereader:
        data.append(row)

# data is a list, convert it to dict type... ughh. Better way?
d = {}
for row in data:
    d[row[0]] = [ row[1] ]

catcorpus = CategorizedPlaintextCorpusReader(corpusdir, '.*', cat_map=d)
texts = [(list(catcorpus.words(fileid)), category) for category in catcorpus.categories() for fileid in catcorpus.fileids(category)]

#augments texts
random.shuffle(texts)

strip_chars = '*_-. '
# Remove Stopwords
# prepare stopword list.  problem is the default removes stopwords I want to keep
# keep 'not'

from nltk.corpus import stopwords

#stops = set(stopwords.words("english"))
#words = [words for words in catcorpus.words()]
#filtered_words = [word for word in word_list if word not in stops]

# TODO: Remove numbers, non-dictionary characters, 

# Converts to lowercase and calcultates freq. dist of words
words_ds = nltk.FreqDist(words.lower().rstrip(strip_chars) for words in catcorpus.words())

#use words as features
word_features = list(words_ds)[:3000] # TODO not sure why the 3000 limitation?????
#use "representative" bigrams as features
bigram_features = list([('principal', 'amount'), ('maturity', 'date'), ('interest', 'rate'), ('applicable', 'rate'), ('conversion', 'rate'), ('conversion', 'formula'), ('change', 'control'), ('events' 'default'), ('events' 'termination'), ('make' 'whole'), ('default' 'interest'), ('rights' 'remedies'), ('payment' 'principal'), ('accrued' 'interest'), ('convertible' 'debt')])

#each word from a doc in checked if it has our features
def get_features(doc):
    doc_words = set(doc)

    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in doc_words)

    # Look for features of Convertible Debt Agreement
    doc_bigrams = list(nltk.bigrams(doc_words))
    for bigram in bigram_features:
        features['contains(%s)' % " ".join(bigram)] = (bigram in doc_bigrams) 

    # Look for features of Credit Agreement

    features['paragraph_count'] = doc.count('.')
    features['word_count'] = len(doc)

    return features

#def get_para_features():
#    features['paragraph_count(%s)' % para_count]
#    return features;

#save features for each doc in each class
featuresets = [(get_features(_doc), _class) for (_doc,_class) in texts]

#splits docs between our sets
train_set, test_set = featuresets[1:200], featuresets[201:]
print ("# training dataset: ", len(train_set))
print ("# test dataset: ", len(test_set))

#give train set to classifier
classifier = nltk.NaiveBayesClassifier.train(train_set)

#print accuracy
print("Accuracy is: ")
print(nltk.classify.accuracy(classifier, test_set))
#prints some cool features
print(classifier.show_most_informative_features(100))

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



