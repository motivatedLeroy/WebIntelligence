#!/usr/bin/env python3

import json
from sys import argv

raw_dataset = 'one_week/20170102'
collaborative = 'collaborative.csv'
content = 'content.csv'

max_print_count = int(argv[1]) if len(argv) > 1 else None

def scan_line(line, subscribed_users):
    obj = json.loads(line.strip())

    uid = obj['userId']
    if uid not in subscribed_users and 'pluss' in obj['url']:
        subscribed_users.add(uid)

def parse_line(line, subscribed_users, sessions_count, sessions):
    obj = json.loads(line.strip())

    is_news_article = 'id' in obj
    if not is_news_article:
        return None

    iid = obj['userId']
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

    event['active_time'] = obj['activeTime'] if 'activeTime' in obj else None
    event['keywords'] = obj['keywords'] if 'keywords' in obj else None

    return event

subscribed_users = set()
print('\n1st pass: scanning for subscribed users')
with open(raw_dataset) as fin:
    read_count = 0

    for line in fin:
        scan_line(line, subscribed_users)

        print('preprocessing: {} line(s) read, {} subscribed users found.'.
              format(read_count, len(subscribed_users)), end='\r')
        read_count += 1
print()

sessions_count = {}
sessions = {}
print('\n2nd pass: preprocessing')
with open(raw_dataset) as fin, open(collaborative, 'w') as fcoll, open(
        content, 'w') as fcont:
    print_coll_count = 0
    print_cont_count = 0

    read_count = 0

    print('user\titem\trating', file=fcoll)
    print('user\titem\tcontent', file=fcont)
    for line in fin:
        if (max_print_count is not None
            and print_coll_count == print_cont_count == max_print_count):
            break

        event = parse_line(line, subscribed_users, sessions_count, sessions)
        if event is not None:
            iid, uid = event['iid'], event['uid']
            active_time, keywords = event['active_time'], event['keywords']

            if (active_time is not None
                and (max_print_count is None
                     or print_coll_count < max_print_count)):
                print('\t'.join([uid, iid, str(active_time)]), file=fcoll)
                print_coll_count += 1

            if (keywords is not None
                and (max_print_count is None
                     or print_cont_count < max_print_count)):
                print('\t'.join([uid, iid, keywords]), file=fcont)
                print_cont_count += 1

        read_count += 1
        print('preprocessing: {} line(s) read, {}@coll, {}@cont written.'.
              format(read_count, print_coll_count, print_cont_count), end='\r')

print()
