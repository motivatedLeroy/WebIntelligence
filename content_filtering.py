
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import linear_kernel
import csv
import datetime
from operator import itemgetter

time1= datetime.datetime.now()
print(time1)
print('>>> Start content filtering...')
#reading the csv files
with open('articles.csv', newline='') as trainFile1, open('hits.csv', newline='') as trainFile2 :
    trainSet1 = csv.reader(trainFile1, delimiter='\t')
    trainSet2 = csv.reader(trainFile2, delimiter='\t')
    articles = list(trainSet1)
    userList = list(trainSet2)

#delete header
articles.pop(0)
# split into keywords and articles
keywordList = list(map(itemgetter(1), articles))
articleIds = list(map(itemgetter(0), articles))

#userlist reorganising
betterUsers = {}
for user in userList:
    if user[0] in betterUsers.keys():
        # user did not read the article yet
        if user[1] not in betterUsers[user[0]]:
            betterUsers[user[0]].append(user[1])
    elif user[0] not in betterUsers.keys():
        betterUsers[user[0]] = [user[1]]

# Vectorizer
count = CountVectorizer()
count_matrix = count.fit_transform(keywordList)
shape = count_matrix.shape
print("Count Matrix Shape: ", shape)
print(len(keywordList))
#performing cosine similarity
cosine_sim = cosine_similarity(count_matrix)

# calculating similiar articles for each user
for user, arts in betterUsers.items():
    sim_per_user = {}
    for a in arts:
        sim_per_article = {}
        if a in articleIds:
            as_i =  articleIds.index(a)
            #combine sims with articleIDs
            tmp_sim_list = list(zip(articleIds, cosine_sim[as_i])) 
            for i in range(len(tmp_sim_list)):
                # if not sim to itself and not 0 and not already read
                if i != as_i and tmp_sim_list[i][1] != 0 and tmp_sim_list[i][0] not in arts:
                    if tmp_sim_list[i][0] in sim_per_user.keys():
                        new_value = sim_per_user[tmp_sim_list[i][0]] + tmp_sim_list[i][1]
                        sim_per_user[tmp_sim_list[i][0]] = new_value
                    else:
                        sim_per_user[tmp_sim_list[i][0]] = tmp_sim_list[i][1]
    with open('contentbased.txt', 'a') as f:
            for a, v in sim_per_user.items():
                if(v > 5):
                    f.write(user + "," + a + "," + str(v) + "\n")

print('>>> Done!')
print(datetime.datetime.now())
print(datetime.datetime.now()-time1)

