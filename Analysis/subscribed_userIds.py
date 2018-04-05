#!/usr/bin/env python3
# Filter out userIds of subscribed users and print them to subscribed_userIds.txt

import json
import os

input_fname = 'one_week/20170101'
output_dir = 'results/'
output_fname = output_dir + 'subscribed_userIds.txt'

subscribed_uids = set()
with open(input_fname) as f:
    for line in f:
        obj = json.loads(line.strip())
        uid, url = obj['userId'], obj['url']
        if uid not in subscribed_uids and '/pluss' in url:
            subscribed_uids.add(uid)

os.makedirs(output_dir, exist_ok=True)
with open(output_fname, 'w') as f:
    for uid in sorted(subscribed_uids):
        print(uid, file=f)

print(len(subscribed_uids), 'subscribed userId(s) found.')
