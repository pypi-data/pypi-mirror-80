from .content import Content
from typing import Optional, Dict

class DataQuestion:
    def __init__(
        self,
        content: Content,
        interest: str,
        target_lemma: str,
        target_word: str,
        pos: str,
        tag: Optional[str] = None,
        verbgames_pattern_items: Optional[Dict[str, str]] = None,
        bait_content: Optional[Content] = None, 
        pair_content: Optional[Content] = None,
    ):
        self.content = content
        self.interest = interest
        self.target_lemma = target_lemma
        self.target_word = target_word
        self.pos = pos
        self.tag = tag
        self.verbgames_pattern_items = verbgames_pattern_items
        self.bait_content = bait_content
        self.pair_content = pair_content

    def __repr__(self):
        return "DataQuestion({}, {} , {} , {} , {} , {} , {} )".format(
            self.content,
            self.target_lemma,
            self.target_word,
            self.pos,
            self.tag,
            self.verbgames_pattern_items,
            self.bait_content.id if self.bait_content else None,
        )
