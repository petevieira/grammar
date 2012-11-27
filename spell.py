import operator
import itertools
import distance
import nltk.data
import random
import scorer


def correct(text):
	# load sentence tokenzier from nltk
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

    sentences = []
	# for each sentence in 'text' break it up into words
    # and append it as a list item to 'sentences'
    # tokenizer.tokenize(text) splits 'text' into sentences
    # words(s) splits each sentence 's' into words separated
    # by commas 
    for s in tokenizer.tokenize(text):
        sentences.append(words(s))

    candSents = confusionSets(sentences)

	# create trigrams from candidate sentences
    trigrams = []
    cid = 0
    for (cs, sid) in candSents:
        trigrams += trigramify(cs, (sid, cid))
        cid += 1
    trigrams.sort()

    #run score function
    scoredgrams = map(lambda (t0, t1, t2, ((sid, cid), wid)):
            (sid, cid, wid, t1, 1), trigrams)
    #getScore(trigrams)

    scoredgrams.sort()
    #print scoredgrams

    nsentences = []
    bsid = 0
    bcid = 0
    bwid = 0
    cand = []
    candS = []
    candidates = []
    for (sid, cid, wid, t1, score) in scoredgrams + [(None,None,None,None,None)]:
        if (bcid != cid or bsid != sid) and cand != []:
            candidates.append( calcScore(cand) )
            cand = []
        if bsid != sid:
            candidates.sort(reverse=True)
            print candidates
            nsentences.append(candidates[0][1])
            candidates = []
        cand.append( (t1, score, wid) )
        #print sid,cid,wid, cand
        bsid = sid
        bcid = cid
        bwid = wid
    #print
    #print scoredgrams
    #print
    #print nsentences
    return " ".join(map(lambda s: " ".join(s), nsentences))

def calcScore(s):
    #print s
    assert( len(s) != 0 )
    rs = []
    score=0
    for (((d, s1), w), s2, wid) in s:
        rs.append(w)
        score += s1 + s2 + d
    return (score, rs)

# Takes a list of sentences formed by comma-separated words
# and  
def confusionSets(sentences):

	# gets a list of lists of trigrams for each sentence
	# in the text and sets tcgrams equal to it
    tcgrams = taggedConfusionTrigrams(sentences)
    #print tcgrams
    #print
    tcgrams.sort() # how is this sorted

    #run candidate generator
    #tcgrams = map(lambda (t0, t1, t2, (sid, wid)):
    #        ((sid, wid), t1, random.random()), tcgrams)
	# generates sets of confusion words based on trigrams
    tcgrams = scorer.generate(tcgrams)
    tcgrams.sort()
    #print tcgrams
    #print

	# generate a list of n empty list, where n
	# is the number of sentences in the text.
	# this will be used to store a list of candidate
	# sentences
    candidates = nEmpty(len(sentences))

	# for each word in the confusion set of each word in
	# each sentence store this candidate word, its score,
	# sentence id and word id in 'candidates' list and
	# do this for each confusion set word to create a list
	# of candidate sentences to replace the original sentence
    for ((sid, wid), t1, score) in tcgrams:
        if len(candidates[sid]) == 0:
            candidates[sid] = nEmpty(len(sentences[sid]))
        candidates[sid][wid].append((t1, score))

	# for each sentence and candidate sentence get each
	# corresponding word and candidate word and calculate
	# the Damerau Levenshtein distance between them
    candSents = []
    sid = 0
    for (s,css) in zip(sentences, candidates):
        ncss = []
        for (word,cs) in zip(s,css):
            ncs = []
            for (candidate,score) in cs:
                dist = distance.distance(candidate, word)
                ncs.append( ((-dist, score), candidate) )
            ncs.sort(reverse=True)
            #print word, ncs
            ncss.append(ncs[0:5])
            #ncss.append(ncs)
        
        candSents += map(lambda s: (s, sid), combinations2(ncss))
        sid += 1
    #print candidates
    #print candSents
    candSents.sort()
    return candSents

# Create a list of n empty lists, where n is the
# number of sentences in the text being corrected
def nEmpty(n):
    return [[] for i in xrange(n)]

# takes a sentence, 's', and sentence id, 'sid',
# and creates all the trigrams in the sentence with
# corresponding sentence id's 'sid' and word id's 'wid'
# which corresponds to the middle word of the trigram,
# adds all of the these trigram,id pairs to a list and
# returns it. 
def trigramify(words, sid):
    o = []				# create empty list
    wid = -1
    t0 = "^"			# beginning of sentence marker
    t1 = "^"
	# create trigrams, where t0, t1 and w are the
	# three words in the trigram, with sentence id
    # and word id corresponding to the word in the
    # middle of the trigram 
    for w in words:
        if wid >= 0:
            o.append( (t0, t1, w, (sid, wid)) )
        t0 = t1
        t1 = w
        wid += 1
    # add the last trigram with the last two words and
    # and the end of sentence marker, '$'
    o.append( (t0, t1, "$", (sid, wid)) )
    return o	# return list of trigrams with sid's and wid's

# takes a list of sentences and tags them with
# the trigrams in each sentence and each trigram's
# sentence id 'sid' and middle word id 'wid'
# and creates a list of lists of trigrams for
# each sentence.
def taggedConfusionTrigrams(sentences):
    o = []		#create empty list
    sid = 0		
	# for each sentence in 'sentences' create a list
	# of all the trigrams and their sentence and word id's
	# and add each one to the list 'o'
    for s in sentences:
        o += trigramify(s, sid)
        sid += 1
    return o


def words(sentence):
    return sentence.split(" ")

def combinations(ls):
    if len(ls) == 0:
        return []
    if len(ls) == 1:
        return ls[0]
    tail = combinations(ls[1:])
    return [l+" "+t for l in ls[0] for t in tail]

def combinations2(ls):
    if len(ls) == 0:
        return [[]]
    tail = combinations2(ls[1:])
    return [[l]+t for l in ls[0] for t in tail]

if __name__ == '__main__':
    #print combinations([["0","1"], ["2","3"], ["4","5"]])
    #print combinations([["0","1"], ["2","3","5"]])
    #print combinations([["0","1","3"], ["2","3","5"]])
    #print combinations([["0","1"], ["0","1"]])
    #print combinations([["0","1"], ["0","1"], ["0","1"]])
    #print combinations([[], ["0","1"]])
    #print combinations([[]])
    #print combinations([])
    #print combinations2([["0","1"], ["0","1"]])
    #print combinations2([[], ["0","1"]])
    #print combinations2([[]])
    #print combinations2([])

	# text to be checked
    ss = ["This is a sentence .", "This is another sentence .", "Hello"]
    #print taggedConfusionTrigrams(map(words, ss))
	# run spell checker and print result
    print correct(" ".join(ss))
