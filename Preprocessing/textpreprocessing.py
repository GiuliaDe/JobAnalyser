from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import nltk
import re

STOPWORDS = set(stopwords.words('italian'))

def filter(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    #tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    cl_text = re.sub(r'[^A-Za-z0-9+#-]+',' ', text)
    tokens=cl_text.split(' ')
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z0-9]', token):
            filtered_tokens.append(token.lower())
    return ' '.join(filtered_tokens)

def stopwordremoval(text):
    #print STOPWORDS
    cleanwords=[]
    words = text.split(' ')
    for word in words:
        if word not in STOPWORDS:
            cleanwords.append(word)
    return ' '.join(cleanwords)

def stemming(text):
    stemwords=[]
    ps = PorterStemmer()
    words = text.split(' ')
    for word in words:

        try:
            stemwords.append(ps.stem(word))
        except:
            pass

    return ' '.join(stemwords)

def tokenizer(text):
    return text.split(' ')


