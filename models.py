from pydantic import BaseModel
from typing import List, Optional

class Email(BaseModel):
    id: int
    subject: str
    body: str
    sender: str
    priority_hint: Optional[str] = None
    deadline: Optional[str] = None

class Observation(BaseModel):
    inbox: List[Email]
    history: List[str]
    last_action_error: Optional[str] = None
    step_count: int = 0

class Action(BaseModel):
    type: str
    email_id: int
    label: Optional[str] = None
    response: Optional[str] = None

class Reward(BaseModel):
    value: float
    feedback: str
