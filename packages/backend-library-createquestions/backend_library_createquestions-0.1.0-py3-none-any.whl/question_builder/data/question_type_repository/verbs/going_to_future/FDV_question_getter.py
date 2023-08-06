from collections import defaultdict

from ...question_getter import QuestionGetter
from .going_to_future_affirmative_queries import GET_N_DATA_QUESTIONS
from .going_to_future_affirmative_queries import GET_N_DATA_QUESTIONS_PER_WORD
from .going_to_future_bait_content_queries import GET_CONTENT_BAITS
from .lemma_queries import GET_LEMMA_LIST_DATA
from question_builder.data import config
from question_builder.data.domain.data_converters import to_content
from question_builder.data.domain.data_converters import to_verb_question
from question_builder.data.domain.lemma_data import LemmaData
from question_builder.data.domain.content import Content
from neo4j import DirectDriver, Session
from neo4j import BoltStatementResult
from typing import Dict, List


class FDVQuestionGetter(QuestionGetter):
    code = "FDV"
    query_n_data_questions_per_word = GET_N_DATA_QUESTIONS_PER_WORD
    query_n_data_questions = GET_N_DATA_QUESTIONS
    query_lemma_data = GET_LEMMA_LIST_DATA
    query_baits = GET_CONTENT_BAITS

    def get(self, user_id: str, lemma_list: List[str], n_questions: int, n_questions_per_word: int) -> Dict[str, List[LemmaData]]:

        lemma_to_lemma_data_list = super().get(
            user_id, lemma_list, n_questions, n_questions_per_word
        )

        self._append_bait_content(user_id, lemma_to_lemma_data_list)

        return lemma_to_lemma_data_list

    def _append_bait_content(self, user_id: str, lemma_to_lemma_data_list: Dict[str, List[LemmaData]]):
        with self._driver.session() as session:
            for lemma, lemma_data_list in lemma_to_lemma_data_list.items():
                for lemma_data in lemma_data_list:
                    bait_content = self._get_no_going_content(session, user_id, lemma)
                    lemma_data.data_question.bait_content = bait_content

    def _get_no_going_content(self, session: Session, user_id: str, lemma: str) -> Content:

        for res in session.read_transaction(
            self._get_no_going_content_tx, user_id, lemma
        ):
            content_rel_json = res[config.CONTENT_KEY]

            return to_content(content_rel_json[config.CONTENT_KEY])

    @classmethod
    def _get_no_going_content_tx(cls, tx, user_id: str, lemma: str) -> BoltStatementResult:
        return tx.run(cls.query_baits, user_id=user_id, lemma=lemma)
