VERB_PAST_TENSE = "VBD"


def verb_is_past(tag: str) -> bool:
    return tag == VERB_PAST_TENSE
