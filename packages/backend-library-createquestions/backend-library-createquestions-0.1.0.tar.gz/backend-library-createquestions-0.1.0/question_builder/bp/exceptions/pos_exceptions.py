from .question_creator_exception import QuestionCreatorException


class WordNotAdjective(QuestionCreatorException):
    pass


class WordNotVerb(QuestionCreatorException):
    pass


class NotConjugation(QuestionCreatorException):
    pass


class InvalidMorpheme(QuestionCreatorException):
    pass


class WordNotNoun(QuestionCreatorException):
    pass


class WordHasNotValidPos(QuestionCreatorException):
    pass
