from typing import Optional, List, Dict

ID = "id"
MEDIA = "media"
MEDIA_TYPE = "mediaType"
MEDIA_LINK = "link"
PHRASE = "phrase"
ORIGINAL_PHRASE = "originalphrase"
TRANSLATION_KEY = "phrase_translation"
QUESTION_TYPE = "questiontype"
OPTIONS = "options"
LEVEL = "level"
IS_LAST_LEVEL = "lastlevel"
TARGET_LEMMA = "targetlemma"
MASTERED = "mastered"
CORRECT = "correct"
N_BAITS = 3
GETYARN_KEY = "getyarn"
TWITTER_KEY = "twitter"
VIDEO = "video"
IMAGE = "image"
TEXT = "text"
INSTRUCTIONS = "instructions"


class Question:
    def __init__(self):
        self.content_id: Optional[str] = None
        self.target_lemma: Optional[str] = None
        self.links: Optional[List[str]] = None
        self.media_types: Optional[List[str]] = None
        self.options: Optional[List[Dict]] = None
        self.phrase: Optional[str] = None
        self.original_phrase: Optional[str] = None
        self.phrase_translation: Optional[str] = None
        self.question_type: Optional[str] = None
        self.baits_type: Optional[str] = None
        self.level_to_master: Optional[int] = 1
        self.level: Optional[int] = 1
        self.mastered: Optional[bool] = False
        self.instructions: Optional[str] = ""

    def __repr__(self):
        return "Question({})".format(self.id)

    @property
    def id(self) -> str:
        return "{}_{}_{}_{}_{}".format(
            self.content_id,
            self.target_lemma,
            self.target_word,
            self.question_type,
            self.baits_type,
        )

    @property
    def is_last_level(self) -> bool:
        return self.level >= self.level_to_master

    def to_json(self) -> Dict:
        question = {
            ID: self.id,
            MEDIA: [
                {MEDIA_TYPE: media_type, MEDIA_LINK: link}
                for media_type, link in zip(self.media_types, self.links)
            ],
            PHRASE: self.phrase,
            ORIGINAL_PHRASE: self.original_phrase,
            TRANSLATION_KEY: self.phrase_translation,
            OPTIONS: self.options,
            QUESTION_TYPE: self.question_type,
            LEVEL: self.level,
            IS_LAST_LEVEL: self.is_last_level,
            TARGET_LEMMA: self.target_lemma,
            MASTERED: self.mastered,
            INSTRUCTIONS: self.instructions
        }
        return question
