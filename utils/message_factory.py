from dataclasses import dataclass
from typing import List, Union

from django.core.paginator import Page, Paginator
from linebot.models import FlexSendMessage, BubbleContainer, BoxComponent, TextComponent, SeparatorComponent, \
    ButtonComponent, PostbackAction

QuestionComponent = List[Union[TextComponent, SeparatorComponent]]


@dataclass
class KnowledgeMessageFactory:
    topic: str

    def get_return_flex_message(self) -> FlexSendMessage:
        return FlexSendMessage()
