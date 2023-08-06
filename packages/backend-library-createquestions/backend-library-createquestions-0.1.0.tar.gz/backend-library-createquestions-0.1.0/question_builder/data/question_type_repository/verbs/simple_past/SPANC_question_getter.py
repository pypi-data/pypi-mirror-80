from ...question_getter import QuestionGetter
from .lemma_queries import GET_LEMMA_LIST_DATA
from .simple_past_negative_queries import GET_N_DATA_QUESTIONS
from .simple_past_negative_queries import GET_N_DATA_QUESTIONS_PER_WORD


class SPANCQuestionGetter(QuestionGetter):
    code = "SPANC"
    query_n_data_questions_per_word = GET_N_DATA_QUESTIONS_PER_WORD
    query_n_data_questions = GET_N_DATA_QUESTIONS
    query_lemma_data = GET_LEMMA_LIST_DATA
