from typing import List, ClassVar
from pydantic import BaseModel, Field
from syncom import TypedTemplate

CHAIN_OF_THOUGHT_PROMPT = """
# Instructions
{{ instructions }}

# Examples
{% for example in examples %}
## Example {{ loop.index }}
### Question
{{ example.question }}
### Answer
{{ example.answer }}
{% endfor %}

# Question
{{ question }}
"""


class QuestionAnswerPair(BaseModel):
    question: str = Field(required=True, description="The question to ask the user")
    answer: str = Field(required=True, description="The answer to the question")


class ChainOfThoughtTemplate(TypedTemplate):
    template_string: ClassVar[str] = CHAIN_OF_THOUGHT_PROMPT

    instructions: str = Field(required=True, description="The instructions for the user to follow.")
    examples: List[QuestionAnswerPair] = Field(
        required=True,
        description="Examples of how to answer questions for the user"
    )
    question: str = Field(required=True, description="The question to ask the user")
