GET_LEMMA_LIST_DATA = """
MATCH (lemma:LEMMA)
MATCH (user:USER{id:$user_id})
WHERE lemma.text in $lemma_list
OPTIONAL MATCH (lemma) -[:HAS_LEMMA{tag:"VBG"}]-(verb_vbg:WORD)
WITH user, lemma, {VBG: coalesce(collect(verb_vbg.text)[0], 'N/A')} as lemma_conjugations
OPTIONAL MATCH (user) -[has_seen:HAS_SEEN] -(lemma)
RETURN lemma.text as lemma, coalesce(has_seen.level, 1) as level, coalesce(has_seen.mastered, False) as mastered, lemma_conjugations
"""
