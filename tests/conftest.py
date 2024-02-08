import os
from typing import Dict, ClassVar

import pytest
from syncom import AIModel, LLMStep, RunnableConfig, configure_engine, TypedTemplate
from pydantic import BaseModel, Field


def pytest_configure(config):
    current_directory = os.path.dirname(os.path.abspath(__file__))
    test_data_dir = os.path.join(current_directory, "test_data")
    configure_engine(dirs=[test_data_dir])


@pytest.fixture(name="openai_key")
def get_openai_key() -> str:
    return os.getenv("OPENAI_API_KEY")


@pytest.fixture(name="config")
def get_config() -> RunnableConfig:
    return RunnableConfig()


@pytest.fixture(name="model")
def fixture_model(openai_key: str) -> AIModel:
    return AIModel(
        name="gpt-4",
        api_key=openai_key,
    )


@pytest.fixture(name="prompt")
def get_prompt_value():
    return {
        "system": "You are an AI assistant. You must respond to questions and follow all instructions.",
        "prompt": "Please respond with just 'Hi' to this message"
    }


@pytest.fixture(name="configured_completion")
def fixture_configured_completion(model: AIModel) -> LLMStep:
    return LLMStep(model, {})


class IOScheme(BaseModel):
    response: str = Field(description="LLM response to message here.")


@pytest.fixture(name="io")
def get_io() -> Dict[str, str]:
    return {"response": "Hi"}
