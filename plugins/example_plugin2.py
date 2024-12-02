from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton
from PySide6.QtGui import QIcon
from plugins.utils.plugin_interface import PluginInterface


class ExamplePlugin(PluginInterface):
    name = "Second Example Plugin"
    description = "A simple example plugin."
    version = "2.0"
    inputs = {}
    outputs = {}
    icon = QIcon("icons/icons/plug.png")  # Optional icon file

    def __init__(self):
        # Initialize inputs
        self.ip_input = QLineEdit()
        self.inputs = {"IP Address": self.ip_input}

        self.outputs = {"Result": ""}
        self.ui_widget = None

    def execute(self):
        """
        Simple plugin execution logic.
        """
        ip_address = self.inputs["IP Address"].text()
        self.outputs["Result"] = f"Processed IP: {ip_address}"
        print(self.outputs["Result"])

    def ui(self) -> QWidget:
        """
        Build and return the plugin UI.
        """
        if not self.ui_widget:
            self.ui_widget = QWidget()
            layout = QVBoxLayout(self.ui_widget)
            layout.addWidget(self.ip_input)
        return self.ui_widget

    def set_input(self, key, value):
        if key in self.inputs:
            self.inputs[key].setText(value)

    def get_output(self, key):
        return self.outputs.get(key)

    def connect_output(self, key, callback):
        """
        Connect a specific output signal to another function or plugin.
        """
        self.output_emitted.connect(callback)
