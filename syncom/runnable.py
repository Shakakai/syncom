from pydantic import BaseModel, Field


class RunnableConfig(BaseModel):
    verbose: bool = Field(default=False, description="Whether to run the pipeline in verbose mode.")
    max_retries: int = Field(
        default=3,
        description="The maximum number of retries for a step in the pipeline."
    )
    #is_async: bool = Field(
    #    default=False,
    #    description="Whether to run the pipeline asynchronously."
    #) Not supporting this yet.
    ssl_verify: bool = Field(
        description="Whether to verify the SSL certificate of the model provider.",
        default=True
    )


class Runnable:

    def __init__(self):
        self.input_schema = None
        self.output_schema = None
        self._input = None
        self._output = None
        self._config = None

    @property
    def config(self) -> RunnableConfig:
        return self._config

    @config.setter
    def config(self, value: RunnableConfig):
        self._config = value

    @property
    def input(self):
        return self._input

    @input.setter
    def input(self, value):
        if (self.input_schema
                and hasattr(self.input_schema, "model_validate")
                and not self.input_schema.model_validate(value)):
            raise Exception("Invalid input for this Runnable.")
        self._input = value

    @property
    def output(self):
        return self._output

    @output.setter
    def output(self, value):
        if (self.output_schema
                and hasattr(self.output_schema, "model_validate")
                and not self.output_schema.model_validate(value)):
            raise Exception("Invalid output for this Runnable.")
        self._output = value

    async def run(self):
        raise NotImplementedError("run method must be implemented by subclass")
