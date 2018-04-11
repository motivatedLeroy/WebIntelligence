#!/usr/bin/env python3

import glob
import json
from sys import argv

raw_datasets = sorted(glob.glob('one_week/*'))
train_data = 'train_one_week'
collaborative = 'collaborative.csv'
articles_data = 'articles.csv'
hits_data = 'hits.csv'
test_data = 'test_one_week'
test_hits = 'test_hits.csv'

rating_scale = { 'min': 1, 'max': 5 }

max_lines = int(argv[1]) if len(argv) > 1 else None

def normalize(value, source_scale, target_scale):
    return (target_scale['min'] + (value - source_scale['min'])
            * (target_scale['max'] - target_scale['min'])
            / (source_scale['max'] - source_scale['min']))

print('\nscanning subscribed users 1/5')
subscribed_users = set()

max_reached = False

lines_count = 0
for raw_dataset in raw_datasets:
    with open(raw_dataset) as fin:
        for line in fin:
            if max_lines is not None and lines_count == max_lines:
                max_reached = True
                break

            obj = json.loads(line.strip())
            uid = obj['userId']
            if uid not in subscribed_users and 'pluss' in obj['url']:
                subscribed_users.add(uid)

            lines_count += 1
            print('scanning: {} line(s) read, {} subscribed users'.
                  format(lines_count, len(subscribed_users)), end='\r')
    if max_reached:
        break
print()

print('\ncomputing sessions 2/5')
user_sessions_count = {}
active_sessions = {}
session_user_event_map = {}

unsubusers_count = 0

max_reached = False

lines_count = 0
for raw_dataset in raw_datasets:
    with open(raw_dataset) as fin:
        for line in fin:
            if max_lines is not None and lines_count == max_lines:
                max_reached = True
                break

            obj = json.loads(line.strip())
            uid, eid = obj['userId'], obj['eventId']
            if uid in subscribed_users:
                sid = uid
            else:
                start, stop = obj['sessionStart'], obj['sessionStop']
                if start or uid not in active_sessions:
                    session_count = user_sessions_count.get(uid, 0)
                    user_sessions_count[uid] = session_count + 1
                    sid = uid + '#' + str(session_count)
                    active_sessions[uid] = sid
                    unsubusers_count += 1
                else:
                    sid = active_sessions[uid]

                if stop:
                    del active_sessions[uid]

            if uid not in session_user_event_map:
                session_user_event_map[uid] = {}
            session_user_event_map[uid][eid] = sid

            lines_count += 1
            print('computing: {} line(s) read, {} unsubscribed users'.
                  format(lines_count, unsubusers_count), end='\r')
    if max_reached:
        break
print()

print('\nextracting articles & computing active time scale 3/5')
articles = set()
active_time_scale = {}

lines_count = 0
with open(train_data) as fin, open(articles_data, 'w') as fart:
    print('item\tcontent', file=fart)
    for line in fin:
        if max_lines is not None and lines_count == max_lines:
            break

        obj = json.loads(line.strip())

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
        if (max_lines is not None and max_lines == lines_count):
            break

        obj = json.loads(line.strip())

        uid, eid = obj['userId'], obj['eventId'] # move this down
        sid = session_user_event_map[uid][eid]

        is_news_article = 'id' in obj
        if is_news_article:
            iid = obj['id']

            active_time = obj.get('activeTime', None)
            if active_time is not None:
                active_time = normalize(active_time, active_time_scale,
                                        rating_scale)
                print('\t'.join([sid, iid, str(active_time)]), file=fcoll)
                print_coll_count += 1

            print('\t'.join([sid, iid]), file=fhits)
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
        if (max_lines is not None and max_lines == lines_count):
            break

        obj = json.loads(line.strip())

        is_news_article = 'id' in obj
        if is_news_article:
            uid, eid, iid = obj['userId'], obj['eventId'], obj['id']
            sid = session_user_event_map[uid][eid]
            print('\t'.join([sid, iid]), file=fhits)
            print_hits_count += 1

        lines_count += 1
        print('extracting: {} line(s) read, {} hits'.
              format(lines_count, print_hits_count), end='\r')
    print()
