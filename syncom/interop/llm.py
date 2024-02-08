from typing import Type

import instructor
import httpx
import litellm
from instructor.patch import wrap_chatcompletion
from litellm import acompletion
from openai import OpenAI

from syncom import AIModel, RunnableConfig, PromptValue
from pydantic import BaseModel

completion = wrap_chatcompletion(func=acompletion)
# client = instructor.patch(AsyncOpenAI())


#async def completion(*args, **kwargs):
#    return client.chat.completions.create(*args, **kwargs)


async def llm_request(
        model: AIModel,
        config: RunnableConfig,
        response_model: Type[BaseModel],
        prompt: PromptValue
) -> BaseModel:
    if not config.ssl_verify:
        litellm.client_session = httpx.Client(verify=False)

    if config.verbose:
        litellm.set_verbose = True

    if model.headers:
        litellm.headers = model.headers

    if not isinstance(prompt, dict):
        prompt = prompt.dict()

    req = {
        "model": model.name,
        "response_model": response_model,
        "messages": [
            {
                "role": "system",
                "content": prompt["system"],
            },
            {
                "role": "user",
                "content": prompt["prompt"],
            },
        ],
        "max_retries": config.max_retries,
    }
    if model.organization:
        req["organization"] = model.organization
    if model.api_base:
        req["api_base"] = model.api_base

    response = await completion(**req)

    if not config.ssl_verify:
        litellm.client_session = None  # reset to default. Might be unnecessary. Evaluate later.

    if model.headers:
        litellm.headers = None  # reset to default. Might be unnecessary. Evaluate later.

    if config.verbose:
        litellm.set_verbose = False

    return response
