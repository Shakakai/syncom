from typing import List, Any, ClassVar

from pydantic import Field

from .chain_of_thought import QuestionAnswerPair
from syncom import TypedTemplate

AGENT_PROMPT = """
# Instructions
{{ instructions }}

# Examples
{% for example in examples %}
## Example {{ forloop.counter }}
### Question
{{ example.question }}
### Answer
{{ example.answer }}
{% endfor %}

{% if tool_results %}
# Tool Results
{{ tool_results|pprint }}
{% endif %}

# Question
{{ question }}
"""


class AgentTemplate(TypedTemplate):
    template_string: ClassVar[str] = AGENT_PROMPT

    instructions: str = Field(required=True, description="The instructions for the user to follow.")
    examples: List[QuestionAnswerPair] = Field(
        required=True,
        description="Examples of how to answer questions for the user"
    )
    question: str = Field(required=True, description="The question to ask the user")
    tool_results: Any = Field(required=False, description="The results of the tool")
