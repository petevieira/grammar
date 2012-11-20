#!/usr/bin/python
#Filename: nGrams.py
<<<<<<< HEAD
import nltk.data
=======
asdfasdf
>>>>>>> 505e0a7ef22416e6b18a70ea057630777506b491
from nltk.corpus import brown
from nltk.util import *

# desired names for the ngram output files
fileNames = '1-grams', '3-grams', '4-grams', '5-grams'
# name of file being corrected
textFile = 'textfile'

# Fuction: getNGrams(words, fileName, n)
# Precondition: list of words from a corpus, a filename to be output, type of ngram
# Postcondition: file of n-grams and frequencies from corpus, one per line
# Description: takes a list of words from a corpus and finds all the n-grams
#		(where n specifies type of n-gram) and their respective
#		frequency counts, and writes each n-gram and their 
#		frequency to a file, line by line, with the n-gram and
#		its frequency separated by a tab.
def getNGrams(words, fileName, n):

	# puts all n-grams in a dictionary with format:
	# key : value equal to  n-gram : frequency.
	nGrams = dict()
	for i in range(len(words) - n + 1):
		gram = tuple(words[i:i+n])
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

# Fuction: getSentences(textfile)
# Precondition: a text file path location
# Postcondition: a sentences list of all sentences in textfile
# Description: takes a textfile and uses the nltk punkt sentence tokenizer
#		to break up all the sentences and put them in a list.
def getSentences(textfile):

	# get sentence tokenizer from nltk.data's punkt file english.pickle
	sent_tokenize = nltk.data.load('tokenizer/punkt/english.pickle')
	
	# extract sentences from textfile defined in global variable and put them in a list
	sentences = sent_tokenize.tokenize(open(textfile).read())
	
	return sentences	

# Function: getScores()
# Precondition: a list of sentences
# Postcondition: a dictionary of ngrams is each sentence and their score
# Description: takes a list of sentences and gets all the n-grams (1, 3, 5)
#		in a sentence and scores them based on the n-gram files
#		generated in the getNGrams() function called earlier.
#		It does so for every sentence.
def getScores(sentence):
	
	for fileName in fileNames:
		n = int(fileName[0])
		for i in range(len(sentence) - n + 1):
			gram = tuple(words[i:i+n])
			if gram in nGrams

if __name__ == '__main__':
	
	whichGrams = []

#	words = brown.words()
#	for fileName in fileNames:
#		n = int(fileName[0])
#		fileName = "./ngrams/" + fileName
#		print("Creating %s-file\n" % (n))
#		getNGrams(words, fileName, n)

	# extract sentences from textfile
	sentences = getSentences(textFile)
	print(sentences)
	
	getScores(sentences)

	print "program is done\n"
