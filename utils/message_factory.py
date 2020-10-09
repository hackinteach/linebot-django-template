from dataclasses import dataclass
from typing import List, Union

from django.core.paginator import Page, Paginator
from linebot.models import FlexSendMessage, BubbleContainer, BoxComponent, TextComponent, SeparatorComponent, \
    ButtonComponent, PostbackAction

from knowledge.data_models import QuestionPool, KnowledgePool
from knowledge.models import Knowledge
from knowledge.serializer import KnowledgeSerializer

QuestionComponent = List[Union[TextComponent, SeparatorComponent]]


@dataclass
class KnowledgeMessageFactory:
    topic: str

    def get_return_flex_message(self, page_number: int = 1) -> FlexSendMessage:
        page: Page = self.get_paginated_topic_knowledge(page_number=page_number)
        questions: QuestionPool = KnowledgePool \
            .from_paginated_knowledge(page) \
            .get_question_pool()
        if page.has_next():
            message = self.from_question_with_page(questions=questions, page_number=page.next_page_number())
        else:
            message = self.from_questions_with_admin_contact(questions)
        return message

    def get_topic_knowledge(self) -> KnowledgeSerializer:
        kls = Knowledge.objects.filter(topic__name=self.topic)
        return KnowledgeSerializer(kls, many=True)

    def get_paginated_topic_knowledge(self,
                                      page_number: int,
                                      page_size: int = 10
                                      ) -> Page:
        knowledge: KnowledgeSerializer = self.get_topic_knowledge()
        paginator = Paginator(knowledge.data, page_size)
        page = paginator.get_page(page_number)
        return page

    def from_questions_with_admin_contact(self, questions: QuestionPool) -> FlexSendMessage:
        msg = self.from_questions(questions)
        msg.contents.footer = BoxComponent(
            layout='horizontal',
            spacing='md',
            contents=[
                ButtonComponent(
                    style='primary',
                    action=PostbackAction(
                        label='Contact Admin',
                        display_text='Contact Admin',
                        data=f"action=admin"
                    )
                )
            ]
        )
        return msg

    def from_questions(self, questions: QuestionPool) -> FlexSendMessage:
        question_comp = questions.get_text_components_with_separator()
        return FlexSendMessage(
            alt_text=f"Question for {self.topic}",
            contents=BubbleContainer(
                direction='ltr',
                header=BoxComponent(
                    layout='vertical',
                    contents=
                    [
                        TextComponent(
                            text=self.topic,
                            align='center',
                            weight='bold'),
                        BoxComponent(
                            layout='vertical',
                            margin='sm',
                            contents=[
                                TextComponent(
                                    text='Tap to select question',
                                    align='center'
                                )
                            ]
                        )
                    ]
                ),
                body=BoxComponent(
                    layout='vertical',
                    spacing='md',
                    contents=question_comp
                )
            )
        )

    def from_question_with_page(self, questions: QuestionPool, page_number: int) -> FlexSendMessage:
        msg: FlexSendMessage = self.from_questions(questions)
        msg.contents.footer = BoxComponent(
            layout='horizontal',
            spacing='md',
            contents=[
                ButtonComponent(
                    action=PostbackAction(
                        label='More',
                        display_text='More',
                        data=f"action=more|topic={self.topic}|page={page_number}"
                    )
                )
            ]
        )
        return msg
