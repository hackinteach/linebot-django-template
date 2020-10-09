from dataclasses import dataclass

from utils.postback.action_meta import ActionData


@dataclass
class AskActionData(ActionData):
    knowledge_id: int
