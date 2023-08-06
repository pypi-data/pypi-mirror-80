import random

from question_builder.bp.question_creators.question_creator import QuestionCreator
from question_builder.bp.questions.question import Question
from question_builder.data import DataQuestion
import re
from typing import List

SUBJECT_KEY = "subject"
CONJUGATED_VERBTOBE_KEY = "conjugated_auxiliaryverb"
NEGATION_ADVERB_KEY = "negation"
PATTERN_KEY = "pattern"
APOSTROPHE = "'"
VERBTOBE_PRESENT_1S_ENDING = "m"
VERBTOBE_PRESENT_2S_ENDING = "re"
VERBTOBE_PRESENT_3S_ENDING = "s"
VERBTOBE_PAST_1S = "was"
VERBTOBE_PAST_2S = "were"
VERBTOBE_PRESENT_1S = "am"
VERBTOBE_PRESENT_2S = "are"
VERBTOBE_PRESENT_3S = "is"
AI = "ai"
DONT = "don't"
NOT = "not"
NO = "no"
SAMPLE_N_BAITS = 2
INSTRUCTIONS = 'Elige la opción de presente continuo'


class PresentContinuousNegativeChoiceQuestionCreator(QuestionCreator):

    CODE = "PCNC"
    BAITS_CODE = "nopcnc"

    def create(self, data_question: DataQuestion, user_id: str) -> Question:
        content = data_question.content
        target_lemma = data_question.target_lemma
        target_word = data_question.target_word

        verbgames_pattern_items = data_question.verbgames_pattern_items
        subject = verbgames_pattern_items[SUBJECT_KEY]
        conjugated_verbtobe = verbgames_pattern_items[CONJUGATED_VERBTOBE_KEY]
        negation_adverb = verbgames_pattern_items[NEGATION_ADVERB_KEY]
        pattern = verbgames_pattern_items[PATTERN_KEY]

        subject_verbtobe_negation = self._get_combined_subject_verbtobe_negation(
            subject, conjugated_verbtobe, negation_adverb
        )
        verbtobe_past_tense = self._get_past_tense_verbtobe(conjugated_verbtobe)

        question = Question()
        question.content_id = content.id
        question.target_word = target_word
        question.target_lemma = target_lemma
        question.links, question.media_types = self._get_links_and_media_types(content)
        question.correct_answer = self._get_correct_answer(
            target_word, subject_verbtobe_negation
        )
        question.baits = self._get_baits(
            target_word, target_lemma, subject, conjugated_verbtobe, verbtobe_past_tense
        )
        question.options = self._get_options(question.correct_answer, question.baits)
        question.phrase = self._get_phrase(content.phrase, pattern)
        question.original_phrase = content.phrase
        question.phrase_translation = self._get_translation(content)
        question.question_type = self.CODE
        question.baits_type = self.BAITS_CODE
        question.instructions = INSTRUCTIONS.format(target_lemma)
        return question

    @staticmethod
    def _get_combined_subject_verbtobe_negation(
        subject: str, conjugated_verbtobe: str, negation_adverb: str
    ) -> str:
        if conjugated_verbtobe.startswith(APOSTROPHE):
            return f"{subject}{conjugated_verbtobe} {negation_adverb}"
        elif negation_adverb.startswith(APOSTROPHE) or conjugated_verbtobe == AI:
            return f"{subject} {conjugated_verbtobe}{negation_adverb}"
        else:
            return f"{subject} {conjugated_verbtobe} {negation_adverb}"

    @staticmethod
    def _get_past_tense_verbtobe(conjugated_verbtobe: str) -> str:
        if conjugated_verbtobe.endswith(
            VERBTOBE_PRESENT_1S_ENDING
        ) or conjugated_verbtobe.endswith(VERBTOBE_PRESENT_3S_ENDING):
            return VERBTOBE_PAST_1S
        else:
            return VERBTOBE_PAST_2S

    @staticmethod
    def _get_correct_answer(target_verb: str, subject_verbtobe_negation: str) -> str:
        return f"{subject_verbtobe_negation} {target_verb}"

    def _get_baits(
        self,
        target_verb: str,
        target_lemma: str,
        subject: str,
        conjugated_verbtobe: str,
        verbtobe_past_tense: str,
    ) -> List[str]:

        verbtobe_present_no_contraction = self._get_verbtobe_present_no_contraction(
            conjugated_verbtobe
        )

        return random.sample(
            [
                f"{subject} {DONT} {verbtobe_present_no_contraction} {target_verb}",
                f"{subject} {NOT} {verbtobe_present_no_contraction} {target_verb}",
                f"{subject} {verbtobe_present_no_contraction} {NO} {target_verb}",
                f"{subject} {verbtobe_past_tense} {NOT} {target_lemma}",
            ],
            SAMPLE_N_BAITS,
        )

    def _get_phrase(self, original_phrase: str, correct_answer: str) -> str:
        redata = re.compile(re.escape(correct_answer), re.IGNORECASE)
        phrase = redata.sub(len(correct_answer)*"_" , original_phrase)
        return phrase

    @staticmethod
    def _get_verbtobe_present_no_contraction(conjugated_verbtobe: str) -> str:
        if conjugated_verbtobe.endswith(VERBTOBE_PRESENT_1S_ENDING):
            return VERBTOBE_PRESENT_1S
        elif conjugated_verbtobe.endswith(VERBTOBE_PRESENT_2S_ENDING):
            return VERBTOBE_PRESENT_2S
        else:
            return VERBTOBE_PRESENT_3S
