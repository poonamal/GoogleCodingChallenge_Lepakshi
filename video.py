from typing import Sequence
class Video:
    def __init__(self, video_title: str, video_id: str, video_tags: Sequence[str]):
        """Video constructor."""
        self._title = video_title
        self._video_id = video_id
        self._tags = tuple(video_tags)
        self._flag_reason = None

    @property
    def video_id(self) -> str:
        return self._video_id

    @property
    def tags(self) -> Sequence[str]:
        return self._tags
    
    def __str__(self):
        result = f'{self.title} ({self.video_id}) [{self.tags_string}]'
        if self.is_flagged:
            result += f' - FLAGGED {self.formatted_flag_reason}'
        return result

    @property
    def tags_string(self) -> str:
        return ' '.join(self.tags)

    def flag(self, flag_reason: str):
        self._flag_reason = flag_reason

    def unflag(self):
        self._flag_reason = None
        
    @property
    def title(self) -> str:
        return self._title
        
    def check_allowed(self):
        if self.is_flagged:
            print("Video is currently flagged", self.formatted_flag_reason)

    @property
    def is_flagged(self):
        return self._flag_reason is not None

    @property
    def formatted_flag_reason(self):
        if self.is_flagged:
            return ("reason:", self._flag_reason)
        else:
            return ''