GET_CONTENT_BAITS = """
MATCH (interest) - [:HAS_CONTENT] -> (content:CONTENT) - [pattern_rel:HAS_PATTERN{lemma:$lemma}] -> (:PATTERN{code:'SFC'})
MATCH (content)-[rel_target_word:HAS_WORD{position : pattern_rel.position}]-(target_word:WORD)
WHERE (:USER{id:$user_id}) - [:LIKES] ->(interest)
WITH {
    lemma: pattern_rel.lemma,
    content: {
        id: content.id,
        translation: content.translation,
        source: content.source,
        media_type: content.media_type,
        phrase: content.phrase,
        interest_label: labels(interest)[0]
    },
    interest:interest.name,
    word:target_word.text,
    pos:rel_target_word.pos,
    verbgames_pattern_items:{
                            subject: null,
                            pattern: pattern_rel.pattern,
                            conjugated_auxiliaryverb: null
                            }
} AS content, RAND() AS rnd ORDER BY rnd LIMIT 10

RETURN content LIMIT 1
"""
