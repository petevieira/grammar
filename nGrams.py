#!/usr/bin/python
#Filename: nGrams.py
asdf
from nltk.corpus import brown
from nltk.util import *

fileNames = '1-grams', '3-grams', '4-grams', '5-grams'

def getNGrams(words, fileName, n):

	nGrams = dict()
	for i in range(len(words) - n + 1):
		gram = tuple(words[i:i+n])
		if gram in nGrams:
			nGrams[gram] += 1
		else:
			nGrams[gram] = 1
#	print nGrams
	keylist = nGrams.keys()
	keylist.sort()
#	for key in keylist:
#		print "%s\t%s" % (key, nGrams[key])
	
	file = open(fileName, "w")
	for key in keylist:
		file.write("%s\t%s\n" % (" ".join(key), nGrams[key]))
	file.close()	

if __name__ == '__main__':
	
	print "Cowabunga\n"
	whichGrams = []

	words = brown.words()
#	string = "Boy, do I wish I were younger. Don't you?"
#	words = string.split(' ')
	for fileName in fileNames:
		n = int(fileName[0])
		fileName = "./ngrams/" + fileName
		print("Creating %s-grams file\n" % (n))
		getNGrams(words, fileName, n)

	print "program is done\n"
