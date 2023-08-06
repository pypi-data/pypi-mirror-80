from ..config import QuestionMode
from neo4j import DirectDriver
from neo4j import BoltStatementResult
from typing import List
from typing import Dict
from question_builder.data.domain.lemma_data import LemmaData
from .question_getter import QuestionGetter


class QuestionTypeRepository:
    """
    Handles all the db operations related to user content management
    """

    def __init__(self, driver: DirectDriver):
        """
        Initializes the neo4j db
        """
        self._driver = driver
        self._registry = {}

    def get_random_questions(
        self,
        code: str,
        user_id: str,
        lemmas: List[str],
        mode: str = QuestionMode.N_QUESTIONS_PER_WORD_MODE,
        n_questions: int = None,
        n_questions_per_word: int = None,
    ) -> Dict[str, List[LemmaData]]:
        question_getter = self._registry[code]

        return question_getter(self._driver, mode).get(
            user_id, lemmas, n_questions, n_questions_per_word
        )

    def register_question_getter(self, code: str, question_getter: QuestionGetter):
        self._registry[code] = question_getter
