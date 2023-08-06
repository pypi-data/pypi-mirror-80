GET_USER_RANDOM_QUESTIONS_WITH_CONTENT = """
UNWIND $lemma_dict_list as lemma_dict
MATCH (user:USER{id:$user_id})
MATCH (interest) - [:HAS_LEMMA]-> (lemma:LEMMA)
WHERE (user) - [:LIKES] -> (interest) AND lemma.text = lemma_dict.lemma
OPTIONAL MATCH (user) -[has_seen:HAS_SEEN] -(lemma)
WITH DISTINCT lemma.text AS lemma, lemma_dict.pair as pair, has_seen.level AS level, has_seen.mastered AS mastered

WITH lemma, pair, level, mastered

CALL apoc.cypher.run("

    MATCH (interest) - [:HAS_CONTENT] -> (content:CONTENT) - [has_word:HAS_WORD] -> (word:WORD)-[:HAS_LEMMA]->(:LEMMA{text:{lemma}})       
    WHERE (:USER{id:{user_id}}) - [:LIKES] -> (interest)
    WITH interest, content, has_word, word, RAND() AS rnd LIMIT {n_questions}

    WITH interest, content, has_word, word ORDER BY rnd LIMIT 1
    MATCH (interest) - [:HAS_CONTENT] -> (bait_content:CONTENT) - [has_word_:HAS_WORD] -> (word_:WORD)
    WHERE has_word_.lemma <> {lemma}
	
    WITH interest, content, bait_content, has_word, word LIMIT 1
	OPTIONAL MATCH (pair_word:WORD{text:{pair}})
    OPTIONAL MATCH (interest) - [:HAS_CONTENT] -> (pair_content:CONTENT) - [:HAS_WORD] -> (pair_word)
    
    RETURN {
            content: {
                id: content.id,
                translation: content.translation,
                source: content.source,
                media_type: content.media_type,
                phrase: content.phrase,
                interest_label: labels(interest)[0]
            }, 
            bait_content: {
                id: bait_content.id,
                translation: bait_content.translation,
                source: bait_content.source,
                media_type: bait_content.media_type,
                phrase: bait_content.phrase,
                interest_label: labels(interest)[0]
            }, 
            pair_content: {
                id: pair_content.id,
                translation: pair_content.translation,
                source: pair_content.source,
                media_type: pair_content.media_type,
                phrase: pair_content.phrase,
                interest_label: labels(interest)[0]
            },  
            lemma:{lemma}, 
            interest: interest.name, 
            word: word.text, 
            pos: has_word.pos
            } as content LIMIT 1

    ", {user_id: $user_id, lemma: lemma, pair: pair, n_questions: $n_questions, n_questions_per_word: $n_questions_per_word}) YIELD value
RETURN lemma, value.content AS content, level, mastered
"""


GET_USER_RANDOM_QUESTIONS_WITH_CONTENT_PAGINATED = """
MATCH (interest) - [:HAS_CONTENT] -> (content:CONTENT) - [has_word:HAS_WORD] -> (word:WORD) -[:HAS_LEMMA]-> (lemma_:LEMMA)
WHERE (:USER{id:{user_id}}) - [:LIKES] -> (interest) and lemma_.text in $lemma_list

WITH interest, content, has_word, word, lemma_, RAND() AS rnd SKIP {start} LIMIT {n_questions}

WITH {
        content: {
            id: content.id,
            translation: content.translation,
            source: content.source,
            media_type: content.media_type,
            phrase: content.phrase,
            interest_label: labels(interest)[0]
        }, 
        bait_content: null, 
        pair_content: null, 
        lemma:lemma_.text, 
        interest: interest.name, 
        word: word.text, 
        pos: has_word.pos
    } AS content ORDER BY rnd

RETURN content.lemma as lemma, collect(content) AS content_list"""


GET_QUESTION_FROM_USER = """
UNWIND $lemma_list AS lemma

CALL apoc.cypher.run("

    MATCH (user:USER{id:{user_id}})
	MATCH (interest) - [:HAS_CONTENT] -> (content:CONTENT) - [has_word:HAS_WORD] -> (word_:WORD) - [:HAS_LEMMA] -> (lemma_:LEMMA{text:{lemma}})
	WHERE (user) -[:LIKES] -> (interest)
	RETURN {
        content: {
            id: content.id,
            translation: content.translation,
            source: content.source,
            media_type: content.media_type,
            phrase: content.phrase,
            interest_label: labels(interest)[0]
        }, 
        bait_content: null, 
        pair_content: null, 
        lemma:lemma_.text,
        interest:interest.name,
        word:word_.text,
        pos:has_word.pos
    } AS content LIMIT 10

    ", {lemma:lemma, user_id: $user_id}) YIELD value
RETURN value.content AS qu LIMIT 1
"""


GET_USER_RANDOM_QUESTIONS_WITH_CONTENT_BY_POS = """
UNWIND $pos_lemma_list AS pos_lemma
CALL apoc.cypher.run("

    CALL apoc.cypher.run('

        MATCH (interest) - [:HAS_CONTENT] -> (content:CONTENT) - [has_word:HAS_WORD{pos:{pos_lemma}.pos}] -> (word:WORD) -[:HAS_LEMMA]-(lemma:LEMMA{text:{pos_lemma}.text})
        WHERE (:USER{id:{user_id}}) - [:LIKES] ->(interest)
        RETURN {
            content: {
                id: content.id,
                translation: content.translation,
                source: content.source,
                media_type: content.media_type,
                phrase: content.phrase,
                interest_label: labels(interest)[0]
            },
            interest:interest.name,
            word:word.text,
            pos:has_word.pos
        } AS content LIMIT {n_questions}

    ', {pos_lemma:{pos_lemma}, user_id:{user_id}, n_questions:{n_questions}}) YIELD value
    WITH pos_lemma, value.content AS content, RAND() AS rnd

    RETURN pos_lemma, content, rnd ORDER BY rnd LIMIT 1

    ", {pos_lemma: pos_lemma, user_id: $user_id, n_questions: $n_questions}) YIELD value
RETURN value.pos_lemma AS word, value.content AS content
"""


GET_USER_RANDOM_QUESTIONS_WITH_CONTENT_BY_POS_WITHOUT_LEXEMAS = """
UNWIND $pos_lemma_list AS pos_lemma
CALL apoc.cypher.run("

    CALL apoc.cypher.run('

        MATCH (interest) - [:HAS_CONTENT] -> (content:CONTENT) - [has_word:HAS_WORD{pos:{pos_lemma}.pos}] -> (word:WORD{text:{pos_lemma}.text})
        WHERE (:USER{id:{user_id}}) - [:LIKES] ->(interest)
        RETURN {
            content: {
                id: content.id,
                translation: content.translation,
                source: content.source,
                media_type: content.media_type,
                phrase: content.phrase,
                interest_label: labels(interest)[0]
            },
            interest:interest.name,
            word:word.text,
            pos:has_word.pos
        } AS content LIMIT {n_questions}

    ', {pos_lemma:pos_lemma, user_id:{user_id}, n_questions:{n_questions}}) YIELD value
    WITH pos_lemma, value.content AS content, RAND() AS rnd

    RETURN pos_lemma, content, rnd ORDER BY rnd LIMIT 1

    ", {pos_lemma: pos_lemma, user_id: $user_id, n_questions: $n_questions}) YIELD value
RETURN value.pos_lemma AS word, value.content AS content
"""


GET_LEXEMAS_FROM_LEMMA = """
MATCH (word:WORD) -[:HAS_LEMMA] -(lemma:LEMMA{text:$lemma})
WHERE word.text <> lemma.text
RETURN word.text
"""
