from PySide2 import QtCore
import FreeCAD as App
import math
import time

class CrankOscillator(QtCore.QObject):
    def __init__(self, sheet, amplitude=0, offset=30, period=2, interval=50):
        super().__init__()
        self.sheet = sheet
        self.amplitude = amplitude
        self.offset = offset
        self.period = period
        self.interval = interval
        self.start_time = None

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_crank)

    def start(self):
        """Start the oscillation"""
        self.start_time = time.time()
        self.timer.start(self.interval)
        print("Oscillation started")

    def stop(self):
        """Stop the oscillation"""
        self.timer.stop()
        print("Oscillation stopped")

    def update_crank(self):
        t = time.time() - self.start_time
        if(t>10): self.stop()
        pos = self.amplitude * math.sin(2 * math.pi * t / self.period)
        pos2 = self.amplitude * math.cos(2 * math.pi * t / self.period)
        anglebar = 15 * math.cos((2 * math.pi * t / self.period) + math.pi)
        angle = (180 * t) % 360 - 90

        posrev = self.amplitude * math.sin((2 * math.pi * t / self.period) + math.pi)
        pos2rev = self.amplitude * math.cos((2 * math.pi * t / self.period) + math.pi)
        anglebarrev = 15 * math.cos((2 * math.pi * t / self.period))
        anglerev = (180 * t) % 360 + 90

        self.sheet.setExpression('Crank_Pos', f"{pos} mm")
        self.sheet.setExpression('Bar_PosX', f"{pos2} mm")
        self.sheet.setExpression('Angle', f"{angle} deg")
        self.sheet.setExpression('Bar_Angle', f"{anglebar} deg")
        self.sheet.setExpression('Crank_Pos_rev', f"{posrev} mm")
        self.sheet.setExpression('Bar_PosX_rev', f"{pos2rev} mm")
        self.sheet.setExpression('Angle_rev', f"{anglerev} deg")
        self.sheet.setExpression('Bar_Angle_rev', f"{anglebarrev} deg")
        App.ActiveDocument.recompute()

# --- Usage ---
sheet = App.ActiveDocument.Spreadsheet  # your spreadsheet object
oscillator = CrankOscillator(sheet, amplitude=45, offset=30, period=2)

# To start:
oscillator.start()

# To stop:
# oscillator.stop()