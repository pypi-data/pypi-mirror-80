import random

from question_builder.bp.question_creators.question_creator import QuestionCreator
from question_builder.bp.questions.question import Question
from question_builder.data import DataQuestion
from typing import List

SUBJECT_KEY = "subject"
AUXILIARYVERB_KEY = "conjugated_auxiliaryverb"
TARGET_VERB_CONJUGATIONS_KEY = "lemma_conjugations"
PRESENT_Continuous_KEY = "VBG"
HAD = "had"
HAVE = "have"
WILL = "will"
SAMPLE_N_BAITS = 2


class FuturePerfectChoiceQuestionCreator(QuestionCreator):

    CODE = "FPC"
    BAITS_CODE = "nofpc"

    def create(self, data_question: DataQuestion, user_id: str) -> Question:
        content = data_question.content
        target_lemma = data_question.target_lemma
        target_word = data_question.target_word

        verbgames_pattern_items = data_question.verbgames_pattern_items
        subject = verbgames_pattern_items[SUBJECT_KEY]
        verbtowill = verbgames_pattern_items[AUXILIARYVERB_KEY]
        target_verb_present_continuous = verbgames_pattern_items[
            TARGET_VERB_CONJUGATIONS_KEY
        ][PRESENT_Continuous_KEY]
        subject_and_verbtowill = self._get_combined_subject_and_verbtowill(
            subject, verbtowill
        )

        question = Question()
        question.content_id = content.id
        question.target_word = target_word
        question.target_lemma = target_lemma
        question.links, question.media_types = self._get_links_and_media_types(content)
        question.correct_answer = self._get_correct_answer(
            target_word, subject_and_verbtowill
        )
        question.baits = self._get_baits(
            target_word,
            subject_and_verbtowill,
            target_lemma,
            target_verb_present_continuous,
        )
        question.options = self._get_options(question.correct_answer, question.baits)
        question.phrase = self._get_phrase(content.phrase, question.correct_answer)
        question.original_phrase = content.phrase
        question.phrase_translation = self._get_translation(content)
        question.question_type = self.CODE
        question.baits_type = self.BAITS_CODE
        return question

    @staticmethod
    def _get_combined_subject_and_verbtowill(subject: str, verbtowill: str) -> str:
        if verbtowill == WILL:
            return f"{subject} {verbtowill}"
        else:
            return f"{subject}{verbtowill}"

    @staticmethod
    def _get_correct_answer(target_verb: str, subject_and_verbtowill: str) -> str:
        return f"{subject_and_verbtowill} {HAVE} {target_verb}"

    @staticmethod
    def _get_baits(
        target_verb: str,
        subject_and_verbtowill: str,
        target_verb_lemma: str,
        target_verb_present_continuous: str,
    ) -> List[str]:
        return random.sample(
            [
                f"{subject_and_verbtowill} {HAD} {target_verb}",
                f"{subject_and_verbtowill} {HAVE} {target_verb_present_continuous}",
                f"{subject_and_verbtowill} {HAVE} {target_verb_lemma}",
            ],
            SAMPLE_N_BAITS,
        )

    def _get_phrase(self, original_phrase: str, correct_answer: str) -> str:
        return self._underline_word(original_phrase, correct_answer)
