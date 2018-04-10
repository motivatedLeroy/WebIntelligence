#!/usr/bin/env python3

import glob
import json
from sys import argv

train_data = 'train_one_week'
collaborative = 'collaborative.csv'
content = 'content.csv'

rating_scale = { 'min': 1, 'max': 5 }

max_lines = int(argv[1]) if len(argv) > 1 else None

def scan_line(line, subscribed_users, active_time_scale):
    obj = json.loads(line.strip())

    uid = obj['userId']
    if uid not in subscribed_users and 'pluss' in obj['url']:
        subscribed_users.add(uid)

    if 'activeTime' in obj:
        active_time = obj['activeTime']
        if ('min' not in active_time_scale
            or active_time < active_time_scale['min']):
            active_time_scale['min'] = active_time
        if ('max' not in active_time_scale
            or active_time > active_time_scale['max']):
            active_time_scale['max'] = active_time

def normalize(value, source_scale, target_scale):
    return (target_scale['min'] + (value - source_scale['min'])
            * (target_scale['max'] - target_scale['min'])
            / (source_scale['max'] - source_scale['min']))

def parse_line(line, subscribed_users, active_time_scale, sessions_count,
               sessions):
    obj = json.loads(line.strip())

    is_news_article = 'id' in obj
    if not is_news_article:
        return None

    iid = obj['id']
    event = { 'iid': iid }

    uid, eid = obj['userId'], obj['eventId']

    if uid in subscribed_users:
        event['uid'] = uid
    else:
        start, stop = obj['sessionStart'], obj['sessionStop']
        if start or uid not in sessions:
            sessions_count[uid] = sessions_count.get(uid, 0) + 1
            sid = uid + '#' + str(sessions_count[uid])
            sessions[uid] = sid
        else:
            sid = sessions[uid]

        if stop:
            del sessions[uid]

        event['uid'] = sid

    active_time = obj['activeTime'] if 'activeTime' in obj else None
    if active_time is not None:
        active_time = normalize(active_time, active_time_scale, rating_scale)
    event['active_time'] = active_time

    event['keywords'] = obj['keywords'] if 'keywords' in obj else None

    return event

print('\n1st pass: scanning (limit:{})'.format(max_lines))
subscribed_users = set()
active_time_scale = {}

lines_count = 0
with open(train_data) as fin:
    for line in fin:
        if max_lines is not None and lines_count == max_lines:
            break

        scan_line(line, subscribed_users, active_time_scale)

        lines_count += 1
        print('scanning: {} line(s) read, {} subscribed users found.'.
              format(lines_count, len(subscribed_users)), end='\r')
print()

print('\n2nd pass: preprocessing (limit:{})'.format(max_lines))
sessions_count = {}
sessions = {}

print_coll_count = 0
print_cont_count = 0

lines_count = 0
with open(train_data) as fin, open(collaborative, 'w') as fcoll, open(
        content, 'w') as fcont:
    print('user\titem\trating', file=fcoll)
    print('user\titem\tcontent', file=fcont)
    for line in fin:
        if (max_lines is not None and max_lines == lines_count):
            break

        event = parse_line(line, subscribed_users, active_time_scale,
                           sessions_count, sessions)
        if event is not None:
            iid, uid = event['iid'], event['uid']
            active_time = event['active_time']
            keywords = event['keywords']

            if (active_time is not None):
                print('\t'.join([uid, iid, str(active_time)]), file=fcoll)
                print_coll_count += 1

            if (keywords is not None):
                print('\t'.join([uid, iid, keywords]), file=fcont)
                print_cont_count += 1

        lines_count += 1
        print('preprocessing: {} line(s) read, {}@coll, {}@cont written.'.
              format(lines_count, print_coll_count, print_cont_count), end='\r')
    print()
