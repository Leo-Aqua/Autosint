# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Qt5.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1099, 777)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(1099, 777))
        MainWindow.setMaximumSize(QtCore.QSize(1099, 777))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(20, 10, 241, 261))
        self.groupBox.setObjectName("groupBox")
        self.search_image = QtWidgets.QLabel(self.groupBox)
        self.search_image.setGeometry(QtCore.QRect(10, 30, 220, 220))
        self.search_image.setAcceptDrops(True)
        self.search_image.setText("")
        self.search_image.setPixmap(QtGui.QPixmap("icon.png"))
        self.search_image.setScaledContents(True)
        self.search_image.setAlignment(QtCore.Qt.AlignCenter)
        self.search_image.setWordWrap(False)
        self.search_image.setIndent(-1)
        self.search_image.setObjectName("search_image")
        self.open_image_button = QtWidgets.QPushButton(self.centralwidget)
        self.open_image_button.setGeometry(QtCore.QRect(20, 280, 93, 28))
        self.open_image_button.setObjectName("open_image_button")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(580, 20, 55, 16))
        self.label_2.setObjectName("label_2")
        self.run_button = QtWidgets.QPushButton(self.centralwidget)
        self.run_button.setGeometry(QtCore.QRect(20, 580, 251, 81))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.run_button.setFont(font)
        self.run_button.setAutoExclusive(False)
        self.run_button.setAutoDefault(False)
        self.run_button.setDefault(True)
        self.run_button.setObjectName("run_button")
        self.output_tree = QtWidgets.QTreeWidget(self.centralwidget)
        self.output_tree.setGeometry(QtCore.QRect(580, 40, 501, 621))
        self.output_tree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.output_tree.setTabKeyNavigation(True)
        self.output_tree.setProperty("showDropIndicator", False)
        self.output_tree.setAlternatingRowColors(True)
        self.output_tree.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.output_tree.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.output_tree.setRootIsDecorated(True)
        self.output_tree.setUniformRowHeights(False)
        self.output_tree.setItemsExpandable(True)
        self.output_tree.setAnimated(False)
        self.output_tree.setAllColumnsShowFocus(False)
        self.output_tree.setHeaderHidden(False)
        self.output_tree.setObjectName("output_tree")
        self.output_tree.header().setCascadingSectionResizes(True)
        self.output_tree.header().setDefaultSectionSize(200)
        self.output_tree.header().setHighlightSections(False)
        self.output_tree.header().setMinimumSectionSize(200)
        self.output_tree.header().setStretchLastSection(False)
        self.api_key_button = QtWidgets.QPushButton(self.centralwidget)
        self.api_key_button.setGeometry(QtCore.QRect(20, 540, 101, 31))
        self.api_key_button.setObjectName("api_key_button")
        self.clear_button = QtWidgets.QPushButton(self.centralwidget)
        self.clear_button.setGeometry(QtCore.QRect(310, 340, 93, 28))
        self.clear_button.setObjectName("clear_button")
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(310, 20, 241, 311))
        self.groupBox_3.setObjectName("groupBox_3")
        self.mac_input = QtWidgets.QLineEdit(self.groupBox_3)
        self.mac_input.setGeometry(QtCore.QRect(110, 270, 121, 22))
        self.mac_input.setObjectName("mac_input")
        self.email_input = QtWidgets.QLineEdit(self.groupBox_3)
        self.email_input.setGeometry(QtCore.QRect(110, 90, 121, 22))
        self.email_input.setInputMask("")
        self.email_input.setObjectName("email_input")
        self.crypto_input = QtWidgets.QLineEdit(self.groupBox_3)
        self.crypto_input.setGeometry(QtCore.QRect(110, 180, 121, 22))
        self.crypto_input.setObjectName("crypto_input")
        self.label_5 = QtWidgets.QLabel(self.groupBox_3)
        self.label_5.setGeometry(QtCore.QRect(10, 90, 71, 21))
        self.label_5.setObjectName("label_5")
        self.ip_input = QtWidgets.QLineEdit(self.groupBox_3)
        self.ip_input.setGeometry(QtCore.QRect(110, 60, 121, 22))
        self.ip_input.setInputMask("")
        self.ip_input.setText("")
        self.ip_input.setObjectName("ip_input")
        self.label_8 = QtWidgets.QLabel(self.groupBox_3)
        self.label_8.setGeometry(QtCore.QRect(10, 180, 91, 21))
        self.label_8.setObjectName("label_8")
        self.bssid_input = QtWidgets.QLineEdit(self.groupBox_3)
        self.bssid_input.setGeometry(QtCore.QRect(110, 240, 121, 22))
        self.bssid_input.setObjectName("bssid_input")
        self.ssid_input = QtWidgets.QLineEdit(self.groupBox_3)
        self.ssid_input.setGeometry(QtCore.QRect(110, 210, 121, 22))
        self.ssid_input.setText("")
        self.ssid_input.setObjectName("ssid_input")
        self.phone_input = QtWidgets.QLineEdit(self.groupBox_3)
        self.phone_input.setGeometry(QtCore.QRect(110, 150, 121, 22))
        self.phone_input.setObjectName("phone_input")
        self.label_7 = QtWidgets.QLabel(self.groupBox_3)
        self.label_7.setGeometry(QtCore.QRect(10, 150, 91, 21))
        self.label_7.setObjectName("label_7")
        self.label_9 = QtWidgets.QLabel(self.groupBox_3)
        self.label_9.setGeometry(QtCore.QRect(10, 210, 91, 21))
        self.label_9.setObjectName("label_9")
        self.username_input = QtWidgets.QLineEdit(self.groupBox_3)
        self.username_input.setGeometry(QtCore.QRect(110, 30, 121, 22))
        self.username_input.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.username_input.setObjectName("username_input")
        self.label_3 = QtWidgets.QLabel(self.groupBox_3)
        self.label_3.setGeometry(QtCore.QRect(10, 30, 71, 21))
        self.label_3.setObjectName("label_3")
        self.label_6 = QtWidgets.QLabel(self.groupBox_3)
        self.label_6.setGeometry(QtCore.QRect(10, 120, 71, 21))
        self.label_6.setObjectName("label_6")
        self.label_4 = QtWidgets.QLabel(self.groupBox_3)
        self.label_4.setGeometry(QtCore.QRect(10, 60, 71, 21))
        self.label_4.setObjectName("label_4")
        self.label_15 = QtWidgets.QLabel(self.groupBox_3)
        self.label_15.setGeometry(QtCore.QRect(10, 270, 91, 21))
        self.label_15.setObjectName("label_15")
        self.label_10 = QtWidgets.QLabel(self.groupBox_3)
        self.label_10.setGeometry(QtCore.QRect(10, 240, 91, 21))
        self.label_10.setObjectName("label_10")
        self.domain_input = QtWidgets.QLineEdit(self.groupBox_3)
        self.domain_input.setGeometry(QtCore.QRect(110, 120, 121, 22))
        self.domain_input.setObjectName("domain_input")
        self.image_search_checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.image_search_checkBox.setGeometry(QtCore.QRect(20, 360, 81, 31))
        self.image_search_checkBox.setObjectName("image_search_checkBox")
        self.total_progress = QtWidgets.QProgressBar(self.centralwidget)
        self.total_progress.setGeometry(QtCore.QRect(10, 690, 1081, 20))
        self.total_progress.setProperty("value", 0)
        self.total_progress.setTextVisible(True)
        self.total_progress.setOrientation(QtCore.Qt.Horizontal)
        self.total_progress.setInvertedAppearance(False)
        self.total_progress.setTextDirection(QtWidgets.QProgressBar.BottomToTop)
        self.total_progress.setObjectName("total_progress")
        self.label_16 = QtWidgets.QLabel(self.centralwidget)
        self.label_16.setGeometry(QtCore.QRect(10, 670, 61, 16))
        self.label_16.setObjectName("label_16")
        self.label_17 = QtWidgets.QLabel(self.centralwidget)
        self.label_17.setGeometry(QtCore.QRect(310, 390, 131, 21))
        self.label_17.setObjectName("label_17")
        self.thread_input = QtWidgets.QSpinBox(self.centralwidget)
        self.thread_input.setGeometry(QtCore.QRect(440, 390, 101, 22))
        self.thread_input.setMaximum(999)
        self.thread_input.setProperty("value", 20)
        self.thread_input.setObjectName("thread_input")
        self.refresh_button = QtWidgets.QPushButton(self.centralwidget)
        self.refresh_button.setGeometry(QtCore.QRect(410, 340, 93, 28))
        self.refresh_button.setObjectName("refresh_button")
        self.module_progress_label = QtWidgets.QLabel(self.centralwidget)
        self.module_progress_label.setGeometry(QtCore.QRect(70, 670, 981, 16))
        self.module_progress_label.setText("")
        self.module_progress_label.setObjectName("module_progress_label")
        self.open_image_output_button = QtWidgets.QPushButton(self.centralwidget)
        self.open_image_output_button.setGeometry(QtCore.QRect(120, 280, 93, 28))
        self.open_image_output_button.setToolTip("")
        self.open_image_output_button.setObjectName("open_image_output_button")
        self.image_search_mode_comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.image_search_mode_comboBox.setGeometry(QtCore.QRect(70, 320, 201, 31))
        self.image_search_mode_comboBox.setObjectName("image_search_mode_comboBox")
        self.image_search_mode_comboBox.addItem("")
        self.image_search_mode_comboBox.addItem("")
        self.image_search_mode_comboBox.addItem("")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 320, 51, 31))
        self.label.setObjectName("label")
        self.keep_data_checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.keep_data_checkBox.setGeometry(QtCore.QRect(310, 420, 81, 20))
        self.keep_data_checkBox.setObjectName("keep_data_checkBox")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(20, 390, 251, 81))
        self.groupBox_2.setObjectName("groupBox_2")
        self.label_18 = QtWidgets.QLabel(self.groupBox_2)
        self.label_18.setGeometry(QtCore.QRect(10, 30, 131, 21))
        self.label_18.setObjectName("label_18")
        self.num_predictions_input = QtWidgets.QSpinBox(self.groupBox_2)
        self.num_predictions_input.setGeometry(QtCore.QRect(140, 30, 101, 22))
        self.num_predictions_input.setMinimum(1)
        self.num_predictions_input.setMaximum(999)
        self.num_predictions_input.setProperty("value", 5)
        self.num_predictions_input.setObjectName("num_predictions_input")
        self.quota_button = QtWidgets.QPushButton(self.centralwidget)
        self.quota_button.setGeometry(QtCore.QRect(130, 540, 101, 31))
        self.quota_button.setObjectName("quota_button")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1099, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionExport = QtWidgets.QAction(MainWindow)
        self.actionExport.setObjectName("actionExport")
        self.actionConfiguration = QtWidgets.QAction(MainWindow)
        self.actionConfiguration.setObjectName("actionConfiguration")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionExport)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionAbout)
        self.menuFile.addAction(self.actionQuit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.open_image_button, self.username_input)
        MainWindow.setTabOrder(self.username_input, self.ip_input)
        MainWindow.setTabOrder(self.ip_input, self.email_input)
        MainWindow.setTabOrder(self.email_input, self.domain_input)
        MainWindow.setTabOrder(self.domain_input, self.phone_input)
        MainWindow.setTabOrder(self.phone_input, self.crypto_input)
        MainWindow.setTabOrder(self.crypto_input, self.ssid_input)
        MainWindow.setTabOrder(self.ssid_input, self.bssid_input)
        MainWindow.setTabOrder(self.bssid_input, self.mac_input)
        MainWindow.setTabOrder(self.mac_input, self.clear_button)
        MainWindow.setTabOrder(self.clear_button, self.api_key_button)
        MainWindow.setTabOrder(self.api_key_button, self.run_button)
        MainWindow.setTabOrder(self.run_button, self.output_tree)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Autosint"))
        self.groupBox.setTitle(_translate("MainWindow", "Image tools"))
        self.open_image_button.setText(_translate("MainWindow", "Open Image"))
        self.label_2.setText(_translate("MainWindow", "Output"))
        self.run_button.setText(_translate("MainWindow", "Run"))
        self.output_tree.setSortingEnabled(True)
        self.output_tree.headerItem().setText(0, _translate("MainWindow", "Name"))
        self.output_tree.headerItem().setText(1, _translate("MainWindow", "Value"))
        self.api_key_button.setText(_translate("MainWindow", "API keys"))
        self.clear_button.setToolTip(_translate("MainWindow", "Clears input and output forms"))
        self.clear_button.setText(_translate("MainWindow", "Clear"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Search parameters"))
        self.mac_input.setInputMask(_translate("MainWindow", "HH:HH:HH:HH:HH:HH"))
        self.mac_input.setText(_translate("MainWindow", ":::::"))
        self.label_5.setText(_translate("MainWindow", "E-Mail"))
        self.label_8.setText(_translate("MainWindow", "BTC Adress"))
        self.bssid_input.setInputMask(_translate("MainWindow", "HH:HH:HH:HH:HH:HH"))
        self.bssid_input.setText(_translate("MainWindow", ":::::"))
        self.label_7.setText(_translate("MainWindow", "Phone Number"))
        self.label_9.setText(_translate("MainWindow", "WIFI SSID"))
        self.label_3.setText(_translate("MainWindow", "Username"))
        self.label_6.setText(_translate("MainWindow", "Domain"))
        self.label_4.setText(_translate("MainWindow", "IP"))
        self.label_15.setText(_translate("MainWindow", "MAC Adress"))
        self.label_10.setText(_translate("MainWindow", "WIFI BSSID"))
        self.image_search_checkBox.setText(_translate("MainWindow", "Do search"))
        self.label_16.setText(_translate("MainWindow", "Progress:"))
        self.label_17.setText(_translate("MainWindow", "User search Threads"))
        self.refresh_button.setText(_translate("MainWindow", "Refresh"))
        self.open_image_output_button.setText(_translate("MainWindow", "Open output"))
        self.image_search_mode_comboBox.setItemText(0, _translate("MainWindow", "Metadata"))
        self.image_search_mode_comboBox.setItemText(1, _translate("MainWindow", "AI Geolocate"))
        self.image_search_mode_comboBox.setItemText(2, _translate("MainWindow", "Astro Locate"))
        self.label.setText(_translate("MainWindow", "Mode:"))
        self.keep_data_checkBox.setToolTip(_translate("MainWindow", "Does not reset the output form on new run but if you search for a single thing twice the old one gets overwritten"))
        self.keep_data_checkBox.setText(_translate("MainWindow", "Keep data"))
        self.groupBox_2.setTitle(_translate("MainWindow", "AI Geolocate Parameters"))
        self.label_18.setText(_translate("MainWindow", "Num. predictions"))
        self.quota_button.setText(_translate("MainWindow", "Get Quota"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.actionQuit.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.actionExport.setText(_translate("MainWindow", "Export"))
        self.actionExport.setShortcut(_translate("MainWindow", "Ctrl+E"))
        self.actionConfiguration.setText(_translate("MainWindow", "Configuration"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O"))
