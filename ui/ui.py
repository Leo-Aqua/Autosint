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
        file_menu.setStyle(QtWidgets.QStyleFactory.create("Fusion"))
        help_menu = menubar.addMenu("Help")
        MainWindow.setMenuBar(menubar)

        # add status bar
        self.statusbar = QStatusBar()
        self.statusbar.showMessage("Ready")
        MainWindow.setStatusBar(self.statusbar)

        self.load_plugin_action = file_menu.addAction("Re&load plugin")
        self.load_plugin_action.setIcon(icon("plug--plus"))
        self.load_plugin_action.setShortcut("Ctrl+L")
        self.load_plugin_action.setStatusTip("Reload Plugins")
        self.run_action = file_menu.addAction("&Run")
        self.run_action.setIcon(icon("wand-magic"))
        self.run_action.setShortcut("Ctrl+R")
        self.run_action.setStatusTip("Run all active plugins from top to bottom")
        file_menu.addSeparator()
        self.about_action = file_menu.addAction("&About")  # TODO Implement about dialog
        self.about_action.setIcon(icon("information"))
        self.exit_action = file_menu.addAction("&Quit")
        self.exit_action.setIcon(icon("door-open-out"))
        self.exit_action.setShortcut("Ctrl+Q")
        self.exit_action.setStatusTip("Quit the application")

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

        self.load_plugins_button = QtWidgets.QPushButton("Reload plugins")
        self.load_plugins_button.setFixedHeight(30)
        self.load_plugins_button.setIcon(icon("plug--plus"))
        self.load_plugins_button.setStatusTip("Reload Plugins")
        plugin_list_layout.addWidget(self.load_plugins_button)
        self.run_button = QtWidgets.QPushButton("Run")
        self.run_button.setFixedHeight(40)
        self.run_button.setIcon(icon("wand-magic"))
        self.run_button.setDefault(True)
        self.run_button.setStatusTip("Run all active plugins from top to bottom")
        plugin_list_layout.addWidget(self.run_button)
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
        self.workarea.setGraphicsEffect(QtWidgets.QGraphicsColorizeEffect())
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
