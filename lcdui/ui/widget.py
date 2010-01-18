class Widget:
  def __init__(self, frame):
    self._frame = frame

  def Paint(self):
    return ''


class LineWidget(Widget):
  def __init__(self, frame, contents='', prefix='', postfix=''):
    Widget.__init__(self, frame)
    self._contents = contents
    self._prefix = prefix
    self._postfix = postfix

  def Paint(self):
    cols = self._frame.cols()
    outer_len = len(self._prefix) + len(self._postfix)
    inner_len = cols - outer_len
    contents = self._contents[:inner_len]
    contents += ' '*(inner_len - len(contents))
    result = self._prefix + contents + self._postfix
    return result[:cols]

  def set_contents(self, s):
    self._contents = s
  def contents(self): return self._contents

  def set_prefix(self, s):
    self._prefix = s
  def prefix(self): return self._prefix

  def set_postfix(self, s):
    self._postfix = s
  def postfix(self): return self._postfix
