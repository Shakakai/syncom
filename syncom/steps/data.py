from typing import Any

from .base import BaseStep


class StaticDataStep(BaseStep):

    def __init__(self, data: Any):
        self._data = data
        super().__init__()

    async def run(self):
        self.output = self._data
