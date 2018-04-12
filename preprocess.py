#!/usr/bin/env python3

import glob
import json

raw_datasets = sorted(glob.glob('one_week/*'))
session_map_data = 'session_map.csv'
article_map_data = 'article_map.csv'
train_data = 'train_one_week'
collaborative = 'collaborative.csv'
articles_data = 'articles.csv'
hits_data = 'hits.csv'
test_data = 'test_one_week'
test_hits = 'test_hits.csv'

rating_scale = { 'min': 1, 'max': 5 }

def normalize(value, source_scale, target_scale):
    return (target_scale['min'] + (value - source_scale['min'])
            * (target_scale['max'] - target_scale['min'])
            / (source_scale['max'] - source_scale['min']))

print('\nscanning subscribed users 1/5')
session_uid_map = {}
session_count = 0

lines_count = 0
with open(session_map_data, 'w') as fsmap:
    print('sessionId\tuserId', file=fsmap)
    for raw_dataset in raw_datasets:
        with open(raw_dataset) as fin:
            for line in fin:
                obj = json.loads(line.strip())
                uid = obj['userId']
                if uid not in session_uid_map and 'pluss' in obj['url']:
                    sid = session_count
                    session_count += 1
                    print('\t'.join([str(sid), uid]), file=fsmap)
                    session_uid_map[uid] = sid

                lines_count += 1
                print('scanning: {} line(s) read, {} session ids'.
                      format(lines_count, len(session_uid_map)), end='\r')
    print()

print('\nscanning articles 2/5')
article_id_map = {}
article_count = 0

lines_count = 0
with open(article_map_data, 'w') as famap:
    print('articleId\tid', file=famap)
    for raw_dataset in raw_datasets:
        with open(raw_dataset) as fin:
            for line in fin:
                obj = json.loads(line.strip())
                uid = obj['userId']
                if uid in session_uid_map:
                    iid = obj.get('id', None)
                    if iid is not None and iid not in article_id_map:
                        aid = article_count
                        article_count += 1
                        print('\t'.join([str(aid), iid]), file=famap)
                        article_id_map[iid] = aid

                lines_count += 1
                print('scanning: {} line(s) read, {} article ids'.
                      format(lines_count, article_count), end='\r')
    print()

print('\nextracting articles & computing active time scale 3/5')
articles = set()
active_time_scale = {}

lines_count = 0
with open(train_data) as fin, open(articles_data, 'w') as fart:
    print('item\tcontent', file=fart)
    for line in fin:
        obj = json.loads(line.strip())
        uid = obj['userId']
        if uid in session_uid_map:
            iid = obj.get('id', None)
            if iid is not None and iid not in articles:
                keywords = obj.get('keywords', None)
                if keywords is not None:
                    aid = article_id_map[iid]
                    print('\t'.join([str(aid), keywords]), file=fart)
                    articles.add(iid)

            active_time = obj.get('activeTime', None)
            if active_time is not None:
                min_active_time = active_time_scale.get('min', active_time)
                max_active_time = active_time_scale.get('max', active_time)
                active_time_scale['min'] = min(min_active_time, active_time)
                active_time_scale['max'] = max(max_active_time, active_time)

        lines_count += 1
        print('extracting: {} line(s) read, {} articles'.format(
            lines_count, len(articles)), end='\r')
print()

print('\nextracting coll and hits 4/5')
print_coll_count = 0
print_hits_count = 0

lines_count = 0
with open(train_data) as fin, open(collaborative, 'w') as fcoll, open(
        hits_data, 'w') as fhits:
    print('user\titem\trating', file=fcoll)
    print('user\titem', file=fhits)
    for line in fin:
        obj = json.loads(line.strip())

        is_news_article = 'id' in obj
        uid = obj['userId']
        if is_news_article and uid in session_uid_map:
            iid = obj['id']
            sid = session_uid_map[uid]
            aid = article_id_map[iid]

            active_time = obj.get('activeTime', None)
            if active_time is not None:
                active_time = normalize(active_time, active_time_scale,
                                        rating_scale)
                print('\t'.join([str(sid), str(aid), str(active_time)]), file=fcoll)
                print_coll_count += 1

            print('\t'.join([str(sid), str(aid)]), file=fhits)
            print_hits_count += 1

        lines_count += 1
        print('extracting: {} line(s) read, {} coll {} hits'.
              format(lines_count, print_coll_count, print_hits_count), end='\r')
    print()

print('\nextracting test hits 5/5')
print_hits_count = 0

lines_count = 0
with open(test_data) as fin, open(test_hits, 'w') as fhits:
    print('user\titem', file=fhits)
    for line in fin:
        obj = json.loads(line.strip())

        is_news_article = 'id' in obj
        uid = obj['userId']
        if is_news_article and uid in session_uid_map:
            iid = obj['id']
            sid = session_uid_map[uid]
            aid = article_id_map[iid]

            print('\t'.join([str(sid), str(aid)]), file=fhits)
            print_hits_count += 1

        lines_count += 1
        print('extracting: {} line(s) read, {} hits'.
              format(lines_count, print_hits_count), end='\r')
    print()
