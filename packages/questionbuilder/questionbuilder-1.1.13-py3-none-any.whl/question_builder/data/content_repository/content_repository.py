import logging
from collections import defaultdict
from collections import namedtuple

from . import queries
from .. import config
from ..domain.data_converters import to_content
from ..domain.data_converters import to_question
from ..domain.data_converters import to_verb_question
from ..domain.lemma_data import LemmaData


class ContentRepository:
    """
    Handles all the db operations related to user content management
    """

    def __init__(self, driver):
        """
        Initializes the neo4j db
        """
        self._driver = driver

    def get_lexemas_from_lemma(self, lemma):
        lexemas = []
        with self._driver.session() as session:
            for res in session.read_transaction(self._get_lexemas_from_lemma, lemma):
                lexemas.append(res[0])
        return lexemas

    @staticmethod
    def _get_lexemas_from_lemma(tx, lemma):
        query = queries.GET_LEXEMAS_FROM_LEMMA
        return tx.run(query, lemma=lemma)

    def get_random_questions_by_pos_without_lexemas(
        self, pos_lemma_list, user_id, n_questions
    ):
        lemma_to_question = defaultdict()
        with self._driver.session() as session:
            for res in session.read_transaction(
                self._get_random_questions_by_pos_without_lexemas,
                pos_lemma_list,
                user_id,
                n_questions,
            ):
                target_lemma = res[config.WORD_KEY][config.TEXT]
                content_rel_json = res[config.CONTENT_KEY]
                content_rel_json[config.LEMMA_KEY] = target_lemma
                lemma_to_question[target_lemma] = to_question(content_rel_json)
        return lemma_to_question

    @staticmethod
    def _get_random_questions_by_pos_without_lexemas(
        tx, pos_lemma_list, user_id, n_questions
    ):
        query = queries.GET_USER_RANDOM_QUESTIONS_WITH_CONTENT_BY_POS_WITHOUT_LEXEMAS
        return tx.run(
            query,
            pos_lemma_list=pos_lemma_list,
            user_id=user_id,
            n_questions=int(n_questions / config.N_INTEREST_TYPES),
        )

    def get_random_questions_by_pos(self, pos_lemma_list, user_id, n_questions):
        lemma_to_question = defaultdict()
        with self._driver.session() as session:
            for res in session.read_transaction(
                self._get_random_questions_by_pos, pos_lemma_list, user_id, n_questions
            ):
                target_lemma = res[config.WORD_KEY][config.TEXT]
                content_rel_json = res[config.CONTENT_KEY]
                content_rel_json[config.LEMMA_KEY] = target_lemma
                lemma_to_question[target_lemma] = to_question(content_rel_json)
        return lemma_to_question

    @staticmethod
    def _get_random_questions_by_pos(tx, pos_lemma_list, user_id, n_questions):
        query = queries.GET_USER_RANDOM_QUESTIONS_WITH_CONTENT_BY_POS
        return tx.run(
            query,
            pos_lemma_list=pos_lemma_list,
            user_id=user_id,
            n_questions=int(n_questions / config.N_INTEREST_TYPES),
        )

    def get_random_questions(
        self, lemma_list, user_id, n_questions, n_questions_per_word
    ):
        lemma_to_questions = defaultdict(list)
        with self._driver.session() as session:
            for res in session.read_transaction(
                self._get_random_questions,
                user_id,
                lemma_list,
                n_questions,
                n_questions_per_word,
            ):
                target_lemma = res[config.LEMMA_KEY]
                content_rel_json = res[config.CONTENT_KEY]
                content_rel_json[config.LEMMA_KEY] = target_lemma
                mastered = res[config.MASTERED_KEY]
                level = res[config.LEVEL_KEY]
                mastered = mastered if mastered else False
                level = level if level else 1
                lemma_to_questions[target_lemma].append(
                    LemmaData(to_question(content_rel_json), level, mastered)
                )
        return lemma_to_questions

    @staticmethod
    def _get_random_questions(
        tx, user_id, word_list, n_questions, n_questions_per_word
    ):
        query = queries.GET_USER_RANDOM_QUESTIONS_WITH_CONTENT
        return tx.run(
            query,
            user_id=user_id,
            lemma_list=word_list,
            n_questions=int(n_questions / config.N_INTEREST_TYPES),
            n_questions_per_word=n_questions_per_word,
        )

    def get_random_questions_paginated(
        self, lemma_list, user_id, page, max_items_per_page
    ):
        question_list = []
        with self._driver.session() as session:
            for res in session.read_transaction(
                self._get_random_questions_paginated,
                lemma_list,
                user_id,
                page,
                max_items_per_page,
            ):
                for content_rel_json in res[config.CONTENT_LIST_KEY]:
                    question_list.append(to_question(content_rel_json))
        return page, question_list

    @staticmethod
    def _get_random_questions_paginated(
        tx, lemma_list, user_id, page, max_items_per_page
    ):
        n_questions = int(max_items_per_page / len(lemma_list))
        query = queries.GET_USER_RANDOM_QUESTIONS_WITH_CONTENT_PAGINATED
        return tx.run(
            query,
            lemma_list=lemma_list,
            user_id=user_id,
            start=page * n_questions,
            n_questions=n_questions,
        )

    def get_question(self, user_id, lemma_list):
        with self._driver.session() as session:
            for res in session.read_transaction(
                self._get_random_question, user_id, lemma_list
            ):
                content_rel_json = res[config.Q_VARIABLE_KEY]
                question = to_question(content_rel_json)
                return question

    @staticmethod
    def _get_random_question(tx, user_id, lemma_list):
        query = queries.GET_QUESTION_FROM_USER
        results = tx.run(query, user_id=user_id, lemma_list=lemma_list)
        return results
