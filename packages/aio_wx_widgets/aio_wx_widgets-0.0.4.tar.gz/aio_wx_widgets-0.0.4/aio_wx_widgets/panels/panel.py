"""Panel. Sits in a frame. Holds widgets."""

import logging

import wx

# pylint: disable=unused-import
from aio_wx_widgets import type_annotations as T
from aio_wx_widgets.sizers import PanelMixin, SizerMixin

_LOGGER = logging.getLogger(__name__)


class SimplePanel(PanelMixin, SizerMixin):
    """A simple panel."""

    def __init__(self, parent, **kwargs):
        """Init."""
        self.ui_item = wx.Panel(parent)
        super().__init__()

        self._sizer = wx.BoxSizer(wx.VERTICAL)
        self.ui_item.SetSizer(self._sizer)

    @property
    def controller(self) -> "T.BaseController":
        raise NotImplementedError()
