import random

from question_builder.bp.dictionary_factory import word2englishdefinitions
from question_builder.bp.exceptions.dictionary_exceptions import (
    WordNotInEnglishDefinitionsDictionary,
)
from question_builder.bp.question_creators.question_creator import QuestionCreator
from question_builder.bp.questions.question import Question
from question_builder.data import DataQuestion
from typing import List

SUBJECT_KEY = "subject"
CONJUGATED_AUXILIARYVERB_KEY = "conjugated_auxiliaryverb"
LEMMA_CONJUGATIONS = "lemma_conjugations"
PRESENT_Continuous_KEY = "VBG"
PAST_TENSE_KEY = "VBD"
GOING = "going"
GOING_TO = "going to"
SAMPLE_N_BAITS = 2


class GoingToFutureChoiceQuestionCreator(QuestionCreator):

    CODE = "GTFC"
    BAITS_CODE = "nogtfc"

    def create(self, data_question: DataQuestion, user_id: str) -> Question:
        content = data_question.content
        target_lemma = data_question.target_lemma
        target_word = data_question.target_word

        verbgames_pattern_items = data_question.verbgames_pattern_items
        conjugated_verbtobe = verbgames_pattern_items[CONJUGATED_AUXILIARYVERB_KEY]
        target_verb_present_continuous = verbgames_pattern_items[LEMMA_CONJUGATIONS][
            PRESENT_Continuous_KEY
        ]
        target_verb_past_tense = verbgames_pattern_items[LEMMA_CONJUGATIONS][
            PAST_TENSE_KEY
        ]
        question = Question()
        question.content_id = content.id
        question.target_word = target_word
        question.target_lemma = target_lemma
        question.links, question.media_types = self._get_links_and_media_types(content)
        question.correct_answer = self._get_correct_answer(
            target_word, conjugated_verbtobe
        )
        question.baits = self._get_baits(
            target_word,
            conjugated_verbtobe,
            target_verb_present_continuous,
            target_verb_past_tense,
        )
        question.options = self._get_options(question.correct_answer, question.baits)
        question.phrase = self._get_phrase(
            content.phrase, target_word, conjugated_verbtobe
        )
        question.original_phrase = content.phrase
        question.phrase_translation = self._get_translation(content)
        question.question_type = self.CODE
        question.baits_type = self.BAITS_CODE
        return question

    @staticmethod
    def _get_correct_answer(target_verb: str, conjugated_verbtobe: str) -> str:
        return f"{conjugated_verbtobe} {GOING_TO} {target_verb}"

    @staticmethod
    def _get_baits(
        target_verb: str,
        conjugated_verbtobe: str,
        target_verb_present_continuous: str,
        target_verb_past_tense: str,
    ) -> List[str]:
        return random.sample(
            [
                f"{conjugated_verbtobe} {GOING} {target_verb}",
                f"{conjugated_verbtobe} {GOING_TO} {target_verb_past_tense}",
                f"{conjugated_verbtobe} {GOING_TO} {target_verb_present_continuous}",
            ],
            SAMPLE_N_BAITS,
        )

    def _get_phrase(self, 
                original_phrase: str, 
                target_verb: str, 
                conjugated_verbtobe: str) -> str:
        return self._underline_word(
            original_phrase, f"{conjugated_verbtobe} {GOING_TO} {target_verb}"
        )
