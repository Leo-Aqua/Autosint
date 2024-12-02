from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton
from PySide6.QtGui import QIcon
from plugins.utils.plugin_interface import PluginInterface


class ExamplePlugin(PluginInterface):
    name = "Example Plugin"
    description = "A simple example plugin."
    version = "1.0"

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
        ip_address = self.ip_input.text()
        result = f"Processed IP: {ip_address}"
        self.outputs["Result"] = result
        self.output_emitted.emit("Result", result)  # Emit the result dynamically

    def ui(self) -> QWidget:
        """
        Build and return the plugin UI.
        """
        if not hasattr(self, "_ui_widget"):
            self._ui_widget = QWidget()
            layout = QVBoxLayout(self._ui_widget)
            layout.addWidget(self.ip_input)
        return self._ui_widget
