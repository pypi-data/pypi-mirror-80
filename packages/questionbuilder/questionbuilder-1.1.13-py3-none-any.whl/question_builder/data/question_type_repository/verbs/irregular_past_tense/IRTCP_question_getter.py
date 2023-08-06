from ...question_getter import QuestionGetter
from .irregular_past_tense_affirmative_queries import GET_N_DATA_QUESTIONS
from .irregular_past_tense_affirmative_queries import GET_N_DATA_QUESTIONS_PER_WORD
from .lemma_queries import GET_LEMMA_LIST_DATA


class IRTCPQuestionGetter(QuestionGetter):
    code = "IRTCP"
    query_n_data_questions_per_word = GET_N_DATA_QUESTIONS_PER_WORD
    query_n_data_questions = GET_N_DATA_QUESTIONS
    query_lemma_data = GET_LEMMA_LIST_DATA
