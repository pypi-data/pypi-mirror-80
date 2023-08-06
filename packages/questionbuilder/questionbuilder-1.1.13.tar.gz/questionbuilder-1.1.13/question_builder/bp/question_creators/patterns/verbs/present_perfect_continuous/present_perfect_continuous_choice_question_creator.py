import random
import re

from question_builder.bp.exceptions.question_creator_exception import (
    QuestionCreatorException,
)
from question_builder.bp.question_creators.question_creator import QuestionCreator
from question_builder.bp.questions.question import Question
from question_builder.data import DataQuestion

PATTERN_KEY = "pattern"
SUBJECT_KEY = "subject"
VB = "VB"
BEEN = "been"
BEEING = "beeing"
BE = "be"
N_BAITS = 2


class PresentPerfectContinuousChoiceQuestionCreator(QuestionCreator):

    code = "PRPCC"
    baits_code = "noprpcc"

    def create(self, data_question: DataQuestion, user_id):

        content = data_question.content
        target_lemma = data_question.target_lemma
        target_word = data_question.target_word

        verbgames_pattern_items = data_question.verbgames_pattern_items
        pattern = verbgames_pattern_items[PATTERN_KEY]
        subject = verbgames_pattern_items[SUBJECT_KEY]

        question = Question()
        question.content_id = content.id
        question.target_word = target_word
        question.target_lemma = target_lemma
        question.links, question.media_types = self._get_links_and_media_types(content)
        question.correct_answer = pattern
        question.baits = self._get_baits(subject, target_lemma, pattern)
        question.options = self._get_options(question.correct_answer, question.baits)
        question.phrase = self._get_phrase(content.phrase, pattern)
        question.original_phrase = content.phrase
        question.phrase_translation = self._get_translation(content)
        question.question_type = self.code
        question.baits_type = self.baits_code
        question.content_id = content.id
        question.content_id = content.id
        return question

    def _get_baits(self, subject, target_lemma, pattern):
        return random.sample(
            [
                f"{subject} have {BE} {pattern.split()[-1]}",
                f"{subject} having {BEEN} {target_lemma}",
                f"{subject} have {BEEING} {target_lemma}",
                f"{subject} have {BEEN} {target_lemma}",
            ],
            N_BAITS,
        )

    def _get_phrase(self, original_phrase, pattern):
        redata = re.compile(re.escape(pattern), re.IGNORECASE)
        phrase = redata.sub("_" * len(pattern), original_phrase)
        return phrase
