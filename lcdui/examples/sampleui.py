from lcdui.devices import Generic, CrystalFontz
from lcdui.ui import frame
from lcdui.ui import ui
from lcdui.ui import widget
import time

#device = Generic.MockCharacterDisplay(rows=4, cols=40)
device = CrystalFontz.CFA635Display(port='/dev/ttyUSB0')

device.ClearScreen()
device.BacklightEnable(True)

ui = ui.LcdUi(device)

f = ui.FrameFactory(frame.Frame)

line1 = widget.LineWidget(frame=f, contents="Hello, world!")
f.AddWidget("line1", line1, row=0, col=0)
line2 = widget.LineWidget(frame=f, contents="cutoffXXXX")
f.AddWidget("line2", line2, row=3, col=10, span=6)

ui.PushFrame(f)
ui.Repaint()

f = ui.FrameFactory(frame.MenuFrame)

f.setTitle('example menu')
f.addItem(1, 'first choice')
f.addItem(2, 'second choice')
f.addItem(3, 'another choice')
f.addItem(4, 'last choice')

ui.PushFrame(f)
ui.Repaint()

for i in xrange(6):
  f.scrollDown()
  ui.Repaint()
  time.sleep(2)

for i in xrange(6):
  f.scrollUp()
  ui.Repaint()
  time.sleep(2)
