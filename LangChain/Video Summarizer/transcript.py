from youtube_transcript_api import YouTubeTranscriptApi

class TranscriptFetcher:
    @staticmethod
    def get_transcript(video_id: str):
        api = YouTubeTranscriptApi()

        transcript = api.fetch(video_id)

        text = " ".join([item.text for item in transcript])
        return text