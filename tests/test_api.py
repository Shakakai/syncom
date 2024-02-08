from typing import List, ClassVar

from .conftest import IOScheme
from syncom import (
    Pipeline,
    LogStep,
    RunnableConfig,
    AIModel,
    LLMStep,
    Runnable,
    run_pipeline,
    make_pipeline,
    StaticDataStep,
    PromptValue,
    TemplatePromptStep,
    TypedTemplate
)
from pydantic import BaseModel, Field


def test_llm_completion(
        config: RunnableConfig,
        prompt: PromptValue,
        model: AIModel
):
    steps = (
        StaticDataStep(prompt),
        LLMStep(model, IOScheme)
    )
    pipeline = make_pipeline(config, *steps)
    result = run_pipeline(pipeline)
    assert result.response == "Hi"


def test_llm_prompt_pipeline(config: RunnableConfig, model: AIModel):
    class CodeOutput(BaseModel):
        code: str = Field(description="Generated code to solve the problem.")
        tests: List[str] = Field(description="Unit tests to prove the code works as expected.")

    class CodePrompt(TypedTemplate):
        template_string: ClassVar[str] = (
            "Generate {{ language }} code to solve the following problem: {{ problem }}.\n "
            "You must include unit tests to prove the code works as expected. "
            "There must be at least 3 tests.")
        language: str = Field(description="Programming language to use.", required=True)
        problem: str = Field(description="Problem to solve.", required=True)

    steps = (
        StaticDataStep({
            "language": "python",
            "problem": "Find the sum of all the multiples of 3 or 5 below 1000."
        }),
        TemplatePromptStep(
            "You are an AI assistant. You must respond to questions and follow all instructions.",
            CodePrompt
        ),
        LLMStep(model, CodeOutput)
    )
    pipeline = make_pipeline(config, *steps)
    result = run_pipeline(pipeline)
    assert CodeOutput.model_validate(result)


def test_log_pipeline(io: IOScheme):
    log_step = LogStep()
    pipeline = Pipeline(log_step)
    pipeline.input_schema = IOScheme
    pipeline.output_schema = IOScheme

    pipeline.config = RunnableConfig()
    pipeline.input = io
    pipeline.run()
    assert pipeline.output == io


def test_quick_pipeline_creation(io: IOScheme):
    log_step = LogStep()
    pipeline = make_pipeline(
        RunnableConfig(),
        log_step
    )
    output = run_pipeline(pipeline, io)
    assert output == io
