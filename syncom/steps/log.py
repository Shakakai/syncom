from typing import Any
from .base import BaseStep


class LogStep(BaseStep):
    input_schema = None
    output_schema = None

    def __init__(self, label: str = "LogStep"):
        super().__init__()
        self.label = label

    async def run(self):
        print("-" * 80)
        print(self.label)
        print(self.input)
        self.output = self.input
