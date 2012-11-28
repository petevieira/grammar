import nltk.data
import nltk.tokenize

def words(sentence):
    return nltk.tokenize.word_tokenize(sentence)
    #return sentence.split(" ")

def unwords(sentence):
    return " ".join(sentence)

def unsentences(sentences):
    return " ".join(map(unwords,sentences))

# load sentence tokenzier from nltk
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

# for each sentence in 'text' break it up into words
# and append it as a list item to 'sentences'
# tokenizer.tokenize(text) splits 'text' into sentences
# words(s) splits each sentence 's' into words separated
# by commas 
def splitSentence(text):
    sentences = []
    for s in tokenizer.tokenize(text):
        sentences.append(words(s))
    return sentences

# takes a sentence, 's', and sentence id, 'sid',
# and creates all the trigrams in the sentence with
# corresponding sentence id's 'sid' and word id's 'wid'
# which corresponds to the middle word of the trigram,
# adds all of the these trigram,id pairs to a list and
# returns it. 
def trigramify(words, sid):
    o = []           # create empty list
    wid = -1
    t0 = "^"         # beginning of sentence marker
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
    return o


def gramify(n, sent, id):
    l = []
    sent = ["^"] + sent + ["$"]
    for i in range(len(sent) - n + 1):
        gram = sent[i:i+n]
        l.append( (gram, (id, i)) )
    return l
        


def betweens(words, sid):
    o = []
    wid = -1
    t0 = "^"
    for w in words:
        if wid >= 0:
            o.append( (t0, "", w, (sid, wid)) )
        t0 = w
        wid += 2
    o.append( (t0, "", "$", (sid, wid)) )
    return o

def intersperse(iterable, delimiter):
    it = iter(iterable)
    yield next(it)
    for x in it:
        yield delimiter
        yield x

