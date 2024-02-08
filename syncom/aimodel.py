from typing import Optional, Dict
from pydantic import BaseModel, Field


class AIModel(BaseModel):
    name: str = Field(
        description="The name of the model using the naming conventions of LiteLLM. "
                    "More info here: https://docs.litellm.ai/docs/providers"
    )
    api_key: str = Field(description="The API key for the model provider.")
    organization: Optional[str] = Field(
        description="The organization ID for the model provider.",
        default=None
    )
    api_base: Optional[str] = Field(
        description="If using a Proxy or 3rd Party vendor, this is the base url for requests.",
        default=None
    )
    headers: Optional[Dict[str, str]] = Field(
        description="Additional headers to include with the requests. "
                    "More info here: https://docs.litellm.ai/docs/providers/openai#using-helicone-proxy-with-litellm",
        default=None
    )
