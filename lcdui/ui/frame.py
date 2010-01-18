from lcdui import common
from lcdui.ui import widget

import array

class Frame(object):
  def __init__(self, ui):
    self._ui = ui
    self._widget = {}
    self._position = {}
    self._span = {}
    self._screen_buffer = ScreenBuffer(self.rows(), self.cols())
    self.onInitialize()

  def rows(self):
    return self._ui.rows()

  def cols(self):
    return self._ui.cols()

  def onInitialize(self):
    pass

  def AddWidget(self, name, widget_obj, row=0, col=0, span=None):
    self._widget[name] = widget_obj
    self._position[name] = (row, col)
    self._span[name] = span or max(0, self.cols() - col)

  def GetWidget(self, name):
    return self._widget.get(name)

  def RemoveWidget(self, name):
    del self._widget[name]
    del self._position[name]
    del self._span[name]

  def Paint(self):
    for widgetname, w in self._widget.iteritems():
      outstr = w.Paint()
      row, col = self._position[widgetname]
      span = self._span[widgetname]
      self._screen_buffer.Write(array.array('c', outstr), row, col, span)
    return self._screen_buffer

  def SwitchInEvent(self):
    pass

  def SwitchOutEvent(self):
    pass


class MenuFrame(Frame):
  def onInitialize(self):
    self._show_back = False
    self._items = []

    self._cursor_pos = 0
    self._window_pos = 0
    self._window_size = self.rows() - 1

    self._title_widget = widget.LineWidget(frame=self)
    self.AddWidget('title', self._title_widget, row=0, col=0)
    self.setTitle('')

    self._item_widgets = []
    for i in xrange(self._window_size):
      w = widget.LineWidget(frame=self, prefix=' |', postfix='| ')
      self._item_widgets.append(w)
      self.AddWidget('item%i' % i, w, row=i+1, col=0)
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

    if self._window_pos > 0:
      self._item_widgets[0].set_postfix('|' + symbol_up)
    else:
      self._item_widgets[0].set_postfix('| ')

    if (self._window_pos + self._window_size) < len(self._items):
      self._item_widgets[-1].set_postfix('|' + symbol_down)
    else:
      self._item_widgets[-1].set_postfix('| ')


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
