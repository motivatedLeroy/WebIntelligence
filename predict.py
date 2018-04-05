#!/usr/bin/env python3

from surprise import Dataset
from surprise import Reader
from surprise import SVD
from surprise import accuracy
from surprise.model_selection import KFold

dataset_file = 'collaborative.csv'

reader = Reader(line_format='user item rating', sep='\t')
data = Dataset.load_from_file(dataset_file, reader=reader)
algo = SVD()
kf = KFold(n_splits=10)

for trainset, testset in kf.split(data):
    algo.fit(trainset)
    predictions = algo.test(testset)
    accuracy.rmse(predictions, verbose=True)
