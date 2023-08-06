import random

from question_builder.bp.question_creators.question_creator import QuestionCreator
from question_builder.bp.questions.question import Question
from question_builder.data import DataQuestion

SUBJECT_KEY = "subject"
CONJUGATED_VERBTOBE_KEY = "conjugated_auxiliaryverb"
TARGET_VERB_CONJUGATIONS_KEY = "targetverb_conjugations"
PAST_TENSE_KEY = "VBD"
DID = "did"
SAMPLE_N_BAITS = 2


class PastContinuousChoiceQuestionCreator(QuestionCreator):

    CODE = "PACC"
    BAITS_CODE = "nopacc"

    def create(self, data_question: DataQuestion, user_id):
        content = data_question.content
        target_lemma = data_question.target_lemma
        target_word = data_question.target_word

        verbgames_pattern_items = data_question.verbgames_pattern_items
        subject = verbgames_pattern_items[SUBJECT_KEY]
        conjugated_verbtobe = verbgames_pattern_items[CONJUGATED_VERBTOBE_KEY]
        target_verb_past_tense = verbgames_pattern_items[TARGET_VERB_CONJUGATIONS_KEY][
            PAST_TENSE_KEY
        ]

        question = Question()
        question.content_id = content.id
        question.target_word = target_word
        question.target_lemma = target_lemma
        question.links, question.media_types = self._get_links_and_media_types(content)
        question.correct_answer = self._get_correct_answer(
            target_word, subject, conjugated_verbtobe
        )
        question.baits = self._get_baits(
            target_word,
            target_lemma,
            subject,
            conjugated_verbtobe,
            target_verb_past_tense,
        )
        question.options = self._get_options(question.correct_answer, question.baits)
        question.phrase = self._get_phrase(content.phrase, question.correct_answer)
        question.original_phrase = content.phrase
        question.phrase_translation = self._get_translation(content)
        question.question_type = self.CODE
        question.baits_type = self.BAITS_CODE
        return question

    @staticmethod
    def _get_correct_answer(target_verb, subject, conjugated_verbtobe):
        return f"{subject} {conjugated_verbtobe} {target_verb}"

    @staticmethod
    def _get_baits(
        target_verb, target_lemma, subject, conjugated_verbtobe, target_verb_past_tense
    ):
        return random.sample(
            [
                f"{subject} {DID} {conjugated_verbtobe} {target_verb}",
                f"{subject} {conjugated_verbtobe} {target_verb_past_tense}",
                f"{subject} {conjugated_verbtobe} {target_lemma}",
            ],
            SAMPLE_N_BAITS,
        )

    def _get_phrase(self, original_phrase, correct_answer):
        return self._underline_word(original_phrase, correct_answer)
