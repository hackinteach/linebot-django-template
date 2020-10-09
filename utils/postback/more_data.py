from dataclasses import dataclass

from utils.postback.action_meta import ActionData


@dataclass
class MoreActionData(ActionData):
    topic: str
    page: int
