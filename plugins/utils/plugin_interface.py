from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QIcon
from abc import ABC, abstractmethod


class PluginInterface(ABC):
    """
    Base interface for plugins.
    """

    name: str
    description: str = ""
    version: str
    inputs: dict[str, QWidget]
    outputs: dict[str, str]
    icon: QIcon = None

    @abstractmethod
    def execute(self):
        """
        Execute the plugin functionality.
        """
        pass

    @abstractmethod
    def ui(self) -> QWidget:
        """
        Return the main UI of the plugin.
        """
        pass
