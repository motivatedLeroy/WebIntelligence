#!/usr/bin/env python3

import csv
from operator import itemgetter

results_data = 'Results.csv'

recommendations = {}
with open(results_data, newline='') as fresults:
    reader = csv.DictReader(fresults, delimiter=',')
    for result in reader:
        if result['prediction'] == '1.0':
            if result['user'] not in recommendations:
                recommendations[result['user']] = []
            recommendations[result['user']].append(result)

ctr_top10 = 0
ctr_top20 = 0
arhr = 0
arhr_count = 0
for user_recommendations in recommendations.values():
    user_recommendations.sort(key=lambda r: float(r['similarity_score']) * float(r['collaborative_score']))
    for count, recommendation in enumerate(user_recommendations):
        if recommendation['label'] == '1.0':
            rank = count + 1
            arhr += 1/rank
            arhr_count += 1
            if count < 20:
                ctr_top20 += 1
                if count < 10:
                    ctr_top10 += 1

ctr_top10 /= len(recommendations) * 10.0
ctr_top20 /= len(recommendations) * 20.0
arhr /= arhr_count

print('CTR top 10: {} CTR top 20: {} ARHR: {}'.
      format(ctr_top10, ctr_top20, arhr))
