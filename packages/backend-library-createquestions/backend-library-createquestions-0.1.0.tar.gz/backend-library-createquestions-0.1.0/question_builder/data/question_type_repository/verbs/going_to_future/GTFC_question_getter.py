from ...question_getter import QuestionGetter
from .going_to_future_affirmative_queries import GET_N_DATA_QUESTIONS
from .going_to_future_affirmative_queries import GET_N_DATA_QUESTIONS_PER_WORD
from .lemma_queries import GET_LEMMA_LIST_DATA


class GTFCQuestionGetter(QuestionGetter):
    code = "GTFC"
    query_n_data_questions_per_word = GET_N_DATA_QUESTIONS_PER_WORD
    query_n_data_questions = GET_N_DATA_QUESTIONS
    query_lemma_data = GET_LEMMA_LIST_DATA
