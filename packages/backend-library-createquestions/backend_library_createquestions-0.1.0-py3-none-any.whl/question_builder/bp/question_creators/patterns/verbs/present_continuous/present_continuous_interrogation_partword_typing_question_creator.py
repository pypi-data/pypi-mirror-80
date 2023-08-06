import random
import re

from question_builder.bp.question_creators.question_creator import QuestionCreator
from question_builder.bp.questions.question import Question
from question_builder.data import DataQuestion
from typing import List

LEMMA_CONJUGATIONS = "lemma_conjugations"
PATTERN_KEY = "pattern"
VBG = "VBG"
AM = "am"
CONTRACTED_AM = "'m"
IS = "is"
CONTRACTED_IS = "'s"
ARE = "are"
CONTRACTED_ARE = "'re"
AINT = "ain't"
INSTRUCTIONS = 'Completa la negación'


class PresentContinuousInterrogationPartWordTypingQuestionCreator(QuestionCreator):

    code = "PCIPT"
    baits_code = "nopcipt"

    def create(self, data_question: DataQuestion, user_id: str) -> Question:
        content = data_question.content
        target_lemma = data_question.target_lemma
        target_word = data_question.target_word
        verbgames_pattern_items = data_question.verbgames_pattern_items
        pattern = verbgames_pattern_items[PATTERN_KEY]
        lemma_conjugations = verbgames_pattern_items[LEMMA_CONJUGATIONS]
        verb_present_continuous = lemma_conjugations[VBG]
        question = Question()
        question.content_id = content.id
        question.target_lemma = target_lemma
        question.target_word = target_word
        question.links, question.media_types = self._get_links_and_media_types(content)
        question.correct_answer = self._get_correct_answer(
            verb_present_continuous, pattern
        )
        question.baits = self._get_baits()
        question.options = self._get_options(question.correct_answer, question.baits)

        question.phrase = self._get_phrase(content.phrase, question.correct_answer)
        question.original_phrase = content.phrase
        question.phrase_translation = self._get_translation(content)
        question.question_type = self.code
        question.baits_type = self.baits_code
        question.instructions = INSTRUCTIONS.format(target_lemma)
        return question

    def _get_correct_answer(self, verb_present_continuous: str, pattern: str) -> str:
        if bool(random.getrandbits(1)):
            return verb_present_continuous
        if AM in pattern.lower():
            return AM
        if IS in pattern.lower():
            return IS
        if ARE in pattern.lower():
            return ARE
        if CONTRACTED_AM in pattern.lower():
            return CONTRACTED_AM
        if CONTRACTED_IS in pattern.lower():
            return CONTRACTED_IS
        if CONTRACTED_ARE in pattern.lower():
            return CONTRACTED_ARE
        if AINT in pattern.lower():
            return AINT

    def _get_baits(self) -> List[str]:
        return []

    def _get_phrase(self, original_phrase: str, correct_answer: str) -> str:
        return self._remove_word(original_phrase, correct_answer)
