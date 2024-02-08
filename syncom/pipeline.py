from typing import Any, Optional

from syncom.runnable import Runnable, RunnableConfig


class Pipeline(Runnable):
    def __init__(self, *steps):
        self._steps = steps

        super().__init__()

        if self.input_schema is None:
            self.input_schema = steps[0].input_schema
        if self.output_schema is None:
            self.output_schema = steps[-1].output_schema

    async def run(self):
        next_input = self.input
        for step in self._steps:
            step.config = self.config
            step.input = next_input
            await step.run()
            next_input = step.output
        self.output = next_input


def make_pipeline(config: RunnableConfig, *steps):
    pipeline = Pipeline(*steps)
    pipeline.config = config
    return pipeline


async def run_pipeline(pipeline: Pipeline, pipeline_input: Optional[Any] = None):
    pipeline.input = pipeline_input
    await pipeline.run()
    return pipeline.output
