#!/usr/bin/env python3

import json

raw_dataset = 'one_week/20170102'
collaborative = 'collaborative.csv'
content = 'content.csv'

with open(raw_dataset) as fin, open(collaborative, 'w') as fcoll, open(
        content, 'w') as fcont:
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
        if active_time_recorded: # TODO: consider default active time
            active_time = obj['activeTime']
            print('\t'.join([uid, iid, str(active_time)]), file=fcoll)

        keywords_avaiable = 'keywords' in obj
        if keywords_avaiable:
            keywords = obj['keywords']
            print('\t'.join([uid, iid, keywords]), file=fcont)

        # TODO: print progress
