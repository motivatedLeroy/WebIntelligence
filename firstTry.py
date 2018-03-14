
"""Created on 14. March 2018

@author: Anna Baumgard
"""

import json
import os
import datetime
from surprise import Dataset
from surprise import KNNBasic
from surprise import Reader
from surprise import SVD
from sklearn.model_selection import KFold

output_fname1 = 'dataset1.txt'
output_fname2 = 'dataset2.txt'

input_fname = '20170101'
rootPath = os.path.abspath('.')
input_file = rootPath + os.sep + input_fname

time1= datetime.datetime.now()
print(time1)
print('>>> Start reading file...')
with open(output_fname1, 'a') as f1:
    with open(output_fname2, 'a') as f2:
        for line in open(input_file):
            obj = json.loads(line.strip())
            try:
                uid, iid = obj['userId'], obj['id']
                keywords = obj['keywords'] if 'keywords' in obj else 'None'
                active_time = str(obj['activeTime']) if 'activeTime' in obj else '0'
            except Exception as e:
                continue
            if not keywords=='None':
                print('\t'.join([uid, iid, keywords]).encode('utf8'), file=f2)
            if not active_time=='0':
                print('\t'.join([uid, iid, active_time]).encode('utf8'), file=f1)
print('>>> Done!')
print(datetime.datetime.now())
print(datetime.datetime.now()-time1)

reader = Reader(line_format='user item rating', sep='   ')
data = Dataset.load_from_file('dataset_file', reader=reader)
algo = SVD()
kf = KFold()

for trainset, testset in kf.split(data):
    algo.fit(trainset)
    predictions = algo.test(testset)

