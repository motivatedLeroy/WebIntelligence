#!/usr/bin/env python3
# Generate sessionIds and print them to sids_by_eids.txt

import json
from operator import itemgetter
import os

input_fname = 'one_week/20170101'
output_dir = 'results/'
subscribed_uids_fname = output_dir + 'subscribed_userIds.txt'
output_fname = output_dir + 'sids_by_eids.txt'

subscribed_uids = set()
with open(subscribed_uids_fname) as f:
    for line in f:
        subscribed_uids.add(line.strip())

# counts number of events grouped by userId
sid = 0
sids_by_subscribed_uid = {}
sids_by_uid = {}
sids_by_eids = {}
with open(input_fname) as f:
    for line in f:
        obj = json.loads(line.strip())
        eid, uid, start = obj['eventId'], obj['userId'], obj['sessionStart']
        if uid in subscribed_uids:
            if uid not in sids_by_subscribed_uid:
                sids_by_subscribed_uid[uid] = sid
                sid += 1
            sids_by_eids[eid] = sids_by_subscribed_uid[uid]
        else:
            if start or uid not in sids_by_uid:
                sids_by_uid[uid] = sid
                sid += 1
            sids_by_eids[eid] = sids_by_uid[uid]

os.makedirs(output_dir, exist_ok=True)
with open(output_fname, 'w') as f:
    for eid, sid in sorted(sids_by_eids.items(),
                                     key=itemgetter(0)):
        print('\t'.join([str(eid), str(sid)]), file=f)
