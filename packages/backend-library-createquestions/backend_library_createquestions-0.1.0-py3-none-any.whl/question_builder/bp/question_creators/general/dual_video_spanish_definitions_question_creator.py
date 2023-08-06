import random

from ...dictionary_factory import word2spanishdefinitions
from ...exceptions.dual_video_exceptions import ContentNotFoundException
from ...exceptions.dual_video_exceptions import DefinitionNotFoundException
from ...exceptions.dual_video_exceptions import SpanishBaitsNotFoundException
from ...questions.dual_video_question import DualVideoQuestion
from ...questions.question import N_BAITS
from ...questions.question import Question
from ...validators.pos_validators import ADJ
from ...validators.pos_validators import ADV
from ...validators.pos_validators import NOUN
from ...validators.pos_validators import VERB
from ..dual_video_question_creator import DualVideoQuestionCreator
from ..dual_video_question_creator import PROBABILITY_OF_SHUFFLING_OPTIONS_IN_DUAL_VIDEO
from question_builder.data import DataQuestion


class DualVideoSpanishDefinitionsQuestionCreator(DualVideoQuestionCreator):

    code = "DVS"
    baits_code = "nobaits"

    def create(self, data_question: DataQuestion, user_id: str) -> Question:

        target_lemma = data_question.target_lemma
        target_word = data_question.target_word
        incorrect_content = data_question.bait_content
        correct_content = data_question.content
        definition = self._get_definition(target_lemma)

        question = DualVideoQuestion()
        question.content_id = correct_content.id
        question.target_word = target_word
        question.target_lemma = target_lemma
        medias_list = self._get_medias([correct_content, incorrect_content])
        question.links = medias_list.links
        question.media_types = medias_list.media_types
        question.phrases = medias_list.phrases
        question.correct_values = medias_list.correct_values
        question.definition = definition
        question.options = None
        question.phrase = definition
        question.original_phrase = correct_content.phrase
        question.phrase_translation = ""
        question.question_type = self.code
        question.baits_type = self.baits_code
        return question

    def _get_definition(self, target_lemma) -> str:

        if (target_lemma, NOUN) in word2spanishdefinitions:
            key = (target_lemma, NOUN)
        elif (target_lemma, VERB) in word2spanishdefinitions:
            key = (target_lemma, VERB)
        elif (target_lemma, ADV) in word2spanishdefinitions:
            key = (target_lemma, ADV)
        elif (target_lemma, ADJ) in word2spanishdefinitions:
            key = (target_lemma, ADJ)
        else:
            raise DefinitionNotFoundException()

        return word2spanishdefinitions[key][0]


