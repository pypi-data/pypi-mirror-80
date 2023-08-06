# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'select_synchronous.ui'
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


class Ui_SelectSynchronousDialog(object):
    def setupUi(self, SelectSynchronousDialog):
        if not SelectSynchronousDialog.objectName():
            SelectSynchronousDialog.setObjectName(u"SelectSynchronousDialog")
        SelectSynchronousDialog.resize(400, 49)
        self.verticalLayout_2 = QVBoxLayout(SelectSynchronousDialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")

        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.buttonBox = QDialogButtonBox(SelectSynchronousDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout_2.addWidget(self.buttonBox)


        self.retranslateUi(SelectSynchronousDialog)
        self.buttonBox.accepted.connect(SelectSynchronousDialog.accept)
        self.buttonBox.rejected.connect(SelectSynchronousDialog.reject)

        QMetaObject.connectSlotsByName(SelectSynchronousDialog)
    # setupUi

    def retranslateUi(self, SelectSynchronousDialog):
        SelectSynchronousDialog.setWindowTitle(QCoreApplication.translate("SelectSynchronousDialog", u"Select Synchronous Channels", None))
    # retranslateUi

