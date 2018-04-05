#!/usr/bin/env python3
# Searches for duplicate eventIds and prints them to dup_eventIds.txt if found

import json
import os

input_fname = 'one_week/20170101'
output_dir = 'results/'
output_fname = output_dir + 'dup_eventIds.txt'

event_ids = set()
dup_event_ids = set()
with open(input_fname) as f:
    for line in f:
        obj = json.loads(line.strip())
        event_id = obj['eventId']
        if event_id not in event_ids:
            event_ids.add(event_id)
        elif event_id not in dup_event_ids:
            dup_event_ids.add(event_id)

os.makedirs(output_dir, exist_ok=True)
with open(output_fname, 'w') as f:
    for event_id in sorted(dup_event_ids):
        print(event_id, file=f)

print(len(dup_event_ids), 'duplicate eventId(s) found.')
