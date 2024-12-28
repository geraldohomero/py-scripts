from youtube_transcript_api import YouTubeTranscriptApi

video_id = 'id'

transcript = YouTubeTranscriptApi.get_transcript(video_id=video_id)

# Armazenar a transcrição em um arquivo de texto sem timestamps
with open('transcript.txt', 'w') as file:
    for entry in transcript:
        file.write(f"{entry['text']}\n")