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
from pprint import pprint


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
        self.plugins = load_plugins("plugins")
        logging.info(f"Loaded {str(len(self.plugins))} plugins.")
        self.ui.statusbar.showMessage(f"Loaded {str(len(self.plugins))} plugins.")
        self.updatePluginList()
        # Events
        self.ui.load_plugin_action.triggered.connect(self.reload_plugins)
        self.ui.load_plugins_button.clicked.connect(self.reload_plugins)
        self.ui.plugin_list.itemClicked.connect(self.select_plugin)
        self.ui.exit_action.triggered.connect(sys.exit)
        self.show()

    def reload_plugins(self):
        plugins = load_plugins("plugins")
        self.updatePluginList()
        self.plugins = plugins

    def get_plugins(self):
        return self.plugins

    def updatePluginList(self):
        self.ui.plugin_list.clear()
        for plugin in self.plugins:
            logging.debug(f" Current Plugin: {plugin}")
            item = QtWidgets.QListWidgetItem()
            item.setText(
                f"{self.plugins[plugin]["instance"].name} - {self.plugins[plugin]["instance"].version}"
            )
            item.setToolTip(
                f"v{self.plugins[plugin]["instance"].version}\nDescription: {self.plugins[plugin]["instance"].description}\n{plugin}"
            )
            item.setCheckState(QtCore.Qt.CheckState.Checked)
            item.setStatusTip(
                f"{plugin} - {self.plugins[plugin]["instance"].name}\n{plugin}"
            )
            if self.plugins[plugin]["instance"].icon != None:
                item.setIcon(self.plugins[plugin]["instance"].icon)
            self.ui.plugin_list.addItem(item)

    def select_plugin(self):
        def generate_output_widget(plugin_instance): ...  # TODO implement

        self.ui.workarea.clear()
        current_item = self.ui.plugin_list.currentIndex().row()
        current_item_instance = list(self.plugins.values())[current_item]["instance"]
        self.ui.workarea.addTab(current_item_instance.ui(), "Input")
        logging.debug(current_item_instance.inputs)
        self.ui.workarea.addTab(generate_output_widget(current_item_instance), "Output")


if __name__ == "__main__":
    app = QtWidgets.QApplication()
    app.setStyle(QtWidgets.QStyleFactory.create("windows11"))
    window = Autosint()
    window.show()
    sys.exit(app.exec())
