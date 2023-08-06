from question_builder.bp.exceptions.dual_video_exceptions import (
    ContentNotFoundException,
)
from question_builder.bp.question_creators.dual_video_question_creator import (
    DualVideoQuestionCreator,
)
from question_builder.bp.questions.dual_video_question import DualVideoQuestion
from question_builder.data import DataQuestion


class FutureDualVideoQuestionCreator(DualVideoQuestionCreator):

    code = "FDV"
    baits_code = "nofdv"

    def create(self, data_question: DataQuestion, user_id):

        target_lemma = data_question.target_lemma
        target_word = data_question.target_word
        incorrect_content = self._get_bait_content(data_question.bait_content)
        correct_content = data_question.content

        question = DualVideoQuestion()
        question.content_id = correct_content.id
        question.target_word = target_word
        question.target_lemma = target_lemma
        medias_list = self._get_medias([correct_content, incorrect_content])
        question.links = medias_list.links
        question.media_types = medias_list.media_types
        question.phrases = medias_list.phrases
        question.correct_values = medias_list.correct_values
        question.options = None
        question.phrase = self._get_phrase(correct_content)
        question.original_phrase = correct_content.phrase
        question.phrase_translation = self._get_translation(correct_content)
        question.question_type = self.code
        question.baits_type = self.baits_code
        return question

    def _get_bait_content(self, content):
        if content:
            return content
        raise ContentNotFoundException()

    def _get_phrase(self, content):
        return content.phrase

    def _get_translation(self, content):
        if hasattr(content, "translation"):
            if content.translation is not None:
                phrase_translation = content.translation.strip()
            else:
                phrase_translation = ""
        else:
            phrase_translation = ""
        return phrase_translation
