from ..config import QuestionMode


class QuestionTypeRepository:
    """
    Handles all the db operations related to user content management
    """

    def __init__(self, driver):
        """
        Initializes the neo4j db
        """
        self._driver = driver
        self._registry = {}

    def get_random_questions(
        self,
        code,
        user_id,
        lemmas,
        mode=QuestionMode.N_QUESTIONS_PER_WORD_MODE,
        n_questions=None,
        n_questions_per_word=None,
    ):
        question_getter = self._registry[code]

        return question_getter(self._driver, mode).get(
            user_id, lemmas, n_questions, n_questions_per_word
        )

    def register_question_getter(self, code, question_getter):
        self._registry[code] = question_getter
