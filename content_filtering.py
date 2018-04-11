
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import linear_kernel
import csv
from operator import itemgetter

#reading the csv files
with open('articles.csv', newline='') as trainFile1, open('hits.csv', newline='') as trainFile2 :
    trainFile1.readline()
    trainSet1 = csv.reader(trainFile1, delimiter='\t')
    trainFile2.readline()
    trainSet2 = csv.reader(trainFile2, delimiter='\t')
    keywordList = list(map(itemgetter(1), trainSet1))
    idList = list(map(itemgetter(0), trainSet1))
    userList = list(map(itemgetter(0), trainSet2))
print (keywordList)

#making the tfidf/count matrix
#count = CountVectorizer()
tfidf = TfidfVectorizer()
#count_matrix = count.fit_transform(keywordList)
tfidf_matrix = tfidf.fit_transform(keywordList)
tfidf_feature_names = tfidf.get_feature_names()
shape = tfidf_matrix.shape
#print(tfidf_matrix)
print(shape)

#performing cosine similarity
#cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
#cosine_sim = cosine_similarity(count_matrix, count_matrix)
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
print(cosine_sim)

#sorting the matrix
similar_indices = cosine_sim.argsort().flatten()
print(similar_indices)
similar_items = sorted([(idList[i], cosine_sim[0, i]) for i in similar_indices], key=lambda x: -x[1]) #this does not work
print(similar_items)

