from PySide6.QtWidgets import QApplication
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

class MiVentana:
    def __init__(self):
        loader = QUiLoader()
        file = QFile("interfaz.ui")
        file.open(QFile.ReadOnly)
        self.ui = loader.load(file)
        file.close()

 
        self.ui.pushButton_hola.clicked.connect(self.saludar)

    def saludar(self):
        self.ui.label_terminal.setText("hola mundo")

app = QApplication([])
ventana = MiVentana()
ventana.ui.show()
app.exec()