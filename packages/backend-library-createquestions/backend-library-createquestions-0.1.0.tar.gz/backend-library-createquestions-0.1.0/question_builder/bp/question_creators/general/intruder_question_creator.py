import random

from ...dictionary_factory import BAITS
from ...dictionary_factory import CORRECT
from ...dictionary_factory import word2intruder
from ...exceptions.dictionary_exceptions import WordNotInIntruderDictionary
from ...exceptions.pos_exceptions import WordNotVerb
from ...questions.question import N_BAITS
from ...questions.question import Question
from ...validators import pos_validators
from ..question_creator import QuestionCreator
from question_builder.data import DataQuestion
from typing import List


class IntruderQuestionCreator(QuestionCreator):

    code = "INT"
    baits_code = "nointruder"

    def create(self, data_question: DataQuestion, user_id: str) -> Question:

        content = data_question.content
        target_lemma = data_question.target_lemma
        target_word = data_question.target_word
        pos = data_question.pos

        question = Question()
        question.content_id = content.id
        question.target_word = target_word
        question.target_lemma = target_lemma
        question.links, question.media_types = self._get_links_and_media_types(content)
        question.correct_answer = self._get_correct_answer(pos, target_lemma)
        question.baits = self._get_baits(target_lemma)
        question.options = self._get_options(question.correct_answer, question.baits)
        question.phrase = self._get_phrase(content.phrase, target_word)
        question.original_phrase = content.phrase
        question.phrase_translation = self._get_translation(content)
        question.question_type = self.code
        question.baits_type = self.baits_code
        return question

    def _get_correct_answer(self, pos, target_lemma) -> str:
        if not pos_validators.is_verb(pos):
            raise WordNotVerb()
        if target_lemma not in word2intruder:
            raise WordNotInIntruderDictionary()

        return word2intruder[target_lemma][CORRECT]

    def _get_phrase(self, original_phrase, target_word) -> str:
        return self._underline_word(original_phrase, target_word)

    def _get_baits(self, target_lemma) -> List[str]:
        return random.sample(word2intruder[target_lemma][BAITS], N_BAITS)
