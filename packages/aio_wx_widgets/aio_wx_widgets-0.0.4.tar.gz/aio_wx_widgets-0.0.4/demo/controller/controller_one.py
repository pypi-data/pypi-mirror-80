import logging
from random import randint

from events import Events

from aio_wx_widgets.controller import BaseController
from demo.windows import second_window

_LOGGER = logging.getLogger(__name__)


class ControllerOne(BaseController):
    def __init__(self, model):
        self.value_1: int = 0
        self.a_string_value = "A certain string"
        super().__init__(model)

        self.add_to_log = Events()

    def _add_to_log(self, data: str):
        self.add_to_log.on_change(data)

    async def open_other_window(self):
        """Open a second window."""
        second_window.SecondWindow().Show()
        # _second_window.Show()
        _LOGGER.debug("Closed second window ?")

    async def set_value(self):
        val = randint(1, 100)
        _LOGGER.debug("Setting bound property to %s", val)
        self.value_1 = val
