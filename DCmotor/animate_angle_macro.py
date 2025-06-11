import FreeCAD
import FreeCADGui
from PySide import QtCore

doc = FreeCAD.ActiveDocument
sheet = doc.getObject("Spreadsheet")

class Animator(QtCore.QObject):
    def __init__(self):
        super().__init__()
        self.angle = 0
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_angle)
        self.running = False

    def start(self):
        if not self.running:
            self.timer.start(33)
            self.running = True

    def stop(self):
        if self.running:
            self.timer.stop()
            self.running = False
            self.angle = 0
            sheet.set('Angle', str(self.angle))
            doc.recompute()

    def update_angle(self):
        self.angle = (self.angle + 3) % 360
        sheet.set('Angle', str(self.angle))
        doc.recompute()

class KeyFilter(QtCore.QObject):
    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.KeyPress:
            if event.key() == QtCore.Qt.Key_L:
                anim.stop()
                return True
        return False

anim = Animator()
anim.start()

mw = FreeCADGui.getMainWindow()
key_filter = KeyFilter()
mw.installEventFilter(key_filter)