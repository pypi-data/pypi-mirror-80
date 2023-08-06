import random

from question_builder.bp.question_creators.question_creator import QuestionCreator
from question_builder.bp.questions.question import Question
from question_builder.data import DataQuestion
from typing import List

FULL_REGULAR_PAST_SUFFIX = "ed"
HALF_REGULAR_PAST_SUFFIX = "d"
Y_REGULAR_PAST_SUFFIX = "ied"
VERB_ENDING_E = "e"
VERB_ENDING_Y = "y"
REMOVE_Y_ENDING = -1


class IrregularPastTenseChoiceQuestionCreator(QuestionCreator):

    CODE = "IRTCP"
    BAITS_CODE = "noirtc-p"

    def create(self, data_question: DataQuestion, user_id: str) -> Question:
        content = data_question.content
        target_lemma = data_question.target_lemma
        target_word = data_question.target_word

        question = Question()
        question.content_id = content.id
        question.target_word = target_word
        question.target_lemma = target_lemma
        question.links, question.media_types = self._get_links_and_media_types(content)
        question.correct_answer = target_word
        question.baits = self._get_bait(target_lemma)
        question.options = self._get_options(question.correct_answer, question.baits)
        question.phrase = self._get_phrase(content.phrase, target_word)
        question.original_phrase = content.phrase
        question.phrase_translation = self._get_translation(content)
        question.question_type = self.CODE
        question.baits_type = self.BAITS_CODE
        return question

    @staticmethod
    def _get_bait(target_lemma: str) -> List[str]:
        if target_lemma.endswith(VERB_ENDING_E):
            return [f"{target_lemma}{HALF_REGULAR_PAST_SUFFIX}"]
        elif target_lemma.endswith(VERB_ENDING_Y):
            target_lemma_no_y = target_lemma[:REMOVE_Y_ENDING]
            return [f"{target_lemma_no_y}{Y_REGULAR_PAST_SUFFIX}"]
        else:
            return [f"{target_lemma}{FULL_REGULAR_PAST_SUFFIX}"]

    def _get_phrase(self, original_phrase: str, target_verb: str) -> str:
        return self._underline_word(original_phrase, target_verb)
