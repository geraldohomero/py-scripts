import json
import csv

input_path = 'Videos_202508261525_clean.json'
output_path = 'videos.csv'

CHANNEL_NAMES = {
    'channelId': 'channelName',
    'channelId': 'channelName'
}

def get_channel_name(channel_id):
    return CHANNEL_NAMES.get(channel_id, channel_id)

with open(input_path, 'r', encoding='utf-8') as f:
    data = json.load(f)


rows = []
for video in data.get('Videos', []):
    video_id = video.get('videoId')
    channel_id = video.get('channelId')
    video_title = video.get('videoTitle', '')
    if video_id and channel_id:
        link = f'https://www.youtube.com/watch?v={video_id}'
        channel_name = get_channel_name(channel_id)
        rows.append([link, video_title, channel_name, channel_id])

with open(output_path, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['YouTube Link', 'Video Title', 'Channel Name', 'ChannelId'])
    writer.writerows(rows)

print(f'Arquivo CSV gerado: {output_path}')
