import random

from ...config import MAX_SYNONYM_ANSWERS
from ...dictionary_factory import pos2words
from ...dictionary_factory import word2multisynonym
from ...exceptions.dictionary_exceptions import WordNotInMultiSynonymDictionary
from ...questions.question import CORRECT
from ...questions.question import Question
from ...questions.question import TEXT
from ..question_creator import QuestionCreator
from question_builder.data import DataQuestion
from typing import List, Dict


class MultiSynonymQuestionCreator(QuestionCreator):

    code = "MSYN"
    baits_code = "pos"

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
        question.baits = self._get_baits(pos, question.correct_answer)
        question.options = self._get_options(question.correct_answer, question.baits)
        question.phrase = self._get_phrase(content.phrase, target_word)
        question.original_phrase = content.phrase
        question.phrase_translation = self._get_translation(content)
        question.question_type = self.code
        question.baits_type = self.baits_code
        return question

    def _get_correct_answer(self, pos: str, target_word: str) -> List[str]:
        if (target_word, pos) in word2multisynonym:
            synonym_list = word2multisynonym[(target_word, pos)]
        elif (target_word, None) in word2multisynonym:
            synonym_list = word2multisynonym[(target_word, None)]
        else:
            raise WordNotInMultiSynonymDictionary()

        if len(synonym_list) <= MAX_SYNONYM_ANSWERS:
            synonyms = synonym_list[:]
            random.shuffle(synonyms)
        else:
            synonyms = random.sample(str, MAX_SYNONYM_ANSWERS)
        return synonyms

    def _get_phrase(self, original_phrase: str, target_word: str) -> str:
        return self._underline_word(original_phrase, target_word)

    def _get_baits(self, pos: str, correct_answer: List[str]) -> List[str]:
        baits = set()
        n_baits = MAX_SYNONYM_ANSWERS - len(correct_answer)
        baits.update(random.sample(pos2words[pos], MAX_SYNONYM_ANSWERS))
        while len(baits) < n_baits:
            rnd_pos = random.choice(list(pos2words.keys()))
            if rnd_pos != pos:
                baits.update(pos2words[rnd_pos])
        return list(baits)[:n_baits]

    def _get_options(self, correct_answer: List[str], baits: List[str]) -> List[Dict]:
        """
        Get the baits and the words, and make an array of Options Objects in
        which word is set to True, and all others are False
        """
        options = []
        for word in correct_answer:
            options.append({TEXT: word, CORRECT: True})
        for bait in baits:
            options.append({TEXT: bait, CORRECT: False})
        random.shuffle(options)
        return options
