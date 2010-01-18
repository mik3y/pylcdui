import serial

from lcdui import common
from lcdui.devices import Interfaces

class InvalidPositionError(Exception):
  """Raised when a command was attempted on an out-of-range location"""


class SerialCharacterDisplay(Interfaces.ICharacterDisplay):
  """A character display that is driven by a serial port."""
  def __init__(self, port, baudrate=115200):
    self._serial_handle = serial.Serial(port=port, baudrate=baudrate)


class MockCharacterDisplay(Interfaces.ICharacterDisplay):
  SYMBOLS = {
    common.SYMBOL.ARROW_UP: '^',
    common.SYMBOL.ARROW_DOWN: 'v',
    common.SYMBOL.ARROW_LEFT: '<',
    common.SYMBOL.ARROW_RIGHT: '>',

    common.SYMBOL.TRIANGLE_UP: '^',
    common.SYMBOL.TRIANGLE_DOWN: 'v',
    common.SYMBOL.TRIANGLE_LEFT: '<',
    common.SYMBOL.TRIANGLE_RIGHT: '>',

    common.SYMBOL.PROGBAR_1: '#',
    common.SYMBOL.PROGBAR_2: '#',
    common.SYMBOL.PROGBAR_3: '#',
    common.SYMBOL.PROGBAR_4: '#',
    common.SYMBOL.PROGBAR_5: '#',

    common.SYMBOL.MENU_CURSOR: '*',
    common.SYMBOL.MENU_LIST_UP: '^',
    common.SYMBOL.MENU_LIST_DOWN: 'v',

    common.SYMBOL.FRAME_BACK: '<',
  }

  def __init__(self, rows, cols):
    self._rows = rows
    self._cols = cols
    self._contents = self._AllocContents()

  def _AllocContents(self):
    return " " * (self._rows * self._cols)

  def ClearScreen(self):
    self._contents = self._AllocContents()

  def BacklightEnable(self, enable):
    pass

  def GetSymbol(self, name, default=None):
    return self.SYMBOLS.get(name, default)

  def rows(self):
    return self._rows

  def cols(self):
    return self._cols

  def WriteScreen(self, buf):
    self._contents = buf
    ret = ""
    for i in xrange(self._rows):
      ret += "|" + self._contents[i*self._cols:(i+1)*self._cols].tostring() + "|\n"
    print ret
