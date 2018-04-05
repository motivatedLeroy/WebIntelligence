#!/usr/bin/env python3

import json

raw_dataset = 'one_week/20170102'
collaborative = 'collaborative.csv'

with open(raw_dataset) as fin, open(collaborative, 'w') as fcoll:
    for line in fin:
        obj = json.loads(line.strip())
        is_news_article = 'id' in obj
        if not is_news_article:
            continue # no usable information

        uid, iid = obj['userId'], obj['id']
        subscribed = 'pluss' in obj['url']
        if not subscribed:
            continue # TODO: extract sessions for unsubscribed users

        active_time_recorded = 'activeTime' in obj
        if not active_time_recorded:
            continue # TODO: consider default active time

        active_time = obj['activeTime']
        print('\t'.join([uid, iid, str(active_time)]), file=fcoll)

        # TODO: print progress
