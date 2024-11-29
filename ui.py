from PySide6 import QtCore, QtGui, QtWidgets
import sys
import os


def icon(name, shadowless=False):
    return QtGui.QIcon(
        os.path.dirname(__file__) + "/icons/icons/" + name + ".png"
        if not shadowless
        else os.path.dirname(__file__) + "/icons/icons-shadowless/" + name + ".png"
    )


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        # Resize window
        self.resize(1200, 700)

        # Set window title
        self.setWindowTitle("Autosint")

        # Set window icon
        self.setWindowIcon(icon("autosint"))

        # Add menu bar
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        help_menu = menubar.addMenu("Help")

        load_module_action = file_menu.addAction(
            "Load module"
        )  # TODO implement self.load_module
        load_module_action.setIcon(icon("plug--plus"))
        load_module_action.setShortcut("Ctrl+L")
        exit_action = file_menu.addAction("Exit", sys.exit)
        exit_action.setIcon(icon("door-open-out"))
        exit_action.setShortcut("Ctrl+Q")

        # Setup splitters
        self.splitter_top = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        self.splitter_center = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        self.splitter_bottom = QtWidgets.QSplitter(QtCore.Qt.Horizontal)

        ## Create widgets
        # splitter_top:

        # splitter_top left:
        # Create a container widget with a vertical layout
        plugin_container = QtWidgets.QWidget()
        plugin_layout = QtWidgets.QVBoxLayout(plugin_container)

        # Create the label and add it to the layout
        plugin_title_layout = QtWidgets.QHBoxLayout()
        plugin_icon = QtWidgets.QLabel()
        plugin_icon.setPixmap(icon("plug").pixmap(16, 16))
        plugin_title_layout.addWidget(plugin_icon)
        plugin_label = QtWidgets.QLabel("Plugins")
        plugin_title_layout.addWidget(plugin_label)
        plugin_title_layout.addStretch()
        plugin_layout.addLayout(plugin_title_layout)
        plugin_list_layout = QtWidgets.QVBoxLayout()
        self.plugin_list = QtWidgets.QListWidget()
        plugin_list_layout.addWidget(self.plugin_list)
        self.load_modules_button = QtWidgets.QPushButton("Load modules")
        self.load_modules_button.setFixedHeight(40)
        self.load_modules_button.setIcon(icon("plug--plus"))
        plugin_list_layout.addWidget(self.load_modules_button)
        plugin_layout.addLayout(plugin_list_layout)

        # Add the plugin list to the same layout
        plugin_layout.addWidget(plugin_container)

        # Add the container widget to the splitter
        self.splitter_top.addWidget(plugin_container)

        # splitter_top right:
        workarea_container = QtWidgets.QWidget()
        workarea_layout = QtWidgets.QVBoxLayout(workarea_container)

        workarea_title_layout = QtWidgets.QHBoxLayout()
        workarea_icon = QtWidgets.QLabel()
        workarea_icon.setPixmap(icon("block").pixmap(16, 16))
        workarea_title_layout.addWidget(workarea_icon)
        workarea_label = QtWidgets.QLabel("Workarea")
        workarea_title_layout.addWidget(workarea_label)
        workarea_title_layout.addStretch()

        workarea_layout.addLayout(workarea_title_layout)
        self.workarea = QtWidgets.QTabWidget()
        workarea_layout.addWidget(self.workarea)

        self.splitter_top.addWidget(workarea_container)

        # splitter_center top:

        self.splitter_top.setStretchFactor(0, 1)  # plugin list
        self.splitter_top.setStretchFactor(1, 5)  # workarea
        self.splitter_center.addWidget(self.splitter_top)

        # splitter_center bottom:
        output_container = QtWidgets.QWidget()
        output_layout = QtWidgets.QVBoxLayout(output_container)
        output_title_layout = QtWidgets.QHBoxLayout()

        output_icon = QtWidgets.QLabel()
        output_icon.setPixmap(icon(name="inbox").pixmap(16, 16))
        output_title_layout.addWidget(output_icon)
        output_label = QtWidgets.QLabel("Output")
        output_title_layout.addWidget(output_label)
        output_title_layout.addStretch()

        output_layout.addLayout(output_title_layout)
        self.output = QtWidgets.QTreeWidget()
        output_layout.addWidget(self.output)

        self.splitter_center.addWidget(output_container)
        # Main window:

        self.setCentralWidget(self.splitter_center)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
