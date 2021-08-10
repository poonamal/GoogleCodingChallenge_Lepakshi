from video import Video
from pathlib import Path
from typing import Sequence, Optional
import csv
import random

def _csv_reader_with_strip(reader):
    yield from ((item.strip() for item in line) for line in reader)

class VideoLibrary:

    def __init__(self):
        self._videos = {}
        with open(Path(__file__).parent / "videos.txt") as video_file:
            reader = _csv_reader_with_strip(
                csv.reader(video_file, delimiter="|"))
            for video_info in reader:
                title, url, tags = video_info
                self._videos[url] = Video(
                    title,
                    url,
                    [tag.strip() for tag in tags.split(",")] if tags else [],
                )

    def get_all_videos(self):
        return list(self._videos.values())

    def get_video(self, video_id):
        return self._videos.get(video_id, None)
    
    def get_allowed_videos(self) -> Sequence[Video]:
        return [v for v in self.get_all_videos() if not v.is_flagged]

    def __getitem__(self, video_id):
        return self._videos[video_id]
    def get_random_video_id(self) -> Optional[str]:
        return random.choice([video.video_id for video in self.get_allowed_videos()])

    def search_videos(self, search_term: str):
        search_term = search_term.lower()
        for v in self.get_allowed_videos():
            return [v for v in self.get_allowed_videos() if search_term in v.title.lower()]

    def get_videos_with_tag(self, tag: str):
        return [v for v in self.get_allowed_videos() if tag in v.tags]