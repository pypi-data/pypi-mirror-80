from collections import defaultdict

from .. import config
from ..config import QuestionMode
from ..domain.data_converters import to_verb_question
from ..domain.lemma_data import LemmaData
from neo4j import DirectDriver
from neo4j import BoltStatementResult
from typing import List, Dict


class QuestionGetter:
    """
    Handles all the db operations related to user content management
    """

    def __init__(self, driver: DirectDriver, mode: str):
        """
        Initializes the neo4j db
        """
        self._driver = driver
        self.mode = mode
        self.mode_function_registry = {
            QuestionMode.N_QUESTIONS_MODE: self._get_n_questions,
            QuestionMode.N_QUESTIONS_PER_WORD_MODE: self._get_n_questions_per_word,
        }

    def get(self, user_id: str, lemma_list: List[str], n_questions: int, n_questions_per_word: int) -> Dict[str, List[LemmaData]]:
        with self._driver.session() as session:

            lemma_information = self._get_lemma_information(
                session, user_id, lemma_list
            )

            lemma_to_questions = defaultdict(list)
            for res in session.read_transaction(
                self.mode_function_registry[self.mode],
                user_id,
                list(lemma_information.keys()),
                n_questions,
                n_questions_per_word,
            ):
                content_rel_json = res[config.CONTENT_KEY]
                target_lemma = content_rel_json[config.LEMMA_KEY]
                content_rel_json[config.VERBGAMES_ITEMS_KEY][
                    config.LEMMA_CONJUGATIONS_KEY
                ] = lemma_information[target_lemma][config.LEMMA_CONJUGATIONS_KEY]
                verb_question = to_verb_question(content_rel_json)
                level = lemma_information[target_lemma][config.LEVEL_KEY]
                mastered = lemma_information[target_lemma][config.MASTERED_KEY]
                lemma_data = LemmaData(verb_question, level, mastered)
                lemma_to_questions[target_lemma].append(lemma_data)
            return lemma_to_questions

    def _get_lemma_information(self, session, user_id: str, lemma_list: List[str]) -> Dict:

        lemma_dict = {}
        for res in session.read_transaction(self._get_lemma_data, user_id, lemma_list):

            target_lemma = res[config.LEMMA_KEY]
            mastered = res[config.MASTERED_KEY]
            level = res[config.LEVEL_KEY]
            lemma_conjugations = res[config.LEMMA_CONJUGATIONS_KEY]

            lemma_dict[target_lemma] = {
                config.LEVEL_KEY: level,
                config.MASTERED_KEY: mastered,
                config.LEMMA_CONJUGATIONS_KEY: lemma_conjugations,
            }

        return lemma_dict

    @classmethod
    def _get_n_questions(
        cls, tx, user_id: str, lemma_list: List[str], n_questions: int, n_questions_per_word: int
    ) -> BoltStatementResult:

        return tx.run(
            cls.query_n_data_questions,
            user_id=user_id,
            lemma_list=lemma_list,
            n_questions=n_questions,
        )

    @classmethod
    def _get_n_questions_per_word(
        cls, tx, user_id: str, lemma_list: List[str], n_questions: int, n_questions_per_word: int
    ) -> BoltStatementResult:
        return tx.run(
            cls.query_n_data_questions_per_word,
            user_id=user_id,
            lemma_list=lemma_list,
            n_questions_per_word=n_questions_per_word,
        )

    @classmethod
    def _get_lemma_data(
        cls, tx, user_id: str, lemma_list: List
    ) -> BoltStatementResult:
        return tx.run(cls.query_lemma_data, user_id=user_id, lemma_list=lemma_list)
