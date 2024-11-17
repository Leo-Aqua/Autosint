from PySide6.QtWidgets import QPushButton
from AoPlugin import AoPlugin


class Plugin(AoPlugin):  # Class name MUST be Plugin
    plugin_name = "Plugin Template"  # Plugin name
    plugin_icon = "fugue/icons/puzzle.png"  # Plugin icon (optional)

    def __init__(self):
        super().__init__()
        QPushButton("Test", self)  # Add UI elements and other funcionality
