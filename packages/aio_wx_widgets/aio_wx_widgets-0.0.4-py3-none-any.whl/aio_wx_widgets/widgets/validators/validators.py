"""Validators"""

# todo: Rethink this.

import logging
import string

import wx

_LOGGER = logging.getLogger(__name__)

# pylint: disable=invalid-name,no-self-use


class IntValidator(wx.Validator):
    """Validator."""

    def __init__(self):
        """Init."""
        wx.Validator.__init__(self)
        self.Bind(wx.EVT_CHAR, self._on_char)

    def Clone(self):
        """Clone."""
        return IntValidator()

    def _on_char(self, event):
        value = event.GetKeyCode()
        if value < wx.WXK_SPACE or value == wx.WXK_DELETE or value > 255:
            event.Skip()
            return
        if chr(value) in string.digits:
            event.Skip()
            return
        return

    def Validate(self, win):
        """Validate."""
        ctrl = self.GetWindow()
        value = ctrl.GetValue()
        try:
            int(value)
        except ValueError:
            return False
        return True
