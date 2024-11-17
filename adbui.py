from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon, QPixmap, QFont, QColor
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTabWidget,
    QGridLayout,
    QWidget,
    QPushButton,
    QLabel,
    QListWidget,
    QVBoxLayout,
    QRadioButton,
    QScrollArea,
)
import sys
import os


class OptionsTab(QMainWindow):  # TODO: Load settings from file (if possible)
    save_signal = Signal(dict)  # Define a custom signal

    def __init__(self):
        super().__init__()
        scroll_box = QScrollArea(self)
        self.setCentralWidget(scroll_box)
        layout = QVBoxLayout(scroll_box)
        layout.setAlignment(Qt.AlignTop)
        layout.addWidget(QLabel("Tab orientation"))

        self.tab_orientation_v = QRadioButton("Vertical")
        self.tab_orientation_h = QRadioButton("Horizontal")
        self.tab_orientation_h.setChecked(True)
        layout.addWidget(self.tab_orientation_v)
        layout.addWidget(self.tab_orientation_h)

        save_button = QPushButton("Save")
        save_button.setFixedSize(200, 40)
        save_button.setDefault(True)
        layout.addWidget(save_button)

        save_button.clicked.connect(self.emit_settings)

    def emit_settings(self):
        settings = {"vertical": self.tab_orientation_v.isChecked()}

        self.save_signal.emit(settings)


class MainWindow(QMainWindow):
    """
    The main window of the application. This class sets up the main window and
    creates the layout. The main window is a QMainWindow, which is a top-level
    widget that provides a menu bar and a status bar. The window is divided
    into two parts: a tab widget and a button. The tab widget can be moved
    around, and the button is used to load plugins.
    """

    def __init__(self):
        """
        Initialize the main window. This method sets the window title, the
        window size, and sets up the layout of the window.
        """
        super().__init__()

        self.setWindowTitle("autOsint")
        self.resize(800, 500)

        self.plugins = []

        main_grid_layout = QGridLayout()
        main_grid_layout.setContentsMargins(5, 5, 5, 5)
        # Make sidebar smaller
        main_grid_layout.setColumnStretch(1, 1)

        sidebar_layout = QVBoxLayout()
        sidebar_layout.setContentsMargins(5, 5, 5, 5)

        # The load button is used to load plugins
        load_button = QPushButton("Load Plugins")
        load_button.setFixedSize(200, 40)
        sidebar_layout.addWidget(load_button)

        sidebar_layout.addWidget(QLabel("Loaded Plugins"))

        self.loaded_plugins_listbox = QListWidget()
        sidebar_layout.addWidget(self.loaded_plugins_listbox)

        # The tab widget is used to display the plugins
        self.tab_widget = QTabWidget()
        self.tab_widget.setMovable(True)
        self.tab_widget.setTabPosition(QTabWidget.North)

        self.initialize_tab_widget()

        self.load_plugins()

        # The tab widget is added to the layout
        main_grid_layout.addWidget(self.tab_widget, 0, 1)

        # The central widget is the main widget of the window
        widget = QWidget()
        widget.setLayout(main_grid_layout)

        main_grid_layout.addLayout(sidebar_layout, 0, 0)

        self.setCentralWidget(widget)

        ## Events
        load_button.clicked.connect(self.load_plugins)
        app_tab = OptionsTab()
        app_tab.save_signal.connect(self.apply_options)

    def load_plugins(self):
        old_plugins = set(self.plugins)
        current_plugins = set()

        # Reinitialize tab widget
        self.initialize_tab_widget()

        # Import all plugins in the plugins directory
        plugin_directory = os.path.dirname(__file__) + "/plugins"
        for plugin in os.listdir(plugin_directory):
            if plugin.endswith(".py"):
                current_plugins.add(plugin[:-3])

        # Unload removed plugins
        removed_plugins = old_plugins - current_plugins
        for removed_plugin in removed_plugins:
            plugin_name = f"plugins.{removed_plugin}"
            if plugin_name in sys.modules:
                del sys.modules[plugin_name]

        # Update plugin list
        self.plugins = list(current_plugins)

        # Add or update plugins in the tab widget
        for plugin_name in self.plugins:
            full_plugin_name = f"plugins.{plugin_name}"

            plugin_module = __import__(full_plugin_name, fromlist=["Plugin"])
            if hasattr(plugin_module, "Plugin"):
                ao_plugin_instance = plugin_module.Plugin()
                plugin_tab = self.tab_widget.addTab(
                    ao_plugin_instance, ao_plugin_instance.plugin_name
                )
                if ao_plugin_instance.plugin_icon:
                    self.tab_widget.setTabIcon(
                        plugin_tab, QIcon(ao_plugin_instance.plugin_icon)
                    )

        # Update the loaded plugins listbox
        self.loaded_plugins_listbox.clear()

        self.loaded_plugins_listbox.addItems(self.plugins)

    def initialize_tab_widget(self):
        self.tab_widget.clear()
        # Create and store the instance
        self.options_tab_instance = OptionsTab()
        self.option_tab = self.tab_widget.addTab(self.options_tab_instance, "Options")
        # Connect the signal
        self.options_tab_instance.save_signal.connect(self.apply_options)
        self.tab_widget.tabBar().setTabTextColor(self.option_tab, QColor("lightblue"))
        self.tab_widget.setTabIcon(self.option_tab, QIcon("fugue/icons/gear.png"))

    def apply_options(self, e):  # TODO: Save settings in a file
        if e["vertical"]:
            self.tab_widget.setTabPosition(QTabWidget.East)
        else:
            self.tab_widget.setTabPosition(QTabWidget.North)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
