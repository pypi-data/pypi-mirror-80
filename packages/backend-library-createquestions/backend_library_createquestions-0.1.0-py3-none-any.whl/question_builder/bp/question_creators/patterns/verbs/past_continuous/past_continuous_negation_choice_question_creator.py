import random

from question_builder.bp.exceptions.question_creator_exception import (
    QuestionCreatorException,
)
from question_builder.bp.question_creators.question_creator import QuestionCreator
from question_builder.bp.questions.question import Question
from question_builder.data import DataQuestion
from typing import List

SUBJECT_KEY = "subject"
CONJUGATED_VERBTOBE_KEY = "conjugated_auxiliaryverb"
NEGATION_ADVERB_KEY = "negation"
TARGET_VERB_CONJUGATIONS_KEY = "targetverb_conjugations"
PAST_TENSE_KEY = "VBD"
NOT = "not"
NO = "no"
DONT = "don't"
SAMPLE_N_BAITS = 2


class PastContinuousNegationChoiceQuestionCreator(QuestionCreator):

    CODE = "PACNC"
    BAITS_CODE = "nopacnc"

    def create(self, data_question: DataQuestion, user_id: str) -> Question:
        content = data_question.content
        target_lemma = data_question.target_lemma
        target_word = data_question.target_word

        verbgames_pattern_items = data_question.verbgames_pattern_items
        subject = verbgames_pattern_items[SUBJECT_KEY]
        conjugated_verbtobe = verbgames_pattern_items[CONJUGATED_VERBTOBE_KEY]
        negation_adverb = verbgames_pattern_items[NEGATION_ADVERB_KEY]
        target_verb_past_tense = verbgames_pattern_items[TARGET_VERB_CONJUGATIONS_KEY][
            PAST_TENSE_KEY
        ]
        verbtobe_and_negation_adverb = self._get_combined_verbtobe_and_negation_adverb(
            conjugated_verbtobe, negation_adverb
        )

        question = Question()
        question.content_id = content.id
        question.target_word = target_word
        question.target_lemma = target_lemma
        question.links, question.media_types = self._get_links_and_media_types(content)
        question.correct_answer = self._get_correct_answer(
            target_word, subject, verbtobe_and_negation_adverb
        )
        question.baits = self._get_baits(
            target_word,
            subject,
            conjugated_verbtobe,
            target_verb_past_tense,
            verbtobe_and_negation_adverb,
        )
        question.options = self._get_options(question.correct_answer, question.baits)
        question.phrase = self._get_phrase(content.phrase, question.correct_answer)
        question.original_phrase = content.phrase
        question.phrase_translation = self._get_translation(content)
        question.question_type = self.CODE
        question.baits_type = self.BAITS_CODE
        return question

    @staticmethod
    def _get_combined_verbtobe_and_negation_adverb(
        conjugated_verbtobe: str, negation_adverb: str
    ) -> str:
        if negation_adverb == NOT:
            return f"{conjugated_verbtobe} {negation_adverb}"
        else:
            return f"{conjugated_verbtobe}{negation_adverb}"

    @staticmethod
    def _get_correct_answer(target_verb: str, subject: str, verbtobe_and_negation_adverb: str) -> str:
        return f"{subject} {verbtobe_and_negation_adverb} {target_verb}"

    @staticmethod
    def _get_baits(
        target_verb: str,
        subject: str,
        conjugated_verbtobe: str,
        target_verb_past_tense: str,
        verbtobe_and_negation_adverb: str,
    ) -> List[str]:
        return random.sample(
            [
                f"{subject} {conjugated_verbtobe} {DONT} {target_verb}",
                f"{subject} {verbtobe_and_negation_adverb} {target_verb_past_tense}",
                f"{subject} {conjugated_verbtobe} {NO} {target_verb}",
            ],
            SAMPLE_N_BAITS,
        )

    def _get_phrase(self, original_phrase: str, correct_answer: str) -> str:
        return self._underline_word(original_phrase, correct_answer)
