from typing import List, Union, Optional

from linebot.models import SendMessage, TextSendMessage

from utils.message_factory import KnowledgeMessageFactory
from utils.postback import MenuActionData
from utils.postback.action_meta import ActionData
from utils.postback.ask_data import AskActionData
from utils.postback.more_data import MoreActionData

ACTION_TOKEN = "|"


class PostbackParser:
    @staticmethod
    def get_return_message(data: str, user_id: Optional[str]) -> Union[List[SendMessage], SendMessage]:
        action = ActionParser.from_str(data)
        print("Postback received: ", action)
        if isinstance(action, MenuActionData):
            factory = KnowledgeMessageFactory(topic=action.topic)
            message = factory.get_return_flex_message(page_number=1)
        elif isinstance(action, MoreActionData):
            factory = KnowledgeMessageFactory(action.topic)
            message = factory.get_return_flex_message(page_number=action.page)
        else:
            message = TextSendMessage(text=f"Invalid request, action is {action}")
        print('Returning ', message)
        return message


class ActionParser:
    @staticmethod
    def from_str(data: str) -> ActionData:
        """
        Parse `data` from rich menu postback action
        :param data: of the form `key1=value1&key2=value2...`
        :return: ActionData inheritance
        """
        key_value_list = data.split(ACTION_TOKEN)
        kv_map = dict()
        for st in key_value_list:
            k, v = st.split("=")
            kv_map[k] = v
        action = kv_map['action']
        if action == 'menu':
            return MenuActionData(**kv_map)
        elif action == 'ask':
            return AskActionData(**kv_map)
        elif action == 'more':
            return MoreActionData(**kv_map)
        else:
            return ActionData(action=kv_map['action'])
