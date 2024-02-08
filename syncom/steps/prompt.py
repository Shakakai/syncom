from typing import Any, Dict, Union, Type

from syncom import TypedTemplate
from .base import BaseStep, PromptValue


class StaticPromptStep(BaseStep):

    def __init__(self, system: str, prompt: str):
        super().__init__()
        self.input_schema = None
        self.output_schema = PromptValue
        self.output = PromptValue(system=system, prompt=prompt)

    def run(self):
        pass


TemplateOrString = Union[Type[TypedTemplate], str]


class TemplatePromptStep(BaseStep):

    def __init__(
            self,
            system: TemplateOrString,
            prompt: TemplateOrString,
            initial_context=None
    ):
        super().__init__()
        if initial_context is None:
            initial_context = {}
        self.input_schema = None
        self.output_schema = PromptValue
        self.system = system
        self.prompt = prompt
        self.context = initial_context

    def _render(self, template_obj: TemplateOrString, context: Dict[str, Any]) -> str:
        if isinstance(template_obj, str):
            return template_obj
        template = template_obj(**context)
        return template.render()

    async def run(self):
        context = {**self.context, **self.input}
        prompt = self._render(self.prompt, context)
        system = self._render(self.system, context)
        self.output = PromptValue(system=system, prompt=prompt)
