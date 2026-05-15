from PySide6.QtWidgets import QApplication
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QThread, Signal
import pyqtgraph as pg
import serial
import serial.tools.list_ports

# Subclase de QUiLoader que registra PlotWidget
class CustomLoader(QUiLoader):
    def createWidget(self, className, parent=None, name=""):
        if className == "PlotWidget":
            widget = pg.PlotWidget(parent=parent)
            widget.setObjectName(name)
            return widget
        return super().createWidget(className, parent, name)


class SerialThread(QThread):
    data_received = Signal(float)

    def __init__(self, port, baudrate=9600):
        super().__init__()
        self.port = port
        self.baudrate = baudrate
        self.running = True

    def run(self):
        try:
            self.ser = serial.Serial(self.port, self.baudrate)
            while self.running:
                line = self.ser.readline().decode().strip()
                try:
                    self.data_received.emit(float(line))
                except ValueError:
                    pass
        except Exception as e:
            print(f"Error serial: {e}")

    def stop(self):
        self.running = False
        if hasattr(self, 'ser') and self.ser.is_open:
            self.ser.close()
        self.quit()


class MiVentana:
    def __init__(self):
        loader = CustomLoader()  # <-- usar el loader personalizado
        file = QFile("interfaz_arduino.ui")
        file.open(QFile.ReadOnly)
        self.ui = loader.load(file)
        file.close()

        self.curve = self.ui.widget_plot.plot(pen='y')
        self.data = []

        ports = [p.device for p in serial.tools.list_ports.comports()]
        self.ui.comboBox_ports.addItems(ports)

        self.ui.pushButton_conectar.clicked.connect(self.toggle_conexion)
        self.serial_thread = None

    def toggle_conexion(self):
        if self.serial_thread is None:
            port = self.ui.comboBox_ports.currentText()
            self.serial_thread = SerialThread(port)
            self.serial_thread.data_received.connect(self.actualizar_plot)
            self.serial_thread.start()
            self.ui.pushButton_conectar.setText("Desconectar")
        else:
            self.serial_thread.stop()
            self.serial_thread = None
            self.ui.pushButton_conectar.setText("Conectar")

    def actualizar_plot(self, value):
        self.data.append(value)
        if len(self.data) > 200:
            self.data.pop(0)
        self.curve.setData(self.data)


app = QApplication([])
ventana = MiVentana()
ventana.ui.show()
app.exec()