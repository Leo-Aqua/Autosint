from PySide6 import QtWidgets, QtCore


class IO(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.io_tab = QtWidgets.QTabWidget(self)
        self.input_tab = self.io_tab.addTab(QtWidgets.QWidget, label="Input")
        self.output_tab = self.io_tab.addTab(QtWidgets.QWidget, label="Output")
