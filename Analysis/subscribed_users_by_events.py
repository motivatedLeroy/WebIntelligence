#!/usr/bin/env python3
# Count the number of events (events with duplicate eventIds excluded) per
# subscribed user and print the result to subscribed_users_by_events.txt

import json
from operator import itemgetter
import os

input_fname = 'one_week/20170101'
output_dir = 'results/'
dup_event_ids_fname = output_dir + 'dup_eventIds.txt'
subscribed_uids_fname = output_dir + 'subscribed_userIds.txt'
output_fname = output_dir + 'subscribed_users_by_events.txt'

dup_event_ids = set()
with open(dup_event_ids_fname) as f:
    for line in f:
        dup_event_ids.add(int(line))

subscribed_uids = set()
with open(subscribed_uids_fname) as f:
    for line in f:
        subscribed_uids.add(line.strip())

# counts number of events grouped by userId
events_by_uid = {}
with open(input_fname) as f:
    for line in f:
        obj = json.loads(line.strip())
        eid, uid = obj['eventId'], obj['userId']
        if eid not in dup_event_ids and uid in subscribed_uids:
            if uid not in events_by_uid:
                events_by_uid[uid] = 1
            else:
                events_by_uid[uid] += 1

# count number of userIds grouped by number of events per userId
uids_by_events_count = {}
for uid, events_count in events_by_uid.items():
    if events_count not in uids_by_events_count:
        uids_by_events_count[events_count] = 1
    else:
        uids_by_events_count[events_count] += 1

os.makedirs(output_dir, exist_ok=True)
with open(output_fname, 'w') as f:
    for events_count, uids_count in sorted(uids_by_events_count.items(),
                                     key=itemgetter(0)):
        print('\t'.join([str(events_count), str(uids_count)]), file=f)
