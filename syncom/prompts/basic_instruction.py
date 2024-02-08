from typing import ClassVar
from pydantic import Field
from template import TypedTemplate

BASIC_PROMPT = """
# Instructions
{{ instructions }}
"""


class BasicInstructionTemplate(TypedTemplate):
    template_string: ClassVar[str] = BASIC_PROMPT

    instructions: str = Field(required=True, description="The instructions for the user to follow.")
