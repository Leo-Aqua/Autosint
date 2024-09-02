# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'apikeys.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QMainWindow,
    QMenuBar, QPushButton, QSizePolicy, QStatusBar,
    QWidget)

class Ui_PopupWindow(object):
    def setupUi(self, PopupWindow):
        if not PopupWindow.objectName():
            PopupWindow.setObjectName(u"PopupWindow")
        PopupWindow.resize(457, 569)
        self.centralwidget = QWidget(PopupWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.criminalip_key = QLineEdit(self.centralwidget)
        self.criminalip_key.setObjectName(u"criminalip_key")
        self.criminalip_key.setGeometry(QRect(110, 30, 321, 22))
        self.criminalip_key.setEchoMode(QLineEdit.Password)
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(20, 30, 81, 21))
        self.label.setOpenExternalLinks(True)
        self.save_button = QPushButton(self.centralwidget)
        self.save_button.setObjectName(u"save_button")
        self.save_button.setGeometry(QRect(340, 480, 93, 28))
        self.cancel_button = QPushButton(self.centralwidget)
        self.cancel_button.setObjectName(u"cancel_button")
        self.cancel_button.setGeometry(QRect(240, 480, 93, 28))
        self.warning_label = QLabel(self.centralwidget)
        self.warning_label.setObjectName(u"warning_label")
        self.warning_label.setGeometry(QRect(10, 480, 221, 41))
        font = QFont()
        font.setPointSize(9)
        font.setUnderline(True)
        self.warning_label.setFont(font)
        self.warning_label.setWordWrap(True)
        self.apilayer_key = QLineEdit(self.centralwidget)
        self.apilayer_key.setObjectName(u"apilayer_key")
        self.apilayer_key.setGeometry(QRect(110, 70, 321, 22))
        self.apilayer_key.setEchoMode(QLineEdit.Password)
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(20, 70, 81, 21))
        self.label_2.setOpenExternalLinks(True)
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(20, 110, 81, 21))
        self.label_3.setOpenExternalLinks(True)
        self.wigle_key = QLineEdit(self.centralwidget)
        self.wigle_key.setObjectName(u"wigle_key")
        self.wigle_key.setGeometry(QRect(110, 110, 321, 22))
        self.wigle_key.setEchoMode(QLineEdit.Password)
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(20, 150, 81, 21))
        self.label_4.setOpenExternalLinks(True)
        self.astro_key = QLineEdit(self.centralwidget)
        self.astro_key.setObjectName(u"astro_key")
        self.astro_key.setGeometry(QRect(110, 150, 321, 22))
        self.astro_key.setEchoMode(QLineEdit.Password)
        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(20, 190, 401, 181))
        self.label_5.setOpenExternalLinks(True)
        PopupWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(PopupWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 457, 26))
        PopupWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(PopupWindow)
        self.statusbar.setObjectName(u"statusbar")
        PopupWindow.setStatusBar(self.statusbar)

        self.retranslateUi(PopupWindow)

        self.save_button.setDefault(True)


        QMetaObject.connectSlotsByName(PopupWindow)
    # setupUi

    def retranslateUi(self, PopupWindow):
        PopupWindow.setWindowTitle(QCoreApplication.translate("PopupWindow", u"API Keys", None))
        self.label.setText(QCoreApplication.translate("PopupWindow", u"<a href=\"https://www.criminalip.io/mypage/information\">Criminal IP</a>", None))
        self.save_button.setText(QCoreApplication.translate("PopupWindow", u"Save", None))
        self.cancel_button.setText(QCoreApplication.translate("PopupWindow", u"Cancel", None))
        self.warning_label.setText(QCoreApplication.translate("PopupWindow", u"WARNING: Keys are not encrypted! Use at your own risk!", None))
        self.apilayer_key.setText("")
        self.label_2.setText(QCoreApplication.translate("PopupWindow", u"<a href=\"https://apilayer.com/\">Apilayer</a>", None))
#if QT_CONFIG(tooltip)
        self.label_3.setToolTip(QCoreApplication.translate("PopupWindow", u"Use \"Encoded for use\" key", None))
#endif // QT_CONFIG(tooltip)
        self.label_3.setText(QCoreApplication.translate("PopupWindow", u"<a href=\"https://wigle.net/account\">Wigle.net</a>", None))
        self.wigle_key.setText("")
#if QT_CONFIG(tooltip)
        self.label_4.setToolTip(QCoreApplication.translate("PopupWindow", u"Use \"Encoded for use\" key", None))
#endif // QT_CONFIG(tooltip)
        self.label_4.setText(QCoreApplication.translate("PopupWindow", u"<a href=\"https://nova.astrometry.net/api_help\">Astrometry</a>", None))
        self.astro_key.setText("")
        self.label_5.setText(QCoreApplication.translate("PopupWindow", u"<html>\n"
"   <head/>\n"
"   <body>\n"
"      <p><span style=\" font-size:10pt; font-weight:600;\">IMPORTANT</span><br/></p>\n"
"      <p>You have to subscribe to the following APIs to use the Apilayer APIs</p>\n"
"      <p>(they're free, but you can buy them for more quota)</p>\n"
"      <p>- <a href=\"https://apilayer.com/marketplace/dns_lookup-api\"><span>DNS Lookup</span></a></p>\n"
"      <p>- <a href=\"https://apilayer.com/marketplace/number_verification-api\"><span>Number Verification</span></a></p>\n"
"      <p>- <a href=\"https://apilayer.com/marketplace/whois-api\"><span>Whois</span></a></p>\n"
"   </body>\n"
"</html>", None))
    # retranslateUi

