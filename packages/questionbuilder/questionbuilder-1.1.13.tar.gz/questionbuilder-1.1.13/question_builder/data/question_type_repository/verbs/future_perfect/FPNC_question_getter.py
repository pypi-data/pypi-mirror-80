from ...question_getter import QuestionGetter
from .future_perfect_negative_queries import GET_N_DATA_QUESTIONS
from .future_perfect_negative_queries import GET_N_DATA_QUESTIONS_PER_WORD
from .lemma_queries import GET_LEMMA_LIST_DATA


class FPNCQuestionGetter(QuestionGetter):
    code = "FPNC"
    query_n_data_questions_per_word = GET_N_DATA_QUESTIONS_PER_WORD
    query_n_data_questions = GET_N_DATA_QUESTIONS
    query_lemma_data = GET_LEMMA_LIST_DATA
