from pathlib import Path
import json
import pprint

paths = [str(x) for x in Path('./youtube_data').glob('**/*.json')]
results = []
for path in paths:
    with open(path, 'r') as f:
        data = json.load(f)
        # insert your code here
        videoInfo = {
        'id': data['items'][0]['id'],
        'title': data['items'][0]['snippet']['title'],
        'description': data['items'][0]['snippet']['description']
        }
        results.append(videoInfo)

with open('data_for_indexing.json', 'w') as dump_file:
    json.dump(results, dump_file)
