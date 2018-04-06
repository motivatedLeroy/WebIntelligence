#!/usr/bin/env python3
# Count the number of events per session and print the result to
# sessions_by_events.txt

import json
from operator import itemgetter
import os

input_fname = 'one_week/20170101'
output_dir = 'results/'
sids_by_eids_fname = output_dir + 'sids_by_eids.txt'
output_fname = output_dir + 'sessions_by_events.txt'

sids_by_eids = {}
with open(sids_by_eids_fname) as f:
    for line in f:
        eid, sid = line.strip().split('\t')
        sids_by_eids[int(eid)] = int(sid)

# counts number of events grouped by sessionId
events_by_sid = {}
with open(input_fname) as f:
    for line in f:
        obj = json.loads(line.strip())
        eid = obj['eventId']
        sid = sids_by_eids[eid]
        if sid not in events_by_sid:
            events_by_sid[sid] = 1
        else:
            events_by_sid[sid] += 1

# count number of sessionIds grouped by number of events per sessionId
sids_by_events_count = {}
for sid, events_count in events_by_sid.items():
    if events_count not in sids_by_events_count:
        sids_by_events_count[events_count] = 1
    else:
        sids_by_events_count[events_count] += 1

os.makedirs(output_dir, exist_ok=True)
with open(output_fname, 'w') as f:
    for events_count, sids_count in sorted(sids_by_events_count.items(),
                                     key=itemgetter(0)):
        print('\t'.join([str(events_count), str(sids_count)]), file=f)
