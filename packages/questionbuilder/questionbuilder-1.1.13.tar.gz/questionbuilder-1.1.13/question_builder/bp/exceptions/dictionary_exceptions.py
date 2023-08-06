from .question_creator_exception import QuestionCreatorException


class WordNotInAntonymDictionary(QuestionCreatorException):
    pass


class WordNotInEnglishDefinitionsDictionary(QuestionCreatorException):
    pass


class WordNotInSpanishDefinitionsDictionary(QuestionCreatorException):
    pass


class WordNotInSoundsLikeDictionary(QuestionCreatorException):
    pass


class WordNotInIntruderDictionary(QuestionCreatorException):
    pass


class WordNotInMeansLikeDictionary(QuestionCreatorException):
    pass


class WordNotInMultiSynonymDictionary(QuestionCreatorException):
    pass


class WordNotInPartWordTypingDictionary(QuestionCreatorException):
    pass


class WordNotInRelNounDictionary(QuestionCreatorException):
    pass


class WordNotInPreSuffixDictionary(QuestionCreatorException):
    pass


class WordNotInMultisynonymDictionary(QuestionCreatorException):
    pass
