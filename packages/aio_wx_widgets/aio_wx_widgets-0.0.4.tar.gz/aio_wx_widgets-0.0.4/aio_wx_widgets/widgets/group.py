"""Group layout item. Draws a line around children and sets a title."""


import logging

import wx

from aio_wx_widgets.sizers import SizerMixin

_LOGGER = logging.getLogger(__name__)


class Group(SizerMixin):
    """A Group widget.

    +--<LABEL>-------------+
    |                      |
    |  - Widget 1          |
    |  - Widget 2          |
    |                      |
    +----------------------+

    """

    default_sizer_margin = 20

    def __init__(self, label, **kwargs):
        """Init.

        Args:
            label:
        """
        self._label = label
        self._extra_bottom_border = 10
        # if KEY_PLATFORM == KEY_LINUX:
        #     self._extra_bottom_border = 50
        self._sizer = wx.BoxSizer(wx.VERTICAL)
        self.ui_item = wx.StaticBox()
        kwargs["sizer"] = self._sizer
        super().__init__()
        self._bottom_border = 1

    def __call__(self, parent):
        """Call this class as a function.

        Args:
            parent: The parent of this ui item.

        """
        self.ui_item.Create(parent, label=self._label)

        top, other = self.ui_item.GetBordersForSizer()
        self._bottom_border = other + self._extra_bottom_border
        self._sizer.AddSpacer(top + 5)
        self.ui_item.SetSizer(self._sizer)
        return self

    def __enter__(self):
        """Enter context manager."""
        return self

    def __exit__(self, *args):
        """Exit context manager."""
        self._finish()

    def _finish(self):
        self._sizer.AddSpacer(self._bottom_border)
