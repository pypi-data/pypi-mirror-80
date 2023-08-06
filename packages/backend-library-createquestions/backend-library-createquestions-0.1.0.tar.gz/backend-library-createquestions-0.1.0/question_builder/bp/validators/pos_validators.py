VERB = "VERB"
AUX = "AUX"
NOUN = "NOUN"
PRON = "PRON"
PROPN = "PROPN"
ADJ = "ADJ"
ADV = "ADV"


def is_verb(pos: str) -> bool:
    return pos == VERB


def is_auxiliar(pos: str) -> bool:
    return pos == AUX


def is_noun(pos: str) -> bool:
    return pos == NOUN or pos == PROPN or pos == PRON


def is_adjective(pos: str) -> bool:
    return pos == ADJ


def is_adverb(pos: str) -> bool:
    return pos == ADV
