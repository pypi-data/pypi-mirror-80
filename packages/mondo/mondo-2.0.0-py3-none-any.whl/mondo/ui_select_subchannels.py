# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'select_subchannels.ui'
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


class Ui_SelectSubchannelsDialog(object):
    def setupUi(self, SelectSubchannelsDialog):
        if not SelectSubchannelsDialog.objectName():
            SelectSubchannelsDialog.setObjectName(u"SelectSubchannelsDialog")
        SelectSubchannelsDialog.resize(400, 49)
        self.verticalLayout_2 = QVBoxLayout(SelectSubchannelsDialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")

        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.buttonBox = QDialogButtonBox(SelectSubchannelsDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout_2.addWidget(self.buttonBox)


        self.retranslateUi(SelectSubchannelsDialog)
        self.buttonBox.accepted.connect(SelectSubchannelsDialog.accept)
        self.buttonBox.rejected.connect(SelectSubchannelsDialog.reject)

        QMetaObject.connectSlotsByName(SelectSubchannelsDialog)
    # setupUi

    def retranslateUi(self, SelectSubchannelsDialog):
        SelectSubchannelsDialog.setWindowTitle(QCoreApplication.translate("SelectSubchannelsDialog", u"Select Subchannels Channels", None))
    # retranslateUi

