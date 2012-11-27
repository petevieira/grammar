import nltk.data
import nltk.tokenize

def words(sentence):
    return nltk.tokenize.word_tokenize(sentence)
    #return sentence.split(" ")

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
def splitSentence(text):
    sentences = []
    for s in tokenizer.tokenize(text):
        sentences.append(words(s))
    return sentences

def trigramify(words, sid):
    o = []
    wid = -1
    t0 = "^"
    t1 = "^"
    for w in words:
        if wid >= 0:
            o.append( (t0, t1, w, (sid, wid)) )
        t0 = t1
        t1 = w
        wid += 1
    o.append( (t0, t1, "$", (sid, wid)) )
    return o


