import random

from question_builder.bp.question_creators.question_creator import QuestionCreator
from question_builder.bp.questions.question import Question
from question_builder.data import DataQuestion

SUBJECT_KEY = "subject"
TARGET_VERB_CONJUGATIONS_KEY = "lemma_conjugations"
PRESENT_CONTINUOUS_KEY = "VBG"
HAD = "had"
HAVE = "have"
HAS = "has"
SAMPLE_N_BAITS = 2


class PastPerfectChoiceQuestionCreator(QuestionCreator):

    CODE = "PAPC"
    BAITS_CODE = "nopapc"

    def create(self, data_question: DataQuestion, user_id):
        content = data_question.content
        target_lemma = data_question.target_lemma
        target_word = data_question.target_word

        verbgames_pattern_items = data_question.verbgames_pattern_items
        subject = verbgames_pattern_items[SUBJECT_KEY]
        target_verb_present_continuous = verbgames_pattern_items[
            TARGET_VERB_CONJUGATIONS_KEY
        ][PRESENT_CONTINUOUS_KEY]

        question = Question()
        question.content_id = content.id
        question.target_word = target_word
        question.target_lemma = target_lemma
        question.links, question.media_types = self._get_links_and_media_types(content)
        question.correct_answer = self._get_correct_answer(target_word, subject)
        question.baits = self._get_baits(
            target_word, subject, target_lemma, target_verb_present_continuous
        )
        question.options = self._get_options(question.correct_answer, question.baits)
        question.phrase = self._get_phrase(content.phrase, question.correct_answer)
        question.original_phrase = content.phrase
        question.phrase_translation = self._get_translation(content)
        question.question_type = self.CODE
        question.baits_type = self.BAITS_CODE
        return question

    @staticmethod
    def _get_correct_answer(target_verb, subject):
        return f"{subject} {HAD} {target_verb}"

    @staticmethod
    def _get_baits(
        target_verb, subject, target_verb_lemma, target_verb_present_continuous
    ):
        have_bait_form = random.sample([HAVE, HAS], 1)[0]
        return random.sample(
            [
                f"{subject} {HAD} {target_verb_lemma}",
                f"{subject} {have_bait_form} {target_verb_present_continuous}",
                f"{subject} {HAVE} {target_verb_lemma}",
            ],
            SAMPLE_N_BAITS,
        )

    def _get_phrase(self, original_phrase, correct_answer):
        return self._underline_word(original_phrase, correct_answer)
