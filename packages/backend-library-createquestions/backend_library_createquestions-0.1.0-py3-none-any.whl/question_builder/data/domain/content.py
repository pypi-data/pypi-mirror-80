import typing as t
from dataclasses import dataclass
from typing import Optional

@dataclass
class Content:
    id: str
    phrase: str
    media_type: str
    source: str
    interest_label: str
    translation: Optional[str] = None
    

class TwitterContent(Content):
    image_link: str
    tweet_url: str


class GetyarnContent(Content):
    pass

