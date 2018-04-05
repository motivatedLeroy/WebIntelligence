import json

input_file = 'one_week/20170102'
output_fname = 'dataset.txt'

with open(output_fname, 'w') as f:
    for line in open(input_file):
        obj = json.loads(line.strip())
        try:
            uid, iid, activeTime = obj['userId'], obj['id'], obj['activeTime']
        except Exception as e:
            continue
        print('\t'.join([uid, iid, str(activeTime)]), file=f)
