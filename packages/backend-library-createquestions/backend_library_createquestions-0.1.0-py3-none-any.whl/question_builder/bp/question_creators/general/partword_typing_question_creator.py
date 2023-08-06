import re

from ...dictionary_factory import CORRECT
from ...dictionary_factory import word2partwordtyping
from ...exceptions.dictionary_exceptions import WordNotInPartWordTypingDictionary
from ...questions.question import Question
from ..question_creator import QuestionCreator
from question_builder.data import DataQuestion
from typing import List


class PartWordTypingQuestionCreator(QuestionCreator):

    code = "PWT"
    baits_code = "nobaits"

    def create(self, data_question: DataQuestion, user_id: str) -> Question:
        content = data_question.content
        target_lemma = data_question.target_lemma
        target_word = data_question.target_word

        question = Question()
        question.content_id = content.id
        question.target_lemma = target_lemma
        question.target_word = target_word
        question.links, question.media_types = self._get_links_and_media_types(content)
        question.correct_answer = self._get_correct_answer(target_word)
        question.baits = self._get_baits()
        question.options = self._get_options(question.correct_answer, question.baits)
        question.phrase = self._get_phrase(
            content.phrase, target_word, question.correct_answer
        )
        question.original_phrase = content.phrase
        question.phrase_translation = self._get_translation(content)
        question.question_type = self.code
        question.baits_type = self.baits_code
        return question

    def _get_correct_answer(self, target_word: str) -> str:
        if target_word in word2partwordtyping:
            return word2partwordtyping[target_word][CORRECT]
        raise WordNotInPartWordTypingDictionary()

    def _get_baits(self) -> List[str]:
        return []

    def _get_phrase(self, original_phrase: str, target_word: str, correct_answer: str) -> str:
        return self._remove_word(original_phrase, target_word, correct_answer)

    def _remove_word(self, phrase: str, target_word: str, part_word: str) -> str:

        blank_line = "_" * len(part_word)
        replacement = re.sub(
            r"" + part_word + r"",
            r"" + blank_line + "",
            target_word,
            count=1,
            flags=re.I,
        )
        phrase = re.sub(
            r"\b" + target_word + r"(\b|(?=n't))",
            r" " + replacement + " ",
            phrase,
            flags=re.I,
        )
        phrase = self._clean_phrase(phrase)
        return phrase
