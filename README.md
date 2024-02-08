# Syncom Library

Syncom is a Python library designed to assist in the creation and execution of pipelines for AI models. 
It provides a set of classes and functions to define steps in a pipeline, create a pipeline, and run it.

## Features

- Pipeline Creation: Define a sequence of steps to be executed in a pipeline.
- Step Definition: Define individual steps in a pipeline, such as data input, logging, and AI model execution.
- Pipeline Execution: Run a defined pipeline and get the result.

## Requirements

- Python 3.7 or later
- `pydantic`
- litellm
- instructor

## Usage

To use this library, you need to define the steps of your pipeline, create the pipeline, and then run it. 
Here's a basic usage example:

```python
import asyncio
from pydantic import Field
from syncom import (
    TypedTemplate,
    TemplatePromptStep,
    LLMStep,
    RunnableConfig,
    run_pipeline,
    make_pipeline
)

class PingTemplate(TypedTemplate):
    template_string = """
    # Instructions
    Respond to the user command listed below using the following rules.
    When the user command is "ping", respond with "pong".
    When the user command is "pong", respond with "ping".
    
    # User Command
    {{ command }}
    """
    command: str = Field(enum=["ping", "pong"])

    
class PongResult(BaseModel):
    command: str = Field(
        description="Response command from AI" 
        enum=["ping", "pong"]
    )

# Define the steps
steps = (
    TemplatePromptStep(PingTemplate),
    LogStep("Ping Template"),
    LLMStep(model, PongResult)
)

# Create the pipeline
pipeline = make_pipeline(RunnableConfig(), *steps)

# Run the pipeline
async def main(self):
    global pipeline
    input_data = {"command": "ping"}
    output: PongResult = await run_pipeline(pipeline, input_data)
    print(f"Output Command: {output.command}")

if __name__ == "__main__":
    asyncio.run(main())

```

This will create a pipeline that generates a prompt from a template and then runs the prompt against GPT-4 resulting in a typed PongResult response.

## Contributing

Contributions are welcome. Please open an issue to discuss your ideas or submit a Pull Request with your changes.

## License

[MIT](https://choosealicense.com/licenses/mit/)
