from .. import config
from .content import GetyarnContent
from .content import TwitterContent
from .data_question import DataQuestion


def to_content(content_rel_json):
    content_json = content_rel_json[config.CONTENT_KEY]
    source = content_json[config.SOURCE_KEY]
    if source == config.GETYARN_KEY:
        content = GetyarnContent(
            content_json[config.ID_KEY],
            content_json[config.PHRASE_KEY],
            content_json[config.TRANSLATION_KEY],
            content_json[config.MEDIA_TYPE_KEY],
            content_json[config.SOURCE_KEY],
        )
    elif source == config.TWITTER_KEY:
        content = TwitterContent(
            content_json[config.ID_KEY],
            content_json[config.IMAGE_LINK_KEY],
            content_json[config.PHRASE_KEY],
            content_json[config.MEDIA_TYPE_KEY],
            content_json[config.TWEET_URL_KEY],
            content_json[config.SOURCE_KEY],
        )
    return content


def to_question(content_rel_json):
    content = to_content(content_rel_json)
    interest = content_rel_json[config.INTEREST_KEY]
    target_lemma = content_rel_json[config.LEMMA_KEY]
    target_word = content_rel_json[config.WORD_KEY]
    pos = content_rel_json[config.POS_KEY]
    return DataQuestion(content, interest, target_lemma, target_word, pos)


def to_verb_question(content_rel_json):
    content = to_content(content_rel_json)
    interest = content_rel_json[config.INTEREST_KEY]
    target_lemma = content_rel_json[config.LEMMA_KEY]
    target_word = content_rel_json[config.WORD_KEY]
    pos = content_rel_json[config.POS_KEY]
    verbgames_pattern_items = None
    if config.VERBGAMES_ITEMS_KEY in content_rel_json:
        verbgames_pattern_items = content_rel_json[config.VERBGAMES_ITEMS_KEY]
    return DataQuestion(
        content, interest, target_lemma, target_word, pos, None, verbgames_pattern_items
    )
