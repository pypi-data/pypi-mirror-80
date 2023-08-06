import random

from question_builder.bp.question_creators.question_creator import QuestionCreator
from question_builder.bp.questions.question import Question
from question_builder.data import DataQuestion

SUBJECT_KEY = "subject"
CONJUGATED_VERBTOHAVE_KEY = "conjugated_auxiliaryverb"
TARGET_VERB_CONJUGATIONS_KEY = "targetverb_conjugations"
PRESENT_Continuous_KEY = "VBG"
APOSTROPHE = "'"
SAMPLE_N_BAITS = 2


class PresentPerfectChoiceQuestionCreator(QuestionCreator):

    CODE = "PPC"
    BAITS_CODE = "noppc"

    def create(self, data_question: DataQuestion, user_id):
        content = data_question.content
        target_lemma = data_question.target_lemma
        target_word = data_question.target_word

        verbgames_pattern_items = data_question.verbgames_pattern_items
        subject = verbgames_pattern_items[SUBJECT_KEY]
        conjugated_verbtohave = verbgames_pattern_items[CONJUGATED_VERBTOHAVE_KEY]
        subject_and_verbtohave = self._get_combined_subject_and_verbtohave(
            subject, conjugated_verbtohave
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
            target_word, subject_and_verbtohave
        )
        question.baits = self._get_baits(
            target_lemma,
            subject,
            subject_and_verbtohave,
            target_verb_present_continuous,
        )
        question.options = self._get_options(question.correct_answer, question.baits)
        question.phrase = self._get_phrase(
            content.phrase, target_word, subject_and_verbtohave
        )
        question.original_phrase = content.phrase
        question.phrase_translation = self._get_translation(content)
        question.question_type = self.CODE
        question.baits_type = self.BAITS_CODE
        return question

    @staticmethod
    def _get_combined_subject_and_verbtohave(subject, conjugated_verbtohave):
        if conjugated_verbtohave.startswith(APOSTROPHE):
            return f"{subject}{conjugated_verbtohave}"
        else:
            return f"{subject} {conjugated_verbtohave}"

    @staticmethod
    def _get_correct_answer(target_verb, subject_and_verbtohave):
        return f"{subject_and_verbtohave} {target_verb}"

    @staticmethod
    def _get_baits(
        target_lemma, subject, subject_and_verbtohave, target_verb_present_continuous
    ):
        return random.sample(
            [
                f"{subject_and_verbtohave} {target_verb_present_continuous}",
                f"{subject} having {target_lemma}",
                f"{subject} had {target_verb_present_continuous}",
            ],
            SAMPLE_N_BAITS,
        )

    def _get_phrase(self, original_phrase, target_verb, subject_and_verbtohave):
        return self._underline_word(
            original_phrase, f"{subject_and_verbtohave} {target_verb}"
        )
