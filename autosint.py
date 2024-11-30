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


class Autosint(QtWidgets.QMainWindow):
    def __init__(self):
        super(Autosint, self).__init__()
        logging.basicConfig(
            level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
        )
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Events
        self.ui.load_plugin_action.triggered.connect(self.load_plugins)
        self.ui.load_plugins_button.clicked.connect(self.load_plugins)
        self.show()

    def load_plugins(self):
        def check_valid_plugin(plugin):
            # Check if setupUi method exists

            if "setupUi" in plugin.__dict__:
                logging.debug(f"setupUi() exists in {str(plugin)}")
            else:
                logging.warning(f"{str(plugin)} does not have a setupUi function!")

        self.plugins = {}
        # Get all Python files in the plugins directory
        plugin_files = [f for f in os.listdir("plugins") if f.endswith(".py")]

        for plugin_file in plugin_files:
            # Remove the file extension and import the module dynamically
            plugin_name = plugin_file[:-3]  # Remove '.py'
            try:
                # Import the plugin module dynamically using importlib
                module = importlib.import_module(f"{"plugins"}.{plugin_name}")
            except ModuleNotFoundError as e:
                logging.error(f"Error importing {plugin_name}: {e}")
                continue

            # Find all classes in the module that inherit from Plugin
            for name, obj in inspect.getmembers(module, inspect.isclass):
                for cls in obj.__subclasses__():
                    if issubclass(cls, autosint.Plugin):
                        check_valid_plugin(cls)
                        self.plugins[cls.__name__] = cls

            logging.debug("Loaded plugins: " + str(self.plugins))

    def get_plugins(self):
        return self.plugins


class Plugin(QtWidgets.QWidget):
    plugin_name: str = None
    plugin_icon: QtGui.QIcon = None

    input_fields: list = None
    output_fields: list = None

    compatible_plugins: list = None

    def __init__(self):
        super(Plugin, self).__init__()

    def setupUi(self):
        pass


if __name__ == "__main__":
    app = QtWidgets.QApplication()
    app.setStyle("Fusion")
    window = Autosint()
    window.show()
    sys.exit(app.exec())
