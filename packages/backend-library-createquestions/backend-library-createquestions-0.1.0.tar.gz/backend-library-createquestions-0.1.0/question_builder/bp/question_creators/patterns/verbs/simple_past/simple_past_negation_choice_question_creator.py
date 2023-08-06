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
TARGET_VERB_CONJUGATIONS_KEY = "targetverb_conjugations"
PAST_TENSE_KEY = "VBD"
NEGATION_ADVERB_KEY = "negation"
DID = "did"
NOT = "not"
NO = "no"
SAMPLE_N_BAITS = 2


class SimplePastNegationChoiceQuestionCreator(QuestionCreator):

    CODE = "SPANC"
    BAITS_CODE = "nospanc"

    def create(self, data_question: DataQuestion, user_id: str) -> Question:
        content = data_question.content
        target_lemma = data_question.target_lemma
        target_word = data_question.target_word

        verbgames_pattern_items = data_question.verbgames_pattern_items
        subject = verbgames_pattern_items[SUBJECT_KEY]
        negation_adverb = verbgames_pattern_items[NEGATION_ADVERB_KEY]
        target_verb_past_tense = verbgames_pattern_items[TARGET_VERB_CONJUGATIONS_KEY][
            PAST_TENSE_KEY
        ]
        did_with_negation = self._get_did_with_negation(negation_adverb)
        question = Question()
        question.content_id = content.id
        question.target_word = target_word
        question.target_lemma = target_lemma
        question.links, question.media_types = self._get_links_and_media_types(content)
        question.correct_answer = self._get_correct_answer(
            target_word, subject, did_with_negation
        )
        question.baits = self._get_baits(
            target_word, subject, did_with_negation, target_verb_past_tense
        )
        question.options = self._get_options(question.correct_answer, question.baits)
        question.phrase = self._get_phrase(content.phrase, question.correct_answer)
        question.original_phrase = content.phrase
        question.phrase_translation = self._get_translation(content)
        question.question_type = self.CODE
        question.baits_type = self.BAITS_CODE
        return question

    @staticmethod
    def _get_did_with_negation(negation_adverb: str) -> str:
        if negation_adverb == NOT:
            return f"{DID} {negation_adverb}"
        else:
            return f"{DID}{negation_adverb}"

    @staticmethod
    def _get_correct_answer(target_verb, subject: str, did_with_negation: str) -> str:
        return f"{subject} {did_with_negation} {target_verb}"

    @staticmethod
    def _get_baits(self, subject: str, did_with_negation: str, target_verb_past_tense: str) -> List[str]:
        return random.sample(
            [
                f"{subject} {NOT} {target_verb_past_tense}",
                f"{subject} {NO} {target_verb_past_tense}",
                f"{subject} {did_with_negation} {target_verb_past_tense}",
            ],
            SAMPLE_N_BAITS,
        )

    def _get_phrase(self, original_phrase: str, correct_answer: str) -> str:
        return self._underline_word(original_phrase, correct_answer)
