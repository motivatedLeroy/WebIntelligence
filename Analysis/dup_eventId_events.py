#!/usr/bin/env python3
# Searches for all events with duplicate eventIds and prints them to
# dup_eventId_events.txt if found

import json
from operator import itemgetter
import os

input_fname = 'one_week/20170101'
output_dir = 'results/'
dup_event_ids_fname = output_dir + 'dup_eventIds.txt'
output_fname = output_dir + 'dup_eventId_events.txt'

dup_event_ids = set()
with open(dup_event_ids_fname) as f:
    for line in f:
        dup_event_ids.add(int(line))

dup_event_id_events = []
with open(input_fname) as f:
    for line in f:
        obj = json.loads(line.strip())
        event_id = obj['eventId']
        if event_id in dup_event_ids:
            dup_event_id_events.append((event_id, line))

os.makedirs(output_dir, exist_ok=True)
with open(output_fname, 'w') as f:
    for event_id, line in sorted(dup_event_id_events, key=itemgetter(0)):
        print('{}\t\t{}'.format(event_id, line), end='', file=f)

print(len(dup_event_id_events), 'event(s) with duplicate eventIds found.')

