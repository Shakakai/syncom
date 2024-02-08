from typing import Generic, TypeVar, Type
from pydantic import BaseModel

from syncom.interop.llm import llm_request
from .base import BaseStep, PromptValue
from syncom import AIModel


class LLMStep(BaseStep):
    """
    This step is used to complete the LLM process. It is used to
    complete the LLM process and to generate the final output.
    """

    input_schema = PromptValue
    output_schema = None

    def __init__(self, model: AIModel, response_model: Type[BaseModel]):
        self._model = model
        self._response_model = response_model

    async def run(self):
        response = await llm_request(
            model=self._model,
            config=self._config,
            response_model=self._response_model,
            prompt=self.input
        )
        self.output = response
