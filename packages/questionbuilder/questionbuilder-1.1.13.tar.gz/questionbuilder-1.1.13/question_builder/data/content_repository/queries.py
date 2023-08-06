GET_USER_RANDOM_QUESTIONS_WITH_CONTENT = """
MATCH (user:USER{id:$user_id})
MATCH (interest) - [:HAS_LEMMA]-> (lemma:LEMMA) <- [has_lemma:HAS_LEMMA] - (word:WORD)
WHERE (user) - [:LIKES] -> (interest) AND lemma.text IN $lemma_list
OPTIONAL MATCH (user) -[has_seen:HAS_SEEN] -(lemma)
WITH DISTINCT lemma.text AS lemma, word.text AS word_, has_seen.level AS level, has_seen.mastered AS mastered, RAND() as rand order by rand

WITH lemma, collect(word_)[0] as word, level, mastered

CALL apoc.cypher.run("

    MATCH (interest) - [:HAS_CONTENT] -> (content:CONTENT) - [has_word:HAS_WORD] -> (word_:WORD{text:{word__}})
    WHERE (:USER{id:{user_id}}) - [:LIKES] -> (interest)
    WITH {
            content:content,
            interest:interest.name,
            word:word_.text,
            pos:has_word.pos
        } AS content, word_, RAND() AS rnd ORDER BY rnd LIMIT {n_questions}
	
	RETURN word_.text as word, content LIMIT {n_questions_per_word}

    ", {user_id: $user_id, lemma: lemma, word__: word, n_questions: $n_questions, n_questions_per_word: $n_questions_per_word}) YIELD value
RETURN lemma, value.word AS word, value.content AS content, level, mastered
"""


GET_USER_RANDOM_QUESTIONS_WITH_CONTENT_PAGINATED = """
UNWIND $lemma_list AS lemma

CALL apoc.cypher.run("

    MATCH (interest) - [:HAS_CONTENT] -> (content:CONTENT) - [has_word:HAS_WORD] -> (word:WORD) -[:HAS_LEMMA]-> (lemma_:LEMMA{text:{lemma}})
    WHERE (:USER{id:{user_id}}) - [:LIKES] -> (interest)
    RETURN {
        content:content,
        interest:interest.name,
        word:word.text,
        pos:has_word.pos,
        lemma: lemma_.text
    } AS content SKIP {start} LIMIT {n_questions}

    ", {lemma:lemma, user_id: $user_id, start: $start, n_questions: $n_questions}) YIELD value

RETURN lemma, collect(value.content) AS content_list"""


GET_QUESTION_FROM_USER = """
UNWIND $lemma_list AS lemma

CALL apoc.cypher.run("

    MATCH (user:USER{id:{user_id}})
	MATCH (interest) - [:HAS_CONTENT] -> (content:CONTENT) - [has_word:HAS_WORD] -> (word_:WORD) - [:HAS_LEMMA] -> (lemma_:LEMMA{text:{lemma}})
	WHERE (user) -[:LIKES] -> (interest)
	RETURN {
        content:content,
        interest:interest.name,
        word:word_.text,
        pos:has_word.pos,
        lemma:lemma_.text
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
        RETURN {content:content, interest:interest.name, word:word.text, pos:has_word.pos} AS content LIMIT {n_questions}

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
        RETURN {content:content, interest:interest.name, word:word.text, pos:has_word.pos} AS content LIMIT {n_questions}

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
