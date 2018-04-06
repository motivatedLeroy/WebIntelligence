#!/usr/bin/env python3

import json
from sys import argv

raw_dataset = 'one_week/20170102'
collaborative = 'collaborative.csv'
content = 'content.csv'

max_print_count = int(argv[1]) if len(argv) > 1 else None

with open(raw_dataset) as fin, open(collaborative, 'w') as fcoll, open(
        content, 'w') as fcont:
    read_count = 0
    print_coll_count = 0
    print_cont_count = 0
    sessions_count = {}
    sessions = {}

    print()
    print('user\titem\trating', file=fcoll)
    print('user\titem\tcontent', file=fcont)
    for line in fin:
        read_count += 1
        print('preprocessing: {} line(s) read, {}@coll, {}@cont written.'.
              format(read_count, print_coll_count, print_cont_count), end='\r')

        if (max_print_count is not None
            and print_coll_count == print_cont_count == max_print_count):
            break

        obj = json.loads(line.strip())
        is_news_article = 'id' in obj
        if not is_news_article:
            continue # no usable information

        uid, iid, eid = obj['userId'], obj['id'], obj['eventId']
        subscribed = 'pluss' in obj['url']
        if not subscribed:
            start, stop = obj['sessionStart'], obj['sessionStop']
            if not start and uid not in sessions:
                #print('warning: session not initialized [eid:{}]'.format(eid))
                start = True

            if start:
                sessions_count[uid] = sessions_count.get(uid, 0) + 1
                sid = uid + '#' + str(sessions_count[uid])
                #if uid in sessions:
                #    print('warning: session not terminated [eid:{}, c:{}]'.
                #          format(eid, sessions_count[uid] - 1))
                sessions[uid] = sid
            else:
                sid = sessions[uid]

            if stop:
                del sessions[uid]

            uid = sid

        if max_print_count is None or print_coll_count < max_print_count:
            active_time_recorded = 'activeTime' in obj
            if active_time_recorded: # TODO: consider default active time
                active_time = obj['activeTime']
                print('\t'.join([uid, iid, str(active_time)]), file=fcoll)
                print_coll_count += 1

        if max_print_count is None or print_cont_count < max_print_count:
            keywords_avaiable = 'keywords' in obj
            if keywords_avaiable:
                keywords = obj['keywords']
                print('\t'.join([uid, iid, keywords]), file=fcont)
                print_cont_count += 1

    print()
