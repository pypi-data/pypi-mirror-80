import enum

CONTENT_KEY = "content"
INTEREST_KEY = "interest"
WORD_KEY = "word"
LEMMA_KEY = "lemma"
SOURCE_KEY = "source"
GETYARN_KEY = "getyarn"
TWITTER_KEY = "twitter"
ID_KEY = "id"
POS_KEY = "pos"
TAG_KEY = "tag"
PHRASE_KEY = "phrase"
TRANSLATION_KEY = "translation"
IMAGE_LINK_KEY = "image_link"
MEDIA_TYPE_KEY = "media_type"
TWEET_URL_KEY = "tweet_url"

TEXT = "text"
N_INTEREST_TYPES = 3
MASTERED_KEY = "mastered"
LEVEL_KEY = "level"
CONTENT_LIST_KEY = "content_list"
VERBGAMES_ITEMS_KEY = "verbgames_pattern_items"
LEMMA_CONJUGATIONS_KEY = "lemma_conjugations"
DEFAULT_N_QUESTIONS_PER_INTEREST_TYPE = 3
DEFAULT_N_QUESTIONS = 1

Q_VARIABLE_KEY = "qu"


class QuestionMode(enum.Enum):
    N_QUESTIONS_MODE = 1
    N_QUESTIONS_PER_WORD_MODE = 2
