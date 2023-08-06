# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'about.ui'
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


class Ui_AboutDialog(object):
    def setupUi(self, AboutDialog):
        if not AboutDialog.objectName():
            AboutDialog.setObjectName(u"AboutDialog")
        AboutDialog.resize(505, 506)
        self.verticalLayout = QVBoxLayout(AboutDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setVerticalSpacing(20)
        self.label = QLabel(AboutDialog)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.softwareLabel = QLabel(AboutDialog)
        self.softwareLabel.setObjectName(u"softwareLabel")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.softwareLabel.sizePolicy().hasHeightForWidth())
        self.softwareLabel.setSizePolicy(sizePolicy)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.softwareLabel)

        self.label_4 = QLabel(AboutDialog)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_4)

        self.label_9 = QLabel(AboutDialog)
        self.label_9.setObjectName(u"label_9")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy1)
        self.label_9.setWordWrap(True)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.label_9)

        self.label_5 = QLabel(AboutDialog)
        self.label_5.setObjectName(u"label_5")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_5)

        self.label_10 = QLabel(AboutDialog)
        self.label_10.setObjectName(u"label_10")
        sizePolicy.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy)
        self.label_10.setWordWrap(True)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.label_10)

        self.label_6 = QLabel(AboutDialog)
        self.label_6.setObjectName(u"label_6")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_6)

        self.label_11 = QLabel(AboutDialog)
        self.label_11.setObjectName(u"label_11")
        sizePolicy.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy)
        self.label_11.setWordWrap(True)

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.label_11)

        self.label_7 = QLabel(AboutDialog)
        self.label_7.setObjectName(u"label_7")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.label_7)

        self.label_12 = QLabel(AboutDialog)
        self.label_12.setObjectName(u"label_12")
        sizePolicy.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy)
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_12.setFont(font)
        self.label_12.setWordWrap(True)

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.label_12)


        self.verticalLayout.addLayout(self.formLayout)

        self.buttonBox = QDialogButtonBox(AboutDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(AboutDialog)
        self.buttonBox.accepted.connect(AboutDialog.accept)
        self.buttonBox.rejected.connect(AboutDialog.reject)

        QMetaObject.connectSlotsByName(AboutDialog)
    # setupUi

    def retranslateUi(self, AboutDialog):
        AboutDialog.setWindowTitle(QCoreApplication.translate("AboutDialog", u"About", None))
        self.label.setText(QCoreApplication.translate("AboutDialog", u"Software:", None))
        self.softwareLabel.setText(QCoreApplication.translate("AboutDialog", u"Mondo\n"
"Version: {}\n"
"Build Date: {}", None))
        self.label_4.setText(QCoreApplication.translate("AboutDialog", u"Support:", None))
        self.label_9.setText(QCoreApplication.translate("AboutDialog", u"This software is provided by EPRI \"AS IS\" and without customer support beyond such embodiments within the distribution of this software that may or may not provide such support.", None))
        self.label_5.setText(QCoreApplication.translate("AboutDialog", u"Copyright:", None))
        self.label_10.setText(QCoreApplication.translate("AboutDialog", u"Copyright (c) 2016 Electric Power Research Institute, Inc.\n"
"Copyright (c) 2020 Suprock Technologies, LLC\n"
"All rights reserved.\n"
"\n"
"Permission to use, copy, modify, and distribute this software for any purpose with or without fee is hereby granted, provided that the above copyright notice and this permission notice appear in all copies.", None))
        self.label_6.setText(QCoreApplication.translate("AboutDialog", u"Developed by:", None))
        self.label_11.setText(QCoreApplication.translate("AboutDialog", u"Suprock Technologies\n"
"45 Scott Hill Rd\n"
"Warren, NH 03279", None))
        self.label_7.setText(QCoreApplication.translate("AboutDialog", u"Disclaimer:", None))
        self.label_12.setText(QCoreApplication.translate("AboutDialog", u"THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS \"AS IS\" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL EPRI BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.", None))
    # retranslateUi

