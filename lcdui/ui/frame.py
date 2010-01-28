from lcdui import common
from lcdui.ui import widget

import array
import time

class Frame(object):
  def __init__(self, ui):
    self._ui = ui
    self._widgets = {}
    self._position = {}
    self._span = {}
    self._screen_buffer = ScreenBuffer(self.rows(), self.cols())
    self.onInitialize()

  def BuildWidget(self, widget_cls, name=None, row=0, col=0, span=None, **kwargs):
    widget_obj = widget_cls(self, **kwargs)
    if name is None:
      name = widget_obj
    self.AddWidget(widget_obj, name, row, col, span)
    return widget_obj

  def rows(self):
    """Returns the number of rows in the frame."""
    return self._ui.rows()

  def cols(self):
    """Returns the number of columns in the frame."""
    return self._ui.cols()

  def onInitialize(self):
    pass

  def AddWidget(self, widget_obj, name, row=0, col=0, span=None):
    """Adds a widget to the current frame.

    Args:
      widget_obj: the widget to be added
      name: the name of the widget
      row: the row position of the widget
      col: the column position of the widget
      span: the character mask for the widget (or None if no mask)
    """
    self._widgets[name] = widget_obj
    self._position[name] = (row, col)
    self._span[name] = span or max(0, self.cols() - col)

  def GetWidget(self, name):
    return self._widgets.get(name)

  def RemoveWidget(self, name):
    """Removes the widget with the given name."""
    del self._widgets[name]
    del self._position[name]
    del self._span[name]

  def Paint(self):
    """Causes a repaint to happen, updating any internal buffers."""
    for name, w in self._widgets.iteritems():
      outstr = w.Paint()
      row, col = self._position[name]
      span = self._span[name]
      self._screen_buffer.Write(array.array('c', outstr), row, col, span)
    return self._screen_buffer


class MultiFrame(Frame):
  def __init__(self, ui):
    Frame.__init__(self, ui)
    self._inner_frames = []
    self._display_time = {}
    self._last_rotate = None
    self._current_frame = None
    self._index = 0

  def AddWidget(self, widget_obj, name, row=0, col=0, span=None):
    raise NotImplementedError

  def GetWidget(self, name):
    raise NotImplementedError

  def RemoveWidget(self, name):
    raise NotImplementedError

  def AddFrame(self, frame, display_time):
    self._inner_frames.append(frame)
    self._display_time[frame] = display_time

  def RemoveFrame(self, frame):
    self._inner_frames.remove(frame)
    del self._display_time[frame]

  def Paint(self):
    if not self._inner_frames:
      return ''

    if self._current_frame is None:
      self._index = 0
      self._current_frame = self._inner_frames[self._index]

    now = time.time()
    if self._last_rotate:
      active_time = now - self._last_rotate
    else:
      self._last_rotate = now
      active_time = 0

    if len(self._inner_frames) > 1:
      max = self._display_time[self._current_frame]
      if active_time > max:
        self._index = (self._index + 1) % len(self._inner_frames)
        self._last_rotate = now
    self._current_frame = self._inner_frames[self._index]
    return self._current_frame.Paint()


class MenuFrame(Frame):
  def onInitialize(self):
    self._show_back = False
    self._items = []

    self._cursor_pos = 0
    self._window_pos = 0
    self._window_size = self.rows() - 1

    self._title_widget = self.BuildWidget(widget.LineWidget, row=0, col=0)
    self.setTitle('')

    self._item_widgets = []
    for i in xrange(self._window_size):
      w = self.BuildWidget(widget.LineWidget, row=i+1, col=0)
      self._item_widgets.append(w)
    self._rebuildMenu()

  def addItem(self, key, value):
    self._items.append((key, value))
    self._rebuildMenu()

  def scrollUp(self):
    if self._cursor_pos == 0:
      return
    self._cursor_pos -= 1
    self._updateWindowPos()
    self._rebuildMenu()

  def scrollDown(self):
    if (self._cursor_pos + 1) == len(self._items):
      return
    self._cursor_pos += 1
    self._updateWindowPos()
    self._rebuildMenu()

  def _rebuildMenu(self):
    items = self._items[self._window_pos:self._window_pos+self._window_size]
    num_blank = self._window_size - len(items)
    symbol_up = self._ui.GetSymbol(common.SYMBOL.MENU_LIST_UP)
    symbol_down = self._ui.GetSymbol(common.SYMBOL.MENU_LIST_DOWN)
    symbol_cursor = self._ui.GetSymbol(common.SYMBOL.MENU_CURSOR)

    for item_pos in xrange(len(items)):
      item_id, item_value = items[item_pos]
      w = self._item_widgets[item_pos]
      w.set_contents(item_value)

    for blank_pos in xrange(len(items), self._window_size):
      w = self._item_widgets[blank_pos]
      w.set_contents('')

    # draw cursor
    for i in xrange(len(self._item_widgets)):
      w = self._item_widgets[i]
      if i == (self._cursor_pos % self._window_size):
        w.set_prefix(symbol_cursor + '|')
      else:
        w.set_prefix(' |')
      w.set_postfix('| ')

    if self._window_pos > 0:
      self._item_widgets[0].set_postfix('|' + symbol_up)

    if (self._window_pos + self._window_size) < len(self._items):
      self._item_widgets[-1].set_postfix('|' + symbol_down)

  def _updateWindowPos(self):
    self._window_pos = self._cursor_pos - (self._cursor_pos % self._window_size)

  def setTitle(self, title):
    prefix = ''
    symbol_back = self._ui.GetSymbol(common.SYMBOL.FRAME_BACK)
    if self._show_back:
      postfix = '_' + symbol_back + '_'
    else:
      postfix = ''
    avail = self.cols()
    title_str = title
    if len(title_str) < avail:
      title_str += '_' * (avail - len(title_str))
    self._title_widget.set_contents(title_str)
    self._title_widget.set_prefix(prefix)
    self._title_widget.set_postfix(postfix)

  def onLoad(self, lcd):
    pass

class ScreenBuffer:
   def __init__(self, rows, cols):
      self._rows = rows
      self._cols = cols
      self._array = array.array('c', [' '] * (rows * cols))

   def __eq__(self, other):
      if isinstance(other, ScreenMatrix):
         return self._array == other._array
      return False

   def array(self):
     return self._array

   def _AllocNewArray(self):
     return array.array('c', [' '] * (self._rows * self._cols))

   def _GetOffset(self, row, col):
     return row*self._cols + col

   def Clear(self):
     self._array = self._AllocNewArray()

   def Write(self, data, row, col, span):
      """ replace data at row, col in this matrix """
      assert row in range(self._rows)
      assert col in range(self._cols)

      start = self._GetOffset(row, col)
      datalen = min(len(data), span)
      end = start + datalen
      self._array[start:end] = data[:datalen]

   def __str__(self):
      return self._array.tostring()
