import random
import re

from question_builder.bp.question_creators.question_creator import QuestionCreator
from question_builder.bp.questions.question import Question
from question_builder.data import DataQuestion
from typing import List

PATTERN_KEY = "pattern"
SUBJECT_KEY = "subject"
AUXILIARYVERB_KEY = "conjugated_auxiliaryverb"
LEMMA_CONJUGATIONS = "lemma_conjugations"
VBG = "VBG"
VBD = "VBD"
AM = "am"
AAM = "'m"
IS = "is"
AIS = "'s"
ARE = "are"
AARE = "'re"
WAS = "was"
WERE = "were"
AINT = "ain't"
N_BAITS = 2
INSTRUCTIONS = 'Elige la opción de presente continuo'


class PresentContinuousChoiceQuestionCreator(QuestionCreator):

    code = "PCC"
    baits_code = "nopcc"

    def create(self, data_question: DataQuestion, user_id: str) -> Question:

        content = data_question.content
        target_lemma = data_question.target_lemma
        target_word = data_question.target_word

        verbgames_pattern_items = data_question.verbgames_pattern_items
        pattern = verbgames_pattern_items[PATTERN_KEY]
        subject = verbgames_pattern_items[SUBJECT_KEY]
        lemma_conjugations = verbgames_pattern_items[LEMMA_CONJUGATIONS]
        verb_past = lemma_conjugations[VBD]
        verb_present_continuous = lemma_conjugations[VBG]
        question = Question()
        question.content_id = content.id
        question.target_word = target_word
        question.target_lemma = target_lemma
        question.links, question.media_types = self._get_links_and_media_types(content)
        question.correct_answer = pattern
        question.baits = self._get_baits(
            subject, pattern, target_lemma, verb_past, verb_present_continuous
        )
        question.options = self._get_options(question.correct_answer, question.baits)
        question.phrase = self._get_phrase(content.phrase, pattern)
        question.original_phrase = content.phrase
        question.phrase_translation = self._get_translation(content)
        question.question_type = self.code
        question.baits_type = self.baits_code
        question.instructions = INSTRUCTIONS.format(target_lemma)
        return question

    def _get_baits(
        self, subject: str, pattern: str, target_lemma: str, verb_past: str, verb_present_continuous: str
    ) -> List[str]:
        verb_to_be = self._get_verb_to_be(pattern)
        past_verb_to_be = self._get_past_verb_to_be(verb_to_be)
        return random.sample(
            [
                f"{subject}{past_verb_to_be} {verb_present_continuous}",
                f"{subject}{verb_to_be} {verb_past}",
            ],
            2,
        )

    def _get_phrase(self, original_phrase: str, pattern: str) -> str:
        redata = re.compile(re.escape(pattern), re.IGNORECASE)
        phrase = redata.sub("_" * len(pattern), original_phrase)
        return phrase

    def _get_verb_to_be(self, pattern: str) -> str:
        if f" {AM} " in pattern:
            return f" {AM}"
        elif f"{AAM} " in pattern:
            return f"{AAM}"
        elif f" {IS} " in pattern:
            return f" {IS}"
        elif f"{AIS} " in pattern:
            return f"{AIS}"
        elif f" {ARE} " in pattern:
            return f" {ARE}"
        elif f"{AARE} " in pattern:
            return f"{AARE}"
        elif f"{AINT} " in pattern:
            return f" {AINT}"

    def _get_past_verb_to_be(self, verb: str) -> str:
        if f"{AM}" in verb or f"{AAM}" in verb:
            return f" {WAS}"
        elif f"{IS}" in verb or f"{AIS}" in verb:
            return f" {WAS}"
        elif f"{ARE}" in verb or f"{AARE}" in verb:
            return f" {WERE}"
        if f"{AINT}" in verb:
            return f" {WAS}"