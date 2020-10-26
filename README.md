# COSC381 Fall 2020 Project #
## Setup ##
1. Install the packages necessary: `python3 -m install -r requirements.txt`
2. Add your own API key to `config.py`
## Get Your Search Results ##
1. Run `python3 cse.py` with the search term of your choice as the arguement.
## Preparing Your Data for Indexing ##
1. Run `bash download_youtube_data_batch.sh` to create a folder of json files for the video ids in video_ids.txt
## Preparing for Whoosh Index
1. Run `python3 create_data_for_indexing.py` to prepare for Whoosh index.
## Create Whoosh Indexing 
1. Run `python3 create_whoosh_index.py` to create whoosh index.
## Query on Whoosh
1. Run `python3 query_on_whoosh.py home 2 1`. Outputs result in json format.
