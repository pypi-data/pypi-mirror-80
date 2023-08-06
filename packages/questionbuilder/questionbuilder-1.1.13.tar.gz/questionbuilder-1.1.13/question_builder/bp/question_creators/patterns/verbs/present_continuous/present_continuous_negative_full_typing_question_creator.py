import re

from question_builder.bp.question_creators.question_creator import QuestionCreator
from question_builder.bp.questions.question import Question
from question_builder.data import DataQuestion

PATTERN_KEY = "pattern"
SUBJECT_KEY = "subject"
LEMMA_CONJUGATIONS = "lemma_conjugations"
VBG = "VBG"
AM = "am"
CONTRACTED_AM = "'m"
IS = "is"
CONTRACTED_IS = "'s"
ARE = "are"
CONTRACTED_ARE = "'re"
INSTRUCTIONS = 'Completa la negación del presente continuo'


class PresentContinuousNegativeFullWordTypingQuestionCreator(QuestionCreator):

    code = "PCNFT"
    baits_code = "pcnft"

    def create(self, data_question: DataQuestion, user_id):
        content = data_question.content
        target_lemma = data_question.target_lemma
        target_word = data_question.target_word

        verbgames_pattern_items = data_question.verbgames_pattern_items
        pattern = verbgames_pattern_items[PATTERN_KEY]
        subject = verbgames_pattern_items[SUBJECT_KEY]

        question = Question()
        question.content_id = content.id
        question.target_lemma = target_lemma
        question.target_word = target_word
        question.links, question.media_types = self._get_links_and_media_types(content)
        question.correct_answer = self._get_correct_answer(pattern, subject)
        question.baits = self._get_baits()
        question.options = self._get_options(question.correct_answer, question.baits)
        question.phrase = self._get_phrase(content.phrase, pattern, subject)
        question.original_phrase = content.phrase
        question.phrase_translation = self._get_translation(content)
        question.question_type = self.code
        question.baits_type = self.baits_code
        question.instructions = INSTRUCTIONS.format(target_lemma)
        return question

    def _get_correct_answer(self, pattern, subject):
        correct_answer = pattern.replace(subject, "", 1).replace("'", "").strip()
        correct_answer = correct_answer.replace(CONTRACTED_AM, AM)
        correct_answer = correct_answer.replace(CONTRACTED_IS, IS)
        correct_answer = correct_answer.replace(CONTRACTED_ARE, ARE)
        return correct_answer.replace(" ", "")

    def _get_baits(self):
        return []

    def _get_pattern_substitution(self, pattern, subject):
        final_pattern = pattern
        words_to_remove = pattern.replace(subject, "", 1).replace("'", "").strip()
        for word in words_to_remove.split():
            final_pattern = self._remove_word(final_pattern, word)
        return final_pattern

    def _get_phrase(self, original_phrase, pattern, subject):
        pattern_substitution = self._get_pattern_substitution(pattern, subject)
        redata = re.compile(re.escape(pattern), re.IGNORECASE)
        phrase = redata.sub(pattern_substitution , original_phrase)
        return phrase