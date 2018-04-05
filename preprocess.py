import json

output_fname = 'dataset.txt'

input_file = 'one_week/20170102'

print('>>> Start reading file...')
with open(output_fname, 'w') as f:
    count = 0
    for line in open(input_file):
        obj = json.loads(line.strip())
        try:
            uid, iid, activeTime = obj['userId'], obj['id'], str(obj['activeTime'])
        except Exception as e:
            continue
        print('\t'.join([uid, iid, activeTime]), file=f)
        count += 1
        #if count >= 10000:
        #    break
print('>>> Done!')
