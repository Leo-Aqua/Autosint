from ui.ui import Ui_MainWindow
import PySide6.QtWidgets as QtWidgets
import PySide6.QtCore as QtCore
import PySide6.QtGui as QtGui
import sys
import os
import inspect
import importlib
import autosint
import logging
import coloredlogs
import re
from plugin_loader import load_plugins


class Autosint(QtWidgets.QMainWindow):
    def __init__(self):
        super(Autosint, self).__init__()
        # logging.basicConfig(
        #     level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
        # )
        coloredlogs.install(level="DEBUG")
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        logging.info("Initialized ui")
        self.plugins = load_plugins()
        # Events
        self.ui.load_plugin_action.triggered.connect(self.load_plugins)
        self.ui.load_plugins_button.clicked.connect(self.load_plugins)
        self.ui.plugin_add_button.clicked.connect(self.add_plugin)
        # self.ui.plugin_remove_button.clicked.connect(self.remove_plugin) # TODO Implement
        self.show()

    def get_plugins(self):
        return self.plugins

    def updatePluginList(self):
        self.ui.plugin_list.clear()
        for plugin in self.plugins:

            self.ui.plugin_list.addItem(
                f"{plugin["class"].name} - v{plugin["class"].version}"
            )
            items = [
                self.ui.plugin_list.item(x) for x in range(self.ui.plugin_list.count())
            ]
            self.ui.plugin_list.item(len(items) - 1).setToolTip(
                f"Name: {plugin["class"].name}\nVersion: {plugin["class"].version}\nDescription: {plugin["class"].description}\nSource: {plugin["module"].__name__}"
            )

    def add_plugin(self):
        try:
            selected_row = self.ui.plugin_list.selectedIndexes()[0].row()
            plugin = self.plugins[selected_row]
            self.ui.workarea.addTab(plugin["class"], plugin["class"].name)
        except IndexError:
            pass  # Do nothig in case nothing is selected


class Plugin:

    def __init__(
        self,
        name: str,
        input_fields: list,
        output_fields: list,
        compatible_plugins: list,
        version: str,
        icon: QtGui.QIcon = None,
        description: str = None,
    ):
        super(Plugin, self).__init__()
        self.name = name
        self.input_fields = input_fields
        self.output_fields = output_fields
        self.compatible_plugins = compatible_plugins
        self.icon = icon
        self.description = description
        self.version = version

    class Input(QtWidgets.QWidget):
        pass

    class Output(QtWidgets.QWidget):
        pass


if __name__ == "__main__":
    app = QtWidgets.QApplication()
    print(QtWidgets.QStyleFactory.keys())
    window = Autosint()
    window.show()
    sys.exit(app.exec())
