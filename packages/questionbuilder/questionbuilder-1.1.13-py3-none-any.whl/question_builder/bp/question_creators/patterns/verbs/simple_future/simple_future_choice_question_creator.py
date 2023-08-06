import random
import re

from question_builder.bp.exceptions.dictionary_exceptions import (
    WordNotInRelNounDictionary,
)
from question_builder.bp.exceptions.pos_exceptions import WordNotNoun
from question_builder.bp.question_creators.question_creator import QuestionCreator
from question_builder.bp.questions.question import Question
from question_builder.data import DataQuestion

SUBJECT_KEY = "subject"
PATTERN_KEY = "pattern"
AUXILIARYVERB_KEY = "conjugated_auxiliaryverb"
WILL = "will"
WOULD = "would"
SHOULD = "should"
CAN = "can"
COULD = "could"
N_BAITS = 3


class SimpleFutureChoiceQuestionCreator(QuestionCreator):

    code = "SFC"
    baits_code = "nosfc"

    def create(self, data_question: DataQuestion, user_id):

        content = data_question.content
        target_lemma = data_question.target_lemma
        target_word = data_question.target_word

        verbgames_pattern_items = data_question.verbgames_pattern_items
        pattern = verbgames_pattern_items[PATTERN_KEY]

        question = Question()
        question.content_id = content.id
        question.target_word = target_word
        question.target_lemma = target_lemma
        question.links, question.media_types = self._get_links_and_media_types(content)
        question.correct_answer = WILL
        question.baits = self._get_baits()
        question.options = self._get_options(question.correct_answer, question.baits)
        question.phrase = self._get_phrase(content.phrase, pattern)
        question.original_phrase = content.phrase
        question.phrase_translation = self._get_translation(content)
        question.question_type = self.code
        question.baits_type = self.baits_code
        return question

    def _get_baits(self):
        return random.sample([WOULD, SHOULD, CAN, COULD], N_BAITS)

    def _get_phrase(self, original_phrase, pattern):
        redata = re.compile("('ll|will)", re.IGNORECASE)
        phrase = redata.sub("_____", pattern)

        redata = re.compile(re.escape(pattern), re.IGNORECASE)
        phrase = redata.sub(phrase, original_phrase)

        phrase = self._clean_phrase(phrase)
        return phrase
