from lcdui import common
from lcdui.devices import Generic

MTX_ORB_SYMBOLS = {
  common.SYMBOL.ARROW_UP: '^',
  common.SYMBOL.ARROW_DOWN: 'v',
  common.SYMBOL.ARROW_LEFT: '\x7e',
  common.SYMBOL.ARROW_RIGHT: '\x7f',

  common.SYMBOL.MENU_CURSOR: '\x7e',  # arrow right
  common.SYMBOL.MENU_LIST_UP: '^',  # arrow up
  common.SYMBOL.MENU_LIST_DOWN: 'v', # arrow down

  common.SYMBOL.FRAME_BACK: '<', # double left arrow
}

class MatrixOrbitalDisplay(Generic.SerialCharacterDisplay):
  ROWS = 4
  COLS = 20

  def _WriteCommand(self, command):
    self._serial_handle.write('\xfe' + command)

  ### IGenericDisplay interface

  def rows(self):
    return self.ROWS

  def cols(self):
    return self.COLS

  def ClearScreen(self):
    self._WriteCommand('\x58')

  def BacklightEnable(self, enable):
    if enable:
      self._WriteCommand('\x42\x00')
    else:
      self._WriteCommand('\x46')

  def SetCursor(self, row, col):
    row += 1
    col += 1
    command = '\x47%c%c' % (col, row)
    self._WriteCommand(command)

  def WriteData(self, data, row, col):
    #self._logger.debug('Writing data: %s' % data)
    #outstr = data.translate(self._TRANSLATION_TABLE)
    self.SetCursor(row, col)
    self._serial_handle.write(data)

  def WriteScreen(self, buf):
    for i in xrange(self.rows()):
      start = i*self.cols()
      end = start+self.cols()
      self.WriteData(data=buf[start:end].tostring(), row=i, col=0)

  def GetSymbol(self, key, alt=None):
    return MTX_ORB_SYMBOLS.get(key, alt)
