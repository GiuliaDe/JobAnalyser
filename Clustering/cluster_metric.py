from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer

def list_common_entities(entity_1, entity_2):
    return list(set(entity_1).intersection(entity_2))


def tfidfmatrix(testo):
    tfidf_vectorizer = TfidfVectorizer(max_df=0.9, max_features=200000,
                                 min_df=0.1, stop_words='english',
                                 use_idf=True, ngram_range=(1,3))

    tfidf_matrix = tfidf_vectorizer.fit_transform(testo)
    return tfidf_matrix

def getdistancefromtfidf(matrix):
    return 1 - cosine_similarity(matrix)


def tfidfkmeans(matrix,num_clusters):
    km = KMeans(n_clusters=num_clusters)
    km.fit(matrix)
    clusters = km.labels_.tolist()
    return clusters

