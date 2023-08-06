"""Text entry widgets."""

# pylint: disable=invalid-name,no-self-use

import logging
from typing import Union, Optional

import wx

from aio_wx_widgets.binding import Bindable, Binding
from aio_wx_widgets.widgets.validators.validators import IntValidator

_LOGGER = logging.getLogger(__name__)


class Entry(Bindable):
    """A general textctrl for any input.

    Inherits from Bindable as it
    """

    def __init__(
        self,
        binding: Binding,
        label: Union[None, int, str] = None,
        wx_ctrl=None,
        validator: wx.Validator = None,
    ):

        super().__init__(binding)
        self.value: Optional[int] = None

        self._label = label

        if wx_ctrl is None:
            self._txt = wx.TextCtrl()
        else:
            self._txt = wx_ctrl

        self._validator = validator
        self.ui_item = self._txt

    def _set_ui_value(self, value):
        self._txt.SetValue(str(value))

    def _get_ui_value(self):
        return self._txt.GetValue()

    def __call__(self, parent):
        args = dict({"parent": parent})
        if self._validator:
            args["validator"] = self._validator
        if self._label:
            args["value"] = str(self._label)

        self._txt.Create(**args)
        self._txt.Bind(wx.EVT_TEXT, self._on_ui_change)
        self._make_binding()

        return self


class IntEntry(Entry):
    """Textentry which only allows numerical values."""

    def __init__(self, binding: "Binding", label: Union[None, int, str] = None):
        super().__init__(binding=binding, label=label, validator=IntValidator())


def text_ctrl(
    label=None, parent=None, multiline=False, validator=wx.DefaultValidator,
):
    """Create a wx text control."""
    txt = wx.TextCtrl()
    style = 0
    if multiline:
        style = style | wx.TE_MULTILINE

    def _create(parent):
        args = {"style": style, "validator": validator}
        if label:
            args["value"] = str(label)

        txt.Create(parent, **args)
        return txt

    if parent:
        return _create(parent)
    return _create
