from sklearn.feature_extraction.text import TfidfVectorizer
import mysql.connector

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
#from __future__ import print_function
import pandas as pd
import nltk
import re
from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer("english")




def tokenize_only(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    return filtered_tokens


db=mysql.connector.connect(host="localhost",user="giulia",
                  passwd="giulia",db="JobTest")

cursor = db.cursor(buffered=True)


query_select = "SELECT testo FROM lavori_all WHERE testo IS NOT NULL AND entity_processed=1 LIMIT 5"
cursor.execute(query_select)
jobs = cursor.fetchall()

db.close()

lavori=[]
for job in jobs:
    lavori.append(job[0])

#print lavori

#define vectorizer parameters
tfidf_vectorizer = TfidfVectorizer(max_df=0.8, max_features=200000,
                                 min_df=0.2, stop_words='english',
                                 use_idf=True, ngram_range=(1,3))

tfidf_matrix = tfidf_vectorizer.fit_transform(lavori) #fit the vectorizer to synopses

print(tfidf_matrix.shape)

terms = tfidf_vectorizer.get_feature_names()

dist = 1 - cosine_similarity(tfidf_matrix)

#print dist



num_clusters = 2

km = KMeans(n_clusters=num_clusters)
km.fit(tfidf_matrix)
clusters = km.labels_.tolist()
#print clusters


totalvocab_stemmed = []
totalvocab_tokenized = []
for i in lavori:
    allwords_stemmed = tokenize_and_stem(i)  # for each item in 'synopses', tokenize/stem
    totalvocab_stemmed.extend(allwords_stemmed)  # extend the 'totalvocab_stemmed' list

    allwords_tokenized = tokenize_only(i)
    totalvocab_tokenized.extend(allwords_tokenized)

vocab_frame = pd.DataFrame({'words': totalvocab_tokenized}, index = totalvocab_stemmed)
frame = pd.DataFrame(lavori, index = [clusters] , columns = ['testo'])

print("Top terms per cluster:")
print()
# sort cluster centers by proximity to centroid
order_centroids = km.cluster_centers_.argsort()[:, ::-1]

for i in range(num_clusters):
    print("Cluster %d words:" % i)

    for ind in order_centroids[i, :6]:  # replace 6 with n words per cluster
        print(' %s' % vocab_frame.ix[terms[ind].split(' ')].values.tolist()[0][0].encode('utf-8', 'ignore'))
    print()  # add whitespace
    print()  # add whitespace

    print("Cluster %d titles:" % i)
    for title in frame.ix[i]['title'].values.tolist():
        print(' %s,' % title)
    print()  # add whitespace
    print()  # add whitespace

print()
print()