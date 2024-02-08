from syncom.runnable import Runnable
from pydantic import BaseModel


class PromptValue(BaseModel):
    system: str
    prompt: str


class BaseStep(Runnable):
    pass
