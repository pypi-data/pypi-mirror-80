from youtube_transcript_api import (
    YouTubeTranscriptApi as Api,
    TranscriptsDisabled,
    NoTranscriptFound,
    CouldNotRetrieveTranscript,
    VideoUnavailable,
    NotTranslatable,
    TranslationLanguageNotAvailable,
    NoTranscriptAvailable,
    CookiePathInvalid,
    CookiesInvalid
)

class Extractor:
    def __init__(self, videi_id, callback=None):
        self.video_id = videi_id
        self.callback = callback

    def extract(self) -> dict:
        try:
            transcript_list = Api.list_transcripts(self.video_id)
            for transcript in transcript_list:
                # transcripts = Api.get_transcript(self.video_id)
                return transcript.fetch()
        except (TranscriptsDisabled,
                NoTranscriptFound,
                CouldNotRetrieveTranscript,
                VideoUnavailable,
                NotTranslatable,
                TranslationLanguageNotAvailable,
                NoTranscriptAvailable) as e:
                print("Transcripts unavailable.")
                return [{"error": 1}]
        except (CookiePathInvalid, CookiesInvalid) as e:
                print("Cookie error.")
                return [{"error": 2}]