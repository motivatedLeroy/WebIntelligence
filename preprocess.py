#!/usr/bin/env python3

import glob
import json
from sys import argv

raw_datasets = sorted(glob.glob('one_week/*'))
collaborative = 'collaborative.csv'
content = 'content.csv'

max_print_count = int(argv[1]) if len(argv) > 1 else None
max_scan_count = max_print_count * 10 if max_print_count is not None else None

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

print('\n1st pass: scanning for subscribed users (limit:{})'.format(
    max_scan_count))
subscribed_users = set()

max_reached = False

read_count = 0
for raw_dataset in raw_datasets:
    print('scanning: {}'.format(raw_dataset).ljust(80))
    with open(raw_dataset) as fin:
        for line in fin:
            if max_scan_count is not None and read_count == max_scan_count:
                max_reached = True
                break

            scan_line(line, subscribed_users)

            read_count += 1
            print('scanning: {} line(s) read, {} subscribed users found.'.
                  format(read_count, len(subscribed_users)), end='\r')
    if max_reached:
        break

print()

print('\n2nd pass: preprocessing (limit:{})'.format(max_print_count))
sessions_count = {}
sessions = {}

max_reached = False
print_coll_count = 0
print_cont_count = 0

read_count = 0
with open(collaborative, 'w') as fcoll, open(content, 'w') as fcont:
    print('user\titem\trating', file=fcoll)
    print('user\titem\tcontent', file=fcont)
    for raw_dataset in raw_datasets:
        print('preprocessing: {}'.format(raw_dataset).ljust(80))
        with open(raw_dataset) as fin:
            for line in fin:
                if (max_print_count is not None and max_print_count
                    == print_coll_count == print_cont_count):
                    max_reached = True
                    break

                event = parse_line(line, subscribed_users, sessions_count,
                                   sessions)
                if event is not None:
                    iid, uid = event['iid'], event['uid']
                    active_time = event['active_time']
                    keywords = event['keywords']

                    if (active_time is not None
                        and (max_print_count is None
                             or print_coll_count < max_print_count)):
                        print('\t'.join([uid, iid, str(active_time)]),
                              file=fcoll)
                        print_coll_count += 1

                    if (keywords is not None
                        and (max_print_count is None
                             or print_cont_count < max_print_count)):
                        print('\t'.join([uid, iid, keywords]), file=fcont)
                        print_cont_count += 1

                read_count += 1
                print('preprocessing: {} line(s) read, {}@coll, {}@cont written.'.
                      format(read_count, print_coll_count, print_cont_count),
                      end='\r')
        if max_reached:
            break
    print()
