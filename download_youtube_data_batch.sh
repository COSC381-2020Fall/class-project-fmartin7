#!/usr/bin/bash
mkdir -p ~/youtube_data
cd ~/youtube_data
while read p; do
  python3 ~/download_youtube_data.py $p
  done <~/video_ids.txt                      