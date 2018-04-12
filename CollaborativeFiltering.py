from surprise import KNNBasic, Reader, Prediction
from surprise import Dataset
from surprise.model_selection import KFold
from surprise import accuracy
import surprise.prediction_algorithms.algo_base.AlgoBase

reader = Reader(line_format='user	item	rating', sep='	', skip_lines=1, rating_scale=(1,40000))

data = Dataset.load_from_file('collaborative.csv', reader=reader)

sim_options = {'name':'cosine',
               'user_based': True
               }

algo = KNNBasic(sim_options = sim_options)
algo.train(data)
kf = KFold(n_splits=10)

for trainset, testset in kf.split(data):
    algo.fit(trainset)
    predictions = algo.test(testset, verbose=True)
    rmse = accuracy.rmse(predictions, verbose=True)
    mae = accuracy.mae(predictions, verbose=True)








