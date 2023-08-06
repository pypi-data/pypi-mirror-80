GET_N_DATA_QUESTIONS_PER_WORD = """
UNWIND $lemma_list as lemma

CALL apoc.cypher.run("

    MATCH (interest) - [:HAS_CONTENT] -> (content:CONTENT) - [pattern_rel:HAS_PATTERN{lemma:{lemma}}] -> (:PATTERN{code:\\"PCC\\"})
    MATCH (content)-[:HAS_WORD{position : pattern_rel.position - 4}]-(subject:WORD)
    MATCH (content)-[:HAS_WORD{position : pattern_rel.position - 3}]-(auxiliaryverb1:WORD)
    MATCH (content)-[:HAS_WORD{position : pattern_rel.position - 2}]-(auxiliaryverb2:WORD)
    MATCH (content)-[:HAS_WORD{position : pattern_rel.position - 1}]-(auxiliaryverb3:WORD)
    MATCH (content)-[rel_target_word:HAS_WORD{position : pattern_rel.position}]-(target_word:WORD)
    WHERE (:USER{id:{user_id}}) - [:LIKES] ->(interest)
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
                                subject: subject.text,
                                pattern: pattern_rel.pattern,
                                conjugated_auxiliaryverb: auxiliaryverb1.text
                                }
    } AS content, RAND() AS rnd LIMIT 10

    RETURN content LIMIT {n_questions_per_word}

", {user_id: $user_id, lemma: lemma, n_questions_per_word: $n_questions_per_word}) YIELD value

RETURN value.content as content
"""

GET_N_DATA_QUESTIONS = """
MATCH (interest) - [:HAS_CONTENT] -> (content:CONTENT) - [pattern_rel:HAS_PATTERN] -> (:PATTERN{code:'PCC'})
MATCH (content)-[:HAS_WORD{position : pattern_rel.position - 4}]-(subject:WORD)
MATCH (content)-[:HAS_WORD{position : pattern_rel.position - 3}]-(auxiliaryverb1:WORD)
MATCH (content)-[:HAS_WORD{position : pattern_rel.position - 2}]-(auxiliaryverb2:WORD)
MATCH (content)-[:HAS_WORD{position : pattern_rel.position - 1}]-(auxiliaryverb3:WORD)
MATCH (content)-[rel_target_word:HAS_WORD{position: pattern_rel.position}]-(target_word:WORD)
WHERE (:USER{id:{user_id}}) - [:LIKES] ->(interest) AND pattern_rel.lemma in {lemma_list}
WITH {
    lemma:pattern_rel.lemma,
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
							subject: subject.text,
							pattern: pattern_rel.pattern,
							conjugated_auxiliaryverb: auxiliaryverb1.text
							}
} AS content, RAND() AS rnd ORDER BY rnd LIMIT 50

RETURN content LIMIT $n_questions
"""
