import random

from question_builder.bp.question_creators.question_creator import QuestionCreator
from question_builder.bp.questions.question import Question
from question_builder.data import DataQuestion
from typing import List

SUBJECT_KEY = "subject"
NEGATION_ADVERB_KEY = "negation"
HAVE = "have"
WILL = "will"
WONT = "won't"
DONT = "don't"
NOT = "not"
NO = "no"
SAMPLE_N_BAITS = 2


class FuturePerfectNegativeChoiceQuestionCreator(QuestionCreator):

    CODE = "FPNC"
    BAITS_CODE = "nofpnc"

    def create(self, data_question: DataQuestion, user_id: str) -> Question:
        content = data_question.content
        target_lemma = data_question.target_lemma
        target_word = data_question.target_word

        verbgames_pattern_items = data_question.verbgames_pattern_items
        subject = verbgames_pattern_items[SUBJECT_KEY]
        negation_adverb = verbgames_pattern_items[NEGATION_ADVERB_KEY]
        verbtowill_and_negation = self._get_combined_verbtowill_and_negation(
            negation_adverb
        )

        question = Question()
        question.content_id = content.id
        question.target_word = target_word
        question.target_lemma = target_lemma
        question.links, question.media_types = self._get_links_and_media_types(content)
        question.correct_answer = self._get_correct_answer(
            target_word, subject, verbtowill_and_negation
        )
        question.baits = self._get_baits(target_word, subject)
        question.options = self._get_options(question.correct_answer, question.baits)
        question.phrase = self._get_phrase(content.phrase, question.correct_answer)
        question.original_phrase = content.phrase
        question.phrase_translation = self._get_translation(content)
        question.question_type = self.CODE
        question.baits_type = self.BAITS_CODE
        return question

    @staticmethod
    def _get_combined_verbtowill_and_negation(negation: str) -> str:
        if negation == NOT:
            return f"{WILL} {NOT}"
        else:
            return WONT

    @staticmethod
    def _get_correct_answer(target_verb: str, subject: str, verbtowill_and_negation: str) -> str:
        return f"{subject} {verbtowill_and_negation} {HAVE} {target_verb}"

    @staticmethod
    def _get_baits(target_verb: str, subject: str) -> List[str]:
        return random.sample(
            [
                f"{subject} {WILL} {NO} {target_verb}",
                f"{subject} {NOT} {WILL} {HAVE} {target_verb}",
                f"{subject} {DONT} {WILL} {HAVE} {target_verb}",
            ],
            SAMPLE_N_BAITS,
        )

    def _get_phrase(self, original_phrase: str, correct_answer: str) -> str:
        return self._underline_word(original_phrase, correct_answer)
