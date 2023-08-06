import re

from question_builder.bp.question_creators.question_creator import QuestionCreator
from question_builder.bp.questions.question import Question
from question_builder.data import DataQuestion

LEMMA_CONJUGATIONS = "lemma_conjugations"
PATTERN_KEY = "pattern"
VBG = "VBG"
NOT = " not "
NT = "n't"
INSTRUCTIONS = 'Completa la negación'


class PresentContinuousNegativePartWordTypingQuestionCreator(QuestionCreator):

    code = "PCNPT"
    baits_code = "nopcnpt"

    def create(self, data_question: DataQuestion, user_id):
        content = data_question.content
        target_lemma = data_question.target_lemma
        target_word = data_question.target_word
        verbgames_pattern_items = data_question.verbgames_pattern_items
        negation = verbgames_pattern_items["negation"]
        pattern = verbgames_pattern_items[PATTERN_KEY]

        question = Question()
        question.content_id = content.id
        question.target_lemma = target_lemma
        question.target_word = target_word
        question.links, question.media_types = self._get_links_and_media_types(content)
        question.correct_answer = negation.replace("'", "").strip()
        question.baits = self._get_baits()
        question.options = self._get_options(question.correct_answer, question.baits)
        question.phrase = self._get_phrase(content.phrase, pattern, negation)
        question.original_phrase = content.phrase
        question.phrase_translation = self._get_translation(content)
        question.question_type = self.code
        question.baits_type = self.baits_code
        question.instructions = INSTRUCTIONS.format(target_lemma)
        return question

    def _get_baits(self):
        return []

    def _get_pattern_substitution(self, pattern, negation):
        final_pattern = pattern
        redata = re.compile(re.escape(negation), re.IGNORECASE)
        if(negation == "n't"):
            final_pattern = redata.sub("_'_", pattern)
        elif(negation == "not"):
            final_pattern = redata.sub("___", pattern)
        return final_pattern

    def _get_phrase(self, original_phrase, pattern, negation):
        pattern_substitution = self._get_pattern_substitution(pattern, negation)
        redata = re.compile(re.escape(pattern), re.IGNORECASE)
        phrase = redata.sub(pattern_substitution , original_phrase)
        return phrase
