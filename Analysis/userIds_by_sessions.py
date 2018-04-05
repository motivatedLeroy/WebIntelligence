#!/usr/bin/env python3
# Calculates how many times userIds are reused between sessions (subscribed
# users excluded) and prints the results to userIds_by_sessions.txt

import json
from operator import itemgetter
import os

input_fname = 'one_week/20170101'
output_dir = 'results/'
subscribed_uids_fname = output_dir + 'subscribed_userIds.txt'
output_fname = output_dir + 'userIds_by_sessions.txt'

subscribed_uids = set()
with open(subscribed_uids_fname) as f:
    for line in f:
        subscribed_uids.add(line.strip())

# counts number of sessions grouped by userId
sessions_by_uid = {}
with open(input_fname) as f:
    for line in f:
        obj = json.loads(line.strip())
        uid, start = obj['userId'], obj['sessionStart']
        if uid not in subscribed_uids and start:
            if uid not in sessions_by_uid:
                sessions_by_uid[uid] = 1
            else:
                sessions_by_uid[uid] += 1

# count number of userIds grouped by number of sessions per userId
uids_by_sessions_count = {}
for uid, sessions_count in sessions_by_uid.items():
    if sessions_count not in uids_by_sessions_count:
        uids_by_sessions_count[sessions_count] = 1
    else:
        uids_by_sessions_count[sessions_count] += 1

os.makedirs(output_dir, exist_ok=True)
with open(output_fname, 'w') as f:
    for sessions_count, uids_count in sorted(uids_by_sessions_count.items(),
                                     key=itemgetter(0)):
        print('\t'.join([str(sessions_count), str(uids_count)]), file=f)
