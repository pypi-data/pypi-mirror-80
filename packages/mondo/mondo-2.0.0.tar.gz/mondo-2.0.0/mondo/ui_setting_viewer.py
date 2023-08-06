# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'setting_viewer.ui'
##
## Created by: Qt User Interface Compiler version 5.15.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *


class Ui_SettingViewerDialog(object):
    def setupUi(self, SettingViewerDialog):
        if not SettingViewerDialog.objectName():
            SettingViewerDialog.setObjectName(u"SettingViewerDialog")
        SettingViewerDialog.resize(400, 53)
        self.verticalLayout = QVBoxLayout(SettingViewerDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tabWidget = QTabWidget(SettingViewerDialog)
        self.tabWidget.setObjectName(u"tabWidget")

        self.verticalLayout.addWidget(self.tabWidget)

        self.buttonBox = QDialogButtonBox(SettingViewerDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Close)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(SettingViewerDialog)
        self.buttonBox.accepted.connect(SettingViewerDialog.accept)
        self.buttonBox.rejected.connect(SettingViewerDialog.reject)

        QMetaObject.connectSlotsByName(SettingViewerDialog)
    # setupUi

    def retranslateUi(self, SettingViewerDialog):
        SettingViewerDialog.setWindowTitle(QCoreApplication.translate("SettingViewerDialog", u"Device Settings", None))
    # retranslateUi

