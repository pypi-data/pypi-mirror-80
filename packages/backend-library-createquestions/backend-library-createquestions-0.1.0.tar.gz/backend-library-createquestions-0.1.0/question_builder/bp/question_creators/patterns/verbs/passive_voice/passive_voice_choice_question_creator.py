import random
import re

from question_builder.bp.question_creators.question_creator import QuestionCreator
from question_builder.bp.questions.question import Question
from question_builder.data import DataQuestion
from typing import List

PATTERN_KEY = "pattern"
SUBJECT_KEY = "subject"
VB = "VB"
BEEN = "been"
BEEING = "beeing"
BE = "be"
N_BAITS = 2


class PassiveVoiceChoiceQuestionCreator(QuestionCreator):

    code = "PVC"
    baits_code = "nopvc"

    def create(self, data_question: DataQuestion, user_id: str) -> Question:
        
        content = data_question.content
        target_lemma = data_question.target_lemma
        target_word = data_question.target_word

        verbgames_pattern_items = data_question.verbgames_pattern_items
        pattern = verbgames_pattern_items[PATTERN_KEY]
        subject = verbgames_pattern_items[SUBJECT_KEY]

        question = Question()
        question.content_id = content.id
        question.target_word = target_word
        question.target_lemma = target_lemma
        question.links, question.media_types = self._get_links_and_media_types(content)
        question.correct_answer = " ".join(pattern.split()[-3:-1])
        question.baits = self._get_baits(subject, target_lemma, pattern)
        question.options = self._get_options(question.correct_answer, question.baits)
        question.phrase = self._get_phrase(content.phrase, question.correct_answer)
        question.original_phrase = content.phrase
        question.phrase_translation = self._get_translation(content)
        question.question_type = self.code
        question.baits_type = self.baits_code
        question.content_id = content.id
        return question

    def _get_baits(self, subject: str, target_lemma: str, pattern: str) -> List[str]:
        return random.sample(
            [f"are {target_lemma}", f"is {target_lemma}", f"are {pattern.split()[-2]}"],
            N_BAITS,
        )

    def _get_phrase(self, original_phrase: str, pattern: str) -> str:
        redata = re.compile(re.escape(pattern), re.IGNORECASE)
        phrase = redata.sub("_" * len(pattern), original_phrase)
        return phrase
