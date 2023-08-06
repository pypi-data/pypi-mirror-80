import random
import re

from question_builder.bp.question_creators.question_creator import QuestionCreator
from question_builder.bp.questions.question import Question
from question_builder.data import DataQuestion

PATTERN_KEY = "pattern"
SUBJECT_KEY = "subject"
AUXILIARYVERB_KEY = "conjugated_auxiliaryverb"
LEMMA_CONJUGATIONS = "lemma_conjugations"
VBD = "VBD"
VBG = "VBG"
WILL = "will"
AWILL = "'ll"
N_BAITS = 2


class SimpleFutureChoiceTwoQuestionCreator(QuestionCreator):

    code = "SFC2"
    baits_code = "nosfc2"

    def create(self, data_question: DataQuestion, user_id):

        content = data_question.content
        target_lemma = data_question.target_lemma
        target_word = data_question.target_word

        verbgames_pattern_items = data_question.verbgames_pattern_items
        pattern = verbgames_pattern_items[PATTERN_KEY]
        subject = verbgames_pattern_items[SUBJECT_KEY]

        lemma_conjugations = verbgames_pattern_items[LEMMA_CONJUGATIONS]
        verb_past = lemma_conjugations[VBD]
        verb_present_continuous = lemma_conjugations[VBG]

        question = Question()
        question.content_id = content.id
        question.target_word = target_word
        question.target_lemma = target_lemma
        question.links, question.media_types = self._get_links_and_media_types(content)
        question.correct_answer = pattern.replace(subject, "").strip()
        question.baits = self._get_baits(pattern, verb_past, verb_present_continuous)
        question.options = self._get_options(question.correct_answer, question.baits)
        question.phrase = self._get_phrase(
            content.phrase, subject, target_lemma, pattern
        )
        question.original_phrase = content.phrase
        question.phrase_translation = self._get_translation(content)
        question.question_type = self.code
        question.baits_type = self.baits_code
        return question

    def _get_baits(self, pattern, verb_past, verb_present_continuous):
        auxiliary_verb = self._get_auxiliary_verb(pattern)

        return random.sample(
            [
                f"{auxiliary_verb} {verb_past}",
                f"{auxiliary_verb} {verb_present_continuous}",
            ],
            2,
        )

    def _get_phrase(self, original_phrase, subject, target_lemma, pattern):
        pattern = pattern.replace(subject, "")
        redata = re.compile(re.escape(pattern), re.IGNORECASE)
        phrase = redata.sub("_" * len(pattern), original_phrase)
        return phrase

    def _get_auxiliary_verb(self, pattern):
        if WILL in pattern:
            return f" {WILL}"
        elif AWILL in pattern:
            return f"{AWILL}"
