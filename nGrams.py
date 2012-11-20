#!/usr/bin/python
#Filename: nGrams.py
import nltk.data
from nltk.corpus import brown
from nltk.util import *

# desired names for the ngram output files
fileNames = '1-grams', '3-grams', '4-grams', '5-grams'

# Fuction: getNGrams(words, fileName, n)
# Precondition: list of words from a corpus, a filename to be output, type of ngram
# Postcondition: file of n-grams and frequencies from corpus, one per line
# Description: takes a list of words from a corpus and finds all the n-grams
#		(where n specifies type of n-gram) and their respective
#		frequency counts, and writes each n-gram and their 
#		frequency to a file, line by line, with the n-gram and
#		its frequency separated by a tab.
def getNGrams(sentences, fileName, n):

	# puts all n-grams in a dictionary with format:
	# key : value equal to  n-gram : frequency.
	nGrams = dict()
	for sent in sentences:
		for i in range(len(sent) - n + 1):
			gram = tuple(sent[i:i+n])
			if gram in nGrams:
				nGrams[gram] += 1
			else:
				nGrams[gram] = 1
	# gets the keys (n-grams) from dictionary of n-grams and sorts them
	keylist = nGrams.keys()
	keylist.sort()
	
	# writes ngrams and frequencies line by line tab-delimited to a file
	file = open(fileName, "w")
	for key in keylist:
		file.write("%s\t%s\n" % (" ".join(key), nGrams[key]))
	file.close()	


if __name__ == '__main__':
	
	sentences = brown.sents()
	for fileName in fileNames:
		n = int(fileName[0])
		fileName = "./ngrams/" + fileName
		print("Creating %s-file\n" % (n))
		getNGrams(sentences, fileName, n)

	print "program is done\n"
