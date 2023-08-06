import random

from ...dictionary_factory import word2minimalpair
from ...exceptions.dual_video_exceptions import ContentNotFoundException
from ...exceptions.dual_video_exceptions import MinimalPairNotFoundException
from ...questions.dual_video_question import DualVideoQuestion
from ..dual_video_question_creator import DualVideoQuestionCreator
from ..question_creator import QuestionCreator
from question_builder.data import DataQuestion
from question_builder.data import Content


class MinimalPairsQuestionCreator(DualVideoQuestionCreator):

    code = "MP"
    baits_code = "nobaits"

    def create(self, data_question: DataQuestion, user_id: str) -> DualVideoQuestion:
        target_lemma = data_question.target_lemma
        target_word = data_question.target_word
        incorrect_content = self._get_bait_content(target_lemma, data_question)
        correct_content = data_question.content
        question = DualVideoQuestion()
        question.content_id = correct_content.id
        question.target_lemma = target_lemma
        question.target_word = target_word
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

    def _get_bait_content(self, target_lemma: str, data_question: DataQuestion) -> Content:
        if target_lemma in word2minimalpair:
            content = data_question.pair_content
            if content:
                return content
            raise ContentNotFoundException()
        raise MinimalPairNotFoundException()

    def _get_phrase(self, content) -> str:
        return content.phrase

    def _get_translation(self, content) -> str:
        if hasattr(content, "translation"):
            if content.translation is not None:
                phrase_translation = content.translation.strip()
            else:
                phrase_translation = ""
        else:
            phrase_translation = ""
        return phrase_translation
