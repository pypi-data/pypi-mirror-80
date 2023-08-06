from ...question_getter import QuestionGetter
from .lemma_queries import GET_LEMMA_LIST_DATA
from .past_continuous_affirmative_queries import GET_N_DATA_QUESTIONS
from .past_continuous_affirmative_queries import GET_N_DATA_QUESTIONS_PER_WORD


class PACCQuestionGetter(QuestionGetter):
    code = "PACC"
    query_n_data_questions_per_word = GET_N_DATA_QUESTIONS_PER_WORD
    query_n_data_questions = GET_N_DATA_QUESTIONS
    query_lemma_data = GET_LEMMA_LIST_DATA
