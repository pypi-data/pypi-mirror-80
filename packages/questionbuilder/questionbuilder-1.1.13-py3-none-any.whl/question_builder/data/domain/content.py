import typing as t


class TwitterContent(t.NamedTuple):
    id: str
    image_link: str
    phrase: str
    media_type: str
    tweet_url: str
    source: str


class GetyarnContent(t.NamedTuple):
    id: str
    phrase: str
    translation: str
    media_type: str
    source: str
