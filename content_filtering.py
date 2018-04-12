
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
with open('sarticles.csv', newline='') as trainFile1, open('shits.csv', newline='') as trainFile2 :
    trainSet1 = csv.reader(trainFile1, delimiter='\t')
    trainSet2 = csv.reader(trainFile2, delimiter='\t')
    articles = list(trainSet1)#dict([ (a[0], a[1]) for a in trainSet1 ])
    userList = list(trainSet2)# list(map(itemgetter(0), trainSet2))

articles.pop(0)
#print(articles)
keywordList = list(map(itemgetter(1), articles))
#print (keywordList)
articleIds = list(map(itemgetter(0), articles))
#for ind in range(len(articles)):
#    print(articleIds[ind])

#userlist reorganising
betterUsers = {}
#i = 0
#j= 0
for user in userList:
    if user[0] in betterUsers.keys():
        #i= i+1
        if user[1] not in betterUsers[user[0]]:
            betterUsers[user[0]].append(user[1])
            #if user[1] in articleIds:
                #print("Article exists! ", user[1])
        #else:
            #j = j +1
    elif user[0] not in betterUsers.keys():
        betterUsers[user[0]] = [user[1]]
#print(betterUsers)
#print("Count of users with multiple articles", i)
#print("Count of users with just one article", j)

# for x in betterUsers:
#     print("User: ",x)
#     for y in betterUsers[x]:
#         print("Articles:")
#         print("[")
#         print(y)
#         print("]")
#exit(0)
#making the tfidf/count matrix
count = CountVectorizer()
count_matrix = count.fit_transform(keywordList)
#print(count_matrix)
shape = count_matrix.shape
print("Count Matrix Shape: ", shape)
print(len(keywordList))
#performing cosine similarity
cosine_sim = cosine_similarity(count_matrix) #calculates pairwise sim. between all samples in matrix
#print("Cosine Sim: ", cosine_sim)
#and this similarity matrix should be used for each user to get his new fav articles
recommUser = userList[0]
#get recommUser.favArticle of cosine_sim and of this list the articles with sim!=0
# so both lists(matrix and article and keywords) has to be sorted strictly by index

# for each user:
    #for each article:
        # get the similarity-array
        #gehe durch und hole index wo nicht =0 und nicht i=j
        # hole articleID mit diesem index und speicher in similarArticles: (artID, sim)
similarArticles = {}
sc = 0
nokeyword = 0
counter = 0
for user, arts in betterUsers.items():
    #Nimm einen User
    print("User:  ", user)
    print(counter)
    print(len(betterUsers))
    sim_per_user = {}
    print("Read Articles: ", len(arts))
    # durchsuche seine gelesenen artikel
    for a in arts:
        #Liste für Ähnlichkeit aller anderen Artikel
        sim_per_article = {}
        #print(a)
        #Wenn ein gelesener Artikel in den ArtikelIDs auftaucht
        if a in articleIds:
            #Setze Index des gelesen Artikels entsprechden der ArtikelID
            as_i =  articleIds.index(a)
            #print("Article: ", a, "FOUND here:", as_i)
            #print(len(articleIds), "similaritymatrix: ", len(cosine_sim))
            #erstelle eine temporäre liste um die similarity des gelesenen artikels (der keywörter hat) mit anderen
            # Artikeln zu vergleichen
            tmp_sim_list = list(zip(articleIds, cosine_sim[as_i])) #combine sims with articleIDs
            for i in range(len(tmp_sim_list)):
                #wenn i nicht auf den gelesen artikel zeigt, die similarity größer 0 ist und der verglichene
                #artikel noch nicht gelesen wurde, addiere die similarity auf
                if i != as_i and tmp_sim_list[i][1] != 0 and tmp_sim_list[i][0] not in arts:
                    #aufsummieren wenn schon im user
                    if tmp_sim_list[i][0] in sim_per_user.keys():
                        #print("Ich summiere! ", sim_per_user[tmp_sim_list[i][0]], " + ", tmp_sim_list[i][1])
                        new_value = sim_per_user[tmp_sim_list[i][0]] + tmp_sim_list[i][1]
                        sim_per_user[tmp_sim_list[i][0]] = new_value

                    else:
                        sim_per_user[tmp_sim_list[i][0]] = tmp_sim_list[i][1]
                    sc = sc + 1
                #else:
                    #tmp_sim_list[i] = 0
        else:
            nokeyword = nokeyword +1
            #print("Article without keyword found!")
            # sort sim_per_Article per sim and cut the 0s
    with open('contentbased.txt', 'a') as f:
            for a, v in sim_per_user.items():
                # csvwriter.writerow([userID, article, a])
                if(v > 5):
                    f.write(user + "," + a + "," + str(v) + "\n")
    #similarArticles[user] = sim_per_user
    counter = counter+1
    #print("Result: ", sim_per_user)
    #print("Similarities: ", sim_per_user)
print("Found Sims: ",sc)
print("No keywords: ", nokeyword)
#print(similarArticles)
#fields = ['user', 'articles', 'similarity']
#with open('output.csv', 'w') as f:
    #csvwriter = csv.DictWriter(f, fieldnames=fields)
    #w.writeheader()



#with open('contentbased.txt', 'w') as f:
    #for userID, article in similarArticles.items():
        #for a,v in article.items():
            #csvwriter.writerow([userID, article, a])
            #f.write(userID+","+a+","+str(v)+"\n")



            #print(userID,a,v)
    #for userID, article in similarArticles.items():
    #    for a in article:
    #        print(userID,article,a)
    #        csvwriter.writerow([userID, article, a])
    #writer = csv.writer(csvfile)#, fieldnames='user, articles')
    #writer.writeheader()
    #users = similarArticles
    #for data in similarArticles:
        #writer.writerow(data)

#for sim in cosine_sim:


print('>>> Done!')
print(datetime.datetime.now())
print(datetime.datetime.now()-time1)



#sorting the matrix
#similar_indices = cosine_sim.argsort().flatten()
#print("Similar Indices: ", similar_indices)
#print("And shape: ", similar_indices.shape)
#similar_items = sorted([(idList[i], cosine_sim[0, i]) for i in similar_indices], key=lambda x: -x[1]) #this does not work
#this is not working because idList has another shape than similiar_indices
# and will not work at all because similar_indices just contains similarities but no IDs
#print(similar_items)
