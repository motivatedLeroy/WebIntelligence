#!/usr/bin/env python3

import glob
import json
from sys import argv

train_data = 'train_one_week'
collaborative = 'collaborative.csv'
articles_data = 'articles.csv'
hits_data = 'hits.csv'

rating_scale = { 'min': 1, 'max': 5 }

max_lines = int(argv[1]) if len(argv) > 1 else None

def normalize(value, source_scale, target_scale):
    return (target_scale['min'] + (value - source_scale['min'])
            * (target_scale['max'] - target_scale['min'])
            / (source_scale['max'] - source_scale['min']))

print('\n1st pass (limit:{})'.format(max_lines))
subscribed_users = set()
articles = set()
active_time_scale = {}

lines_count = 0
with open(train_data) as fin, open(articles_data, 'w') as fart:
    print('item\tcontent', file=fart)
    for line in fin:
        if max_lines is not None and lines_count == max_lines:
            break

        obj = json.loads(line.strip())

        uid = obj['userId']
        if uid not in subscribed_users and 'pluss' in obj['url']:
            subscribed_users.add(uid)

        iid = obj.get('id', None)
        if iid is not None and iid not in articles:
            keywords = obj.get('keywords', None)
            if keywords is not None:
                print('\t'.join([iid, keywords]), file=fart)
                articles.add(iid)

        active_time = obj.get('activeTime', None)
        if active_time is not None:
            min_active_time = active_time_scale.get('min', active_time)
            max_active_time = active_time_scale.get('max', active_time)
            active_time_scale['min'] = min(min_active_time, active_time)
            active_time_scale['max'] = max(max_active_time, active_time)

        lines_count += 1
        print('{} line(s) read, {}@subusers {}@articles'.format(
            lines_count, len(subscribed_users), len(articles)), end='\r')
print()

print('\n2nd pass (limit:{})'.format(max_lines))
sessions_count = {}
sessions = {}

print_coll_count = 0
print_hits_count = 0

lines_count = 0
with open(train_data) as fin, open(collaborative, 'w') as fcoll, open(
        hits_data, 'w') as fhits:
    print('user\titem\trating', file=fcoll)
    print('user\titem', file=fhits)
    for line in fin:
        if (max_lines is not None and max_lines == lines_count):
            break

        obj = json.loads(line.strip())

        is_news_article = 'id' in obj
        if is_news_article:
            iid = obj['id']

            uid, eid = obj['userId'], obj['eventId']

            if uid not in subscribed_users:
                start, stop = obj['sessionStart'], obj['sessionStop']
                if start or uid not in sessions:
                    sessions_count[uid] = sessions_count.get(uid, 0) + 1
                    sid = uid + '#' + str(sessions_count[uid])
                    sessions[uid] = sid
                else:
                    sid = sessions[uid]

                if stop:
                    del sessions[uid]

                uid = sid

            active_time = obj.get('activeTime', None)
            if active_time is not None:
                active_time = normalize(active_time, active_time_scale,
                                        rating_scale)
                print('\t'.join([uid, iid, str(active_time)]), file=fcoll)
                print_coll_count += 1

            print('\t'.join([uid, iid]), file=fhits)
            print_hits_count += 1

        lines_count += 1
        print('preprocessing: {} line(s) read, {}@coll, {}@hits written.'.
              format(lines_count, print_coll_count, print_hits_count), end='\r')
    print()
