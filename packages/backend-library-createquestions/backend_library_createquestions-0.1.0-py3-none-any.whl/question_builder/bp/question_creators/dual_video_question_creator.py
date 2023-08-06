import random

from question_builder.bp.question_creators.question_creator import QuestionCreator
from question_builder.bp.questions.question import GETYARN_KEY
from question_builder.bp.questions.question import IMAGE
from question_builder.bp.questions.question import Question
from question_builder.bp.questions.question import TWITTER_KEY
from question_builder.bp.questions.question import VIDEO
from question_builder.data import Content
from typing import List

PROBABILITY_OF_SHUFFLING_OPTIONS_IN_DUAL_VIDEO = 0.5


class MediasList:
    def __init__(self, 
                links: List[str], 
                media_types: List[str], 
                phrases: List[str], 
                correct_values: List[bool]):
        self.links = links
        self.media_types = media_types
        self.phrases = phrases
        self.correct_values = correct_values


class DualVideoQuestionCreator(QuestionCreator):
    def _get_medias(self, contents: List[Content]) -> MediasList:
        """
        Gets links and media types lists depending on type
        """
        links = []
        medias = []
        phrases = []
        correct_values = []
        contents = self._reorder_content(contents)
        for content in contents:
            if content.source == GETYARN_KEY:
                link_mp4 = f"http://media.wordbox.ai/{content.interest_label.lower()}/{content.id}"
                links.append(link_mp4)
                medias.append(VIDEO)
            if content.source == TWITTER_KEY:
                link_jpg = content.image_link
                links.append(link_jpg)
                medias.append(IMAGE)
            phrases.append(content.phrase)
        number_of_contents = len(contents)
        correct_values = [
            False if index != self.correct_option_index else True
            for index in range(0, number_of_contents)
        ]
        return MediasList(links, medias, phrases, correct_values)

    def _reorder_content(self, contents: List[Content]) -> List[Content]:
        correct_option = contents[0]
        if random.random() < PROBABILITY_OF_SHUFFLING_OPTIONS_IN_DUAL_VIDEO:
            random.shuffle(contents)
        self.correct_option_index = contents.index(correct_option)
        return contents
