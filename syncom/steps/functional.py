from typing import Callable, Any, Optional, Dict

from .base import BaseStep


class FunctionalStep(BaseStep):
    """
    This step is used to complete the LLM process. It is used to
    complete the LLM process and to generate the final output.
    """

    input_schema = None
    output_schema = None

    def __init__(self, func: Callable[[Any, Optional[Dict[str, Any]]], Any], context: Optional[Any]):
        super().__init__()
        self._func = func
        self._context = context

    async def run(self):
        self.output = await self._func(self.input, self._context)
