import pprint
import sys
import json
from googleapiclient.discovery import build
import config

my_api_key = config.my_api_key # The API_KEY I acquired

def youtube_data(video_id):
    service = build("youtube", "v3", developerKey=my_api_key)
    result = service.videos().list(part='snippet', id=video_id).execute()
    return result

if __name__ == '__main__':
    vidId = sys.argv[1]
    result = youtube_data(vidId)
    #pprint.pprint(result)
    with open(vidId+'.json', 'w') as dump_file:
        json.dump(result, dump_file)