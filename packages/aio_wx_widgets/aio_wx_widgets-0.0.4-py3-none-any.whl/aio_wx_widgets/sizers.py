"""Sizer and Layout tooling."""

import collections
import logging
from enum import Enum
from typing import List, Tuple, Optional, Union

import wx

# pylint: disable=unused-import
from aio_wx_widgets import type_annotations as T
from aio_wx_widgets.binding import Binding

_LOGGER = logging.getLogger(__name__)


class AlignHorizontal(Enum):
    """Horizontal alignment options."""

    left = wx.ALIGN_LEFT
    right = wx.ALIGN_RIGHT
    center = wx.ALIGN_CENTER_HORIZONTAL


def _make_window(item: wx.Window, margins: List[Tuple[int, int]]):
    val = margins[0][1]
    for margin in margins[1:]:
        val = val | margin[1]

    new_sizer = wx.BoxSizer()
    margin_value = margins[0][0]
    new_sizer.Add(item, 1, val, margin_value)
    return new_sizer


def _margin_wrapper(item, margins: List[Tuple[int, int]]) -> wx.Window:
    if len(margins) == 0:
        return item

    first = margins.pop(0)

    values = [first]
    for idx, _ in enumerate(margins):
        if margins[idx][0] == first[0]:
            values.append(margins.pop(idx))

    item = _make_window(item, values)
    return _margin_wrapper(item, margins)


def _align_item(
    item: Union[wx.Window, wx.BoxSizer],
    current_sizer_orientation,
    alignment: Optional["AlignHorizontal"],
    current_layout: int,
) -> Tuple[Union[wx.Window, wx.BoxSizer], int]:

    if alignment is None:
        return item, current_layout | wx.EXPAND

    # wx_alignment = _get_wx_alignment(alignment)
    if not current_sizer_orientation == wx.HORIZONTAL:
        return item, current_layout | alignment.value

    sizer = wx.BoxSizer(orient=wx.VERTICAL)
    sizer.Add(item, 0, alignment.value, 0)
    return sizer, current_layout


def _add(
    item,
    parent,
    sizer,
    weight,
    margin,
    default_margin,
    create,
    align_horizontal: Optional[AlignHorizontal],
) -> object:
    if create:
        # this is an item which is part of the aio_wx_widgets family.
        # It is assumed it has the ui_item property.
        item = item(parent)
        ui_item = item.ui_item
    else:
        # this is assumed to be a "normal" wx-widgets item.
        ui_item = item
    if margin is None:
        margin = default_margin
    elif isinstance(margin, collections.Sequence):
        margins = [
            (margin[0], wx.LEFT),
            (margin[1], wx.RIGHT),
            (margin[2], wx.TOP),
            (margin[3], wx.BOTTOM),
        ]
        ui_item = _margin_wrapper(ui_item, margins)
        margin = 0

    layout = wx.ALL

    ui_item, layout = _align_item(ui_item, sizer.Orientation, align_horizontal, layout)
    # if align_horizontal is not None:
    #     wx_alignment = _get_wx_alignment(align_horizontal)
    #
    # if align_horizontal is not None and sizer.Orientation == wx.HORIZONTAL:
    #     ui_item = _align_wrapper(ui_item,align_horizontal)
    # else:
    #     layout = layout | _get_wx_alignment(hor)
    sizer.Add(ui_item, weight, layout, margin)

    return item


class SizerMixin:
    """Mixin providing sizer functionality"""

    default_sizer_margin = 5

    def add(
        self,
        item,
        weight=0,
        layout=wx.EXPAND | wx.ALL,
        margin=None,
        create=True,
        align_horizontal: Optional[AlignHorizontal] = None,
    ):
        """Add an item to this panel

        Args:
            item: the item to be added.
            weight: The relative weight to other items in this container and the size
                it should take
            layout: The layout
            margin: None to use default. An int to use one margin for all sides.
                A tuple (left,right,top,bottom) for side specific margins.
            create: A ready made component can be added to.
        """
        try:
            parent = self._parent  # type: ignore
            if parent is None:
                raise AttributeError("parent cannot be none.")
        except AttributeError:
            parent = self.ui_item  # type: ignore

        return _add(
            item,
            parent,
            self._sizer,  # type: ignore
            weight,
            margin,
            SizerMixin.default_sizer_margin,
            create,
            align_horizontal=align_horizontal,
        )


class PanelMixin:
    """Mixin providing extra functionality."""

    def __init__(self):
        self.ui_item.Bind(wx.EVT_WINDOW_DESTROY, self._on_close)

    def _on_close(self, evt):
        _LOGGER.debug("Window destroyed.")
        self.controller.deactivate()
        evt.Skip()

    @property
    def controller(self) -> "T.BaseController":
        """Return the controller for this panel."""
        raise NotImplementedError()

    def bind(self, prop: str):
        """Bind a property to a bindable control.

        Args:
            prop: the attribute/property to bind.
        """
        return Binding(self.controller, prop)

    def populate(self):
        """Add and configure widgets here."""
