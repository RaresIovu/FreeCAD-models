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

        theta = (t*180 / self.period) % 360
        amp = 20
        PhaseA = 0
        PhaseB = 90
        PhaseC = 180
        PhaseD = 270

        thetaA = (theta+PhaseA) % 360
        thetaB = (theta+PhaseB) % 360
        thetaC = (theta+PhaseC) % 360
        thetaD = (theta+PhaseD) % 360
        #A
        if 0 <= thetaA < 90:
            liftA = amp * math.sin(math.radians(thetaA * 2))
        else:
            liftA = 0

        if 270 <= thetaA < 360:
            liftB = amp * math.sin(math.radians((thetaA - 270) * 2))
        else:
            liftB = 0
        #B
        if 0 <= thetaB < 90:
            liftC = amp * math.sin(math.radians(thetaB * 2))
        else:
            liftC = 0

        if 270 <= thetaB < 360:
            liftD = amp * math.sin(math.radians((thetaB - 270) * 2))
        else:
            liftD = 0
        #B
        if 0 <= thetaC < 90:
            liftE = amp * math.sin(math.radians(thetaC * 2))
        else:
            liftE = 0

        if 270 <= thetaC < 360:
            liftF = amp * math.sin(math.radians((thetaC - 270) * 2))
        else:
            liftF = 0
        #D
        if 0 <= thetaD < 90:
            liftG = amp * math.sin(math.radians(thetaD * 2))
        else:
            liftG = 0

        if 270 <= thetaD < 360:
            liftH = amp * math.sin(math.radians((thetaD - 270) * 2))
        else:
            liftH = 0

        self.sheet.setExpression('Crank_Pos', f"{pos} mm")
        self.sheet.setExpression('Bar_PosX', f"{pos2} mm")
        self.sheet.setExpression('Angle', f"{angle} deg")
        self.sheet.setExpression('Bar_Angle', f"{anglebar} deg")
        self.sheet.setExpression('Crank_Pos_rev', f"{posrev} mm")
        self.sheet.setExpression('Bar_PosX_rev', f"{pos2rev} mm")
        self.sheet.setExpression('Angle_rev', f"{anglerev} deg")
        self.sheet.setExpression('Bar_Angle_rev', f"{anglebarrev} deg")

        self.sheet.setExpression('Supapa_A', f"{liftG} mm")
        self.sheet.setExpression('Supapa_B', f"{liftH} mm")
        self.sheet.setExpression('Supapa_A2', f"{liftA} mm")
        self.sheet.setExpression('Supapa_B2', f"{liftB} mm")
        self.sheet.setExpression('Supapa_A3', f"{liftE} mm")
        self.sheet.setExpression('Supapa_B3', f"{liftF} mm")
        self.sheet.setExpression('Supapa_A4', f"{liftC} mm")
        self.sheet.setExpression('Supapa_B4', f"{liftD} mm")
        App.ActiveDocument.recompute()

# --- Usage ---
sheet = App.ActiveDocument.Spreadsheet  # your spreadsheet object
oscillator = CrankOscillator(sheet, amplitude=45, offset=30, period=2)

# To start:
oscillator.start()

# To stop:
# oscillator.stop()