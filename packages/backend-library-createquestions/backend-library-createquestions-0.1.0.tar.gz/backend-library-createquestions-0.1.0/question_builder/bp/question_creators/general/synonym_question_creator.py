import random

from ...dictionary_factory import pos2words
from ...dictionary_factory import word2multisynonym
from ...dictionary_factory import word2soundslike
from ...exceptions.dictionary_exceptions import WordNotInMultisynonymDictionary
from ...exceptions.dictionary_exceptions import WordNotInSoundsLikeDictionary
from ...questions.question import N_BAITS
from ...questions.question import Question
from ..question_creator import QuestionCreator
from question_builder.data import DataQuestion
from typing import List


class SynonymQuestionCreator(QuestionCreator):

    code = "SYN"
    baits_sounds_code = "sounds"
    baits_pos_code = "pos"

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
        question.correct_answer = self._get_correct_answer(pos, target_word)
        baits_code, question.baits = self._get_baits(target_word, pos)
        question.options = self._get_options(question.correct_answer, question.baits)
        question.phrase = self._get_phrase(content.phrase, target_word)
        question.original_phrase = content.phrase
        question.phrase_translation = self._get_translation(content)
        question.question_type = self.code
        question.baits_type = baits_code
        return question

    def _get_correct_answer(self, pos: str, target_word: str) -> str:
        if (target_word, pos) in word2multisynonym:
            return random.choice(word2multisynonym[(target_word, pos)])
        if (target_word, None) in word2multisynonym:
            return random.choice(word2multisynonym[(target_word, None)])
        raise WordNotInMultisynonymDictionary()

    def _get_baits(self, target_word: str, pos: str) -> List[str]:
        if target_word in word2soundslike:
            return (
                self.baits_sounds_code,
                random.sample(word2soundslike[target_word], N_BAITS),
            )
        else:
            return self.baits_pos_code, random.sample(pos2words[pos], N_BAITS)

    def _get_phrase(self, original_phrase: str, target_word: str) -> str:
        return self._underline_word(original_phrase, target_word)
