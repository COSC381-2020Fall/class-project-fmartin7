import pprint
import  json
from googleapiclient.discovery import build
import config

my_api_key = config.my_api_key  # The API_KEY I acquired
my_cse_id = config.my_cse_id # The search engine ID I created
my_search_topic = 'kobe bryant' # The phrase I want to search in nba

def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res['items']

if __name__ == '__main__':
    total_page_number = 10
    results = []

for page_number in range(total_page_number):
    current_result = google_search(my_search_topic, my_api_key, my_cse_id, num=10, start=page_number*10+1)
    results += current_result
print(len(results))
pprint.pprint(results)