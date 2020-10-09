from dataclasses import dataclass

from utils.postback.action_meta import ActionData


@dataclass
class MenuActionData(ActionData):
    topic: str
