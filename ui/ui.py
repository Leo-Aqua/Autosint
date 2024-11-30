from PySide6 import QtCore, QtGui, QtWidgets
import sys
import os
from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt,
)
from PySide6.QtGui import (
    QAction,
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QMenu,
    QMenuBar,
    QSizePolicy,
    QStatusBar,
    QWidget,
)


def icon(name, shadowless=False):
    ico = QIcon()
    ico.addFile(
        (
            os.path.dirname(__file__)[:-3] + "/icons/icons/" + name + ".png"
            if not shadowless
            else os.path.dirname(__file__)[:-3]
            + "/icons/icons-shadowless/"
            + name
            + ".png"
        ),
    )
    return ico


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        # Resize window
        MainWindow.resize(1200, 700)

        # Set window title
        MainWindow.setWindowTitle("Autosint")

        # Set window icon
        icon_ = QIcon()
        icon_.addFile("icons/icons/autosint.png")
        icon_ = icon("autosint")

        MainWindow.setWindowIcon(icon_)

        # Add menu bar
        menubar = QMenuBar()
        file_menu = menubar.addMenu("File")
        help_menu = menubar.addMenu("Help")
        MainWindow.setMenuBar(menubar)

        # add status bar
        self.statusbar = QStatusBar()
        self.statusbar.showMessage("Ready")
        MainWindow.setStatusBar(self.statusbar)

        self.load_plugin_action = file_menu.addAction("Load plugin")
        self.load_plugin_action.setIcon(icon("plug--plus"))
        self.load_plugin_action.setShortcut("Ctrl+L")
        self.exit_action = file_menu.addAction("Exit", sys.exit)
        self.exit_action.setIcon(icon("door-open-out"))
        self.exit_action.setShortcut("Ctrl+Q")

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
        self.plugin_remove_button = QtWidgets.QPushButton()
        self.plugin_remove_button.setIcon(icon("plug--arrow--left"))
        plugin_title_layout.addWidget(self.plugin_remove_button)
        self.plugin_add_button = QtWidgets.QPushButton()
        self.plugin_add_button.setIcon(icon("plug--arrow--right"))
        plugin_title_layout.addWidget(self.plugin_add_button)
        plugin_title_layout.addStretch()
        plugin_layout.addLayout(plugin_title_layout)

        plugin_list_layout = QtWidgets.QVBoxLayout()

        self.plugin_list = QtWidgets.QListWidget()
        plugin_list_layout.addWidget(self.plugin_list)

        self.load_plugins_button = QtWidgets.QPushButton("(Re)Load plugins")
        self.load_plugins_button.setFixedHeight(40)
        self.load_plugins_button.setIcon(icon("plug--plus"))
        plugin_list_layout.addWidget(self.load_plugins_button)
        plugin_layout.addLayout(plugin_list_layout)

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
        self.workarea.setMovable(True)
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

        MainWindow.setCentralWidget(self.splitter_center)

        QMetaObject.connectSlotsByName(MainWindow)
