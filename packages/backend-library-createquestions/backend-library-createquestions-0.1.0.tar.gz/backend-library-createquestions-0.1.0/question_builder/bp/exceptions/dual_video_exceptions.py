from .question_creator_exception import QuestionCreatorException


class DefinitionNotFoundException(QuestionCreatorException):
    pass


class BaitNotFoundException(QuestionCreatorException):
    pass


class MinimalPairNotFoundException(QuestionCreatorException):
    pass


class SpanishBaitsNotFoundException(QuestionCreatorException):
    pass


class ContentNotFoundException(QuestionCreatorException):
    pass


class MaximumLengthExceeded(QuestionCreatorException):
    pass
