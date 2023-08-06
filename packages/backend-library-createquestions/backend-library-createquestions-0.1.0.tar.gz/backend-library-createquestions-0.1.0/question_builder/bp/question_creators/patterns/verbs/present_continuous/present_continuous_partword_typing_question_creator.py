import random
import re

from question_builder.bp.question_creators.question_creator import QuestionCreator
from question_builder.bp.questions.question import Question
from question_builder.data import DataQuestion
from typing import List

LEMMA_CONJUGATIONS = "lemma_conjugations"
AUXILIARY_VERB = "conjugated_auxiliaryverb"
PATTERN_KEY = "pattern"
VBG = "VBG"
BE = "be"
AM = "am"
CONTRACTED_AM = "'m"
IS = "is"
CONTRACTED_IS = "'s"
ARE = "are"
CONTRACTED_ARE = "'re"
INSTRUCTIONS = 'Completa el presente continuo \n Usa el verbo "{}"'


class PresentContinuousPartWordTypingQuestionCreator(QuestionCreator):

    code = "PCPT"
    baits_code = "nopcpt"

    def create(self, data_question: DataQuestion, user_id: str) -> Question:
        content = data_question.content
        target_lemma = data_question.target_lemma
        target_word = data_question.target_word

        verbgames_pattern_items = data_question.verbgames_pattern_items
        pattern = verbgames_pattern_items[PATTERN_KEY]
        auxiliary_verb = verbgames_pattern_items[AUXILIARY_VERB]

        question = Question()
        question.content_id = content.id
        question.target_lemma = target_lemma
        question.target_word = target_word
        question.links, question.media_types = self._get_links_and_media_types(content)
        question.correct_answer = self._get_correct_answer(
            target_word, auxiliary_verb
        )
        question.baits = self._get_baits()
        question.options = self._get_options(question.correct_answer, question.baits)
        question.phrase = self._get_phrase(content.phrase, pattern, question.correct_answer, auxiliary_verb)
        question.original_phrase = content.phrase
        question.phrase_translation = self._get_translation(content)
        question.question_type = self.code
        question.baits_type = self.baits_code
        question.instructions = INSTRUCTIONS.format(self._get_correct_answer_lemma(question.correct_answer, target_lemma))
        return question

    def _get_correct_answer(self, target_word: str, auxiliary_verb: str) -> str:
        if bool(random.getrandbits(1)):
            return target_word
        return auxiliary_verb.replace("'", "").strip()

    def _get_baits(self) -> List[str]:
        return []

    def _get_correct_answer_lemma(self, correct_answer: str, target_lemma: str) -> str:
        if(correct_answer in [AM, IS, ARE, CONTRACTED_AM, CONTRACTED_IS, CONTRACTED_ARE]):
            return BE
        else:
            return target_lemma


    def _get_pattern_substitution(self, pattern: str, correct_answer: str, auxiliary_verb: str) -> str:
        if(auxiliary_verb.replace("'", "") == correct_answer and \
            auxiliary_verb.startswith("'")):
            redata = re.compile(re.escape(auxiliary_verb), re.IGNORECASE)  
            final_pattern = redata.sub("'"+len(correct_answer)*"_", pattern) 
            return final_pattern

        redata = re.compile(re.escape(correct_answer), re.IGNORECASE)   
        final_pattern = redata.sub(len(correct_answer)*"_", pattern)
        return final_pattern

    def _get_phrase(self, original_phrase: str, pattern: str, correct_answer: str, auxiliary_verb: str) -> str:
        pattern_substitution = self._get_pattern_substitution(pattern, 
                                                            correct_answer, 
                                                            auxiliary_verb)
        redata = re.compile(re.escape(pattern), re.IGNORECASE)
        phrase = redata.sub(pattern_substitution , original_phrase)
        return phrase
