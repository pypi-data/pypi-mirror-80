import random

from question_builder.bp.exceptions.question_creator_exception import (
    QuestionCreatorException,
)
from question_builder.bp.question_creators.question_creator import QuestionCreator
from question_builder.bp.questions.question import Question
from question_builder.data import DataQuestion

SUBJECT_KEY = "subject"
CONJUGATED_VERBTOHAVE_KEY = "conjugated_auxiliaryverb"
NEGATION_ADVERB_KEY = "negation"
TARGET_VERB_CONJUGATIONS_KEY = "targetverb_conjugations"
PRESENT_Continuous_KEY = "VBG"
NOT = "not"
DONT = "don't"
NO = "no"
SAMPLE_N_BAITS = 2


class PresentPerfectNegationChoiceQuestionCreator(QuestionCreator):

    CODE = "PPNC"
    BAITS_CODE = "noppnc"

    def create(self, data_question: DataQuestion, user_id):
        content = data_question.content
        target_lemma = data_question.target_lemma
        target_word = data_question.target_word

        verbgames_pattern_items = data_question.verbgames_pattern_items
        subject = verbgames_pattern_items[SUBJECT_KEY]
        conjugated_verbtohave = verbgames_pattern_items[CONJUGATED_VERBTOHAVE_KEY]
        negation_adverb = verbgames_pattern_items[NEGATION_ADVERB_KEY]
        verbtohave_and_negation_adverb = self._get_combined_verbtohave_and_negation_adverb(
            conjugated_verbtohave, negation_adverb
        )

        target_verb_present_continuous = verbgames_pattern_items[
            TARGET_VERB_CONJUGATIONS_KEY
        ][PRESENT_Continuous_KEY]

        question = Question()
        question.content_id = content.id
        question.target_word = target_word
        question.target_lemma = target_lemma
        question.links, question.media_types = self._get_links_and_media_types(content)
        question.correct_answer = self._get_correct_answer(
            target_word, subject, verbtohave_and_negation_adverb
        )
        question.baits = self._get_baits(
            target_word, subject, conjugated_verbtohave, target_verb_present_continuous
        )
        question.options = self._get_options(question.correct_answer, question.baits)
        question.phrase = self._get_phrase(content.phrase, question.correct_answer)
        question.original_phrase = content.phrase
        question.phrase_translation = self._get_translation(content)
        question.question_type = self.CODE
        question.baits_type = self.BAITS_CODE
        return question

    @staticmethod
    def _get_combined_verbtohave_and_negation_adverb(
        conjugated_verbtohave, negation_adverb
    ):
        if negation_adverb == NOT:
            return f"{conjugated_verbtohave} {negation_adverb}"
        else:
            return f"{conjugated_verbtohave}{negation_adverb}"

    @staticmethod
    def _get_correct_answer(target_verb, subject, verbtohave_and_negation_adverb):
        return f"{subject} {verbtohave_and_negation_adverb} {target_verb}"

    @staticmethod
    def _get_baits(
        target_verb, subject, conjugated_verbtohave, target_verb_present_continuous
    ):
        return random.sample(
            [
                f"{subject} {DONT} {conjugated_verbtohave} {target_verb_present_continuous}",
                f"{subject} {NOT} {conjugated_verbtohave} {target_verb}",
                f"{subject} {conjugated_verbtohave} {NO} {target_verb}",
            ],
            SAMPLE_N_BAITS,
        )

    def _get_phrase(self, original_phrase, correct_answer):
        return self._underline_word(original_phrase, correct_answer)
