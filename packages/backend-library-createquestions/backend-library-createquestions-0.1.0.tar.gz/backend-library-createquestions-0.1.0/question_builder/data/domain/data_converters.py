from .. import config
from .content import GetyarnContent
from .content import TwitterContent
from .content import Content
from .data_question import DataQuestion
from typing import Dict


def to_content(content_json: Dict[str, Dict]) -> Content:
    if(content_json == None):
        return
    source = content_json[config.SOURCE_KEY]
    if source == config.GETYARN_KEY:
        content = GetyarnContent(
            id = content_json[config.ID_KEY],
            phrase = content_json[config.PHRASE_KEY],
            translation = content_json[config.TRANSLATION_KEY],
            media_type = content_json[config.MEDIA_TYPE_KEY],
            source = content_json[config.SOURCE_KEY],
            interest_label = content_json[config.INTEREST_LABEL_KEY],
        )
    elif source == config.TWITTER_KEY:
        content = TwitterContent(
            id = content_json[config.ID_KEY],
            image_link = content_json[config.IMAGE_LINK_KEY],
            phrase = content_json[config.PHRASE_KEY],
            media_type = content_json[config.MEDIA_TYPE_KEY],
            tweet_url = content_json[config.TWEET_URL_KEY],
            source = content_json[config.SOURCE_KEY],
            interest_label = content_json[config.INTEREST_LABEL_KEY],
        )
    return content


def to_question(content_rel_json: Dict) -> DataQuestion:
    content = to_content(content_rel_json[config.CONTENT_KEY])
    bait_content = to_content(content_rel_json[config.CONTENT_BAIT_KEY])
    pair_content = to_content(content_rel_json[config.CONTENT_PAIR_KEY])
    interest = content_rel_json[config.INTEREST_KEY]
    target_lemma = content_rel_json[config.LEMMA_KEY]
    target_word = content_rel_json[config.WORD_KEY]
    pos = content_rel_json[config.POS_KEY]
    return DataQuestion(content, 
                        interest, 
                        target_lemma, 
                        target_word, 
                        pos, 
                        bait_content = bait_content,
                        pair_content = pair_content)


def to_verb_question(content_rel_json: Dict) -> DataQuestion:
    content = to_content(content_rel_json[config.CONTENT_KEY])
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
