# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'datetime_subset.ui'
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


class Ui_DateTimeSubsetDialog(object):
    def setupUi(self, DateTimeSubsetDialog):
        if not DateTimeSubsetDialog.objectName():
            DateTimeSubsetDialog.setObjectName(u"DateTimeSubsetDialog")
        DateTimeSubsetDialog.resize(283, 284)
        self.gridLayout = QGridLayout(DateTimeSubsetDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalSpacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 4, 0, 1, 3)

        self.useAllData = QRadioButton(DateTimeSubsetDialog)
        self.useAllData.setObjectName(u"useAllData")
        self.useAllData.setChecked(True)

        self.gridLayout.addWidget(self.useAllData, 0, 0, 1, 3)

        self.buttonBox = QDialogButtonBox(DateTimeSubsetDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.gridLayout.addWidget(self.buttonBox, 5, 0, 1, 3)

        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.formLayout_2.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        self.startLabel = QLabel(DateTimeSubsetDialog)
        self.startLabel.setObjectName(u"startLabel")
        self.startLabel.setEnabled(False)

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.startLabel)

        self.startDateTime = QDateTimeEdit(DateTimeSubsetDialog)
        self.startDateTime.setObjectName(u"startDateTime")
        self.startDateTime.setEnabled(False)
        self.startDateTime.setWrapping(True)

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.startDateTime)

        self.endLabel = QLabel(DateTimeSubsetDialog)
        self.endLabel.setObjectName(u"endLabel")
        self.endLabel.setEnabled(False)

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.endLabel)

        self.endDateTime = QDateTimeEdit(DateTimeSubsetDialog)
        self.endDateTime.setObjectName(u"endDateTime")
        self.endDateTime.setEnabled(False)
        self.endDateTime.setWrapping(True)

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.endDateTime)

        self.durationLabel = QLabel(DateTimeSubsetDialog)
        self.durationLabel.setObjectName(u"durationLabel")
        self.durationLabel.setEnabled(False)

        self.formLayout_2.setWidget(4, QFormLayout.LabelRole, self.durationLabel)

        self.label = QLabel(DateTimeSubsetDialog)
        self.label.setObjectName(u"label")
        self.label.setEnabled(False)

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.label)

        self.label_2 = QLabel(DateTimeSubsetDialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setEnabled(False)

        self.formLayout_2.setWidget(3, QFormLayout.LabelRole, self.label_2)

        self.startSeconds = QSpinBox(DateTimeSubsetDialog)
        self.startSeconds.setObjectName(u"startSeconds")
        self.startSeconds.setEnabled(False)

        self.formLayout_2.setWidget(2, QFormLayout.FieldRole, self.startSeconds)

        self.endSeconds = QSpinBox(DateTimeSubsetDialog)
        self.endSeconds.setObjectName(u"endSeconds")
        self.endSeconds.setEnabled(False)

        self.formLayout_2.setWidget(3, QFormLayout.FieldRole, self.endSeconds)

        self.duration = QSpinBox(DateTimeSubsetDialog)
        self.duration.setObjectName(u"duration")
        self.duration.setEnabled(False)

        self.formLayout_2.setWidget(4, QFormLayout.FieldRole, self.duration)


        self.gridLayout.addLayout(self.formLayout_2, 3, 1, 1, 2)

        self.horizontalSpacer = QSpacerItem(13, 13, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 3, 0, 1, 1)

        self.useSubset = QRadioButton(DateTimeSubsetDialog)
        self.useSubset.setObjectName(u"useSubset")

        self.gridLayout.addWidget(self.useSubset, 2, 0, 1, 3)

        self.formLayout_4 = QFormLayout()
        self.formLayout_4.setObjectName(u"formLayout_4")
        self.allStartLabel = QLabel(DateTimeSubsetDialog)
        self.allStartLabel.setObjectName(u"allStartLabel")

        self.formLayout_4.setWidget(0, QFormLayout.LabelRole, self.allStartLabel)

        self.allStart = QLabel(DateTimeSubsetDialog)
        self.allStart.setObjectName(u"allStart")

        self.formLayout_4.setWidget(0, QFormLayout.FieldRole, self.allStart)

        self.allEndLabel = QLabel(DateTimeSubsetDialog)
        self.allEndLabel.setObjectName(u"allEndLabel")

        self.formLayout_4.setWidget(1, QFormLayout.LabelRole, self.allEndLabel)

        self.allEnd = QLabel(DateTimeSubsetDialog)
        self.allEnd.setObjectName(u"allEnd")

        self.formLayout_4.setWidget(1, QFormLayout.FieldRole, self.allEnd)

        self.allDurationLabel = QLabel(DateTimeSubsetDialog)
        self.allDurationLabel.setObjectName(u"allDurationLabel")

        self.formLayout_4.setWidget(2, QFormLayout.LabelRole, self.allDurationLabel)

        self.allDuration = QLabel(DateTimeSubsetDialog)
        self.allDuration.setObjectName(u"allDuration")

        self.formLayout_4.setWidget(2, QFormLayout.FieldRole, self.allDuration)


        self.gridLayout.addLayout(self.formLayout_4, 1, 1, 1, 2)

        QWidget.setTabOrder(self.useAllData, self.useSubset)
        QWidget.setTabOrder(self.useSubset, self.startDateTime)
        QWidget.setTabOrder(self.startDateTime, self.endDateTime)
        QWidget.setTabOrder(self.endDateTime, self.buttonBox)

        self.retranslateUi(DateTimeSubsetDialog)
        self.buttonBox.accepted.connect(DateTimeSubsetDialog.accept)
        self.buttonBox.rejected.connect(DateTimeSubsetDialog.reject)
        self.useSubset.toggled.connect(self.startLabel.setEnabled)
        self.useSubset.toggled.connect(self.startDateTime.setEnabled)
        self.useSubset.toggled.connect(self.endLabel.setEnabled)
        self.useSubset.toggled.connect(self.endDateTime.setEnabled)
        self.useSubset.toggled.connect(self.durationLabel.setEnabled)
        self.useAllData.toggled.connect(self.allStartLabel.setEnabled)
        self.useAllData.toggled.connect(self.allStart.setEnabled)
        self.useAllData.toggled.connect(self.allEndLabel.setEnabled)
        self.useAllData.toggled.connect(self.allEnd.setEnabled)
        self.useAllData.toggled.connect(self.allDurationLabel.setEnabled)
        self.useAllData.toggled.connect(self.allDuration.setEnabled)
        self.useSubset.toggled.connect(self.label.setEnabled)
        self.useSubset.toggled.connect(self.label_2.setEnabled)
        self.useSubset.toggled.connect(self.startSeconds.setEnabled)
        self.useSubset.toggled.connect(self.endSeconds.setEnabled)
        self.useSubset.toggled.connect(self.duration.setEnabled)

        QMetaObject.connectSlotsByName(DateTimeSubsetDialog)
    # setupUi

    def retranslateUi(self, DateTimeSubsetDialog):
        DateTimeSubsetDialog.setWindowTitle(QCoreApplication.translate("DateTimeSubsetDialog", u"Select Data Range", None))
        self.useAllData.setText(QCoreApplication.translate("DateTimeSubsetDialog", u"Use all data", None))
        self.startLabel.setText(QCoreApplication.translate("DateTimeSubsetDialog", u"Start Time (UTC):", None))
        self.startDateTime.setDisplayFormat(QCoreApplication.translate("DateTimeSubsetDialog", u"M/d/yyyy h:mm:ss AP", None))
        self.endLabel.setText(QCoreApplication.translate("DateTimeSubsetDialog", u"End Time (UTC):", None))
        self.endDateTime.setDisplayFormat(QCoreApplication.translate("DateTimeSubsetDialog", u"M/d/yyyy h:mm:ss AP", None))
        self.durationLabel.setText(QCoreApplication.translate("DateTimeSubsetDialog", u"Duration:", None))
        self.label.setText(QCoreApplication.translate("DateTimeSubsetDialog", u"Relative Start Time", None))
        self.label_2.setText(QCoreApplication.translate("DateTimeSubsetDialog", u"Relative End Time", None))
        self.startSeconds.setSuffix(QCoreApplication.translate("DateTimeSubsetDialog", u" s", None))
        self.endSeconds.setSuffix(QCoreApplication.translate("DateTimeSubsetDialog", u" s", None))
        self.duration.setSuffix(QCoreApplication.translate("DateTimeSubsetDialog", u" s", None))
        self.useSubset.setText(QCoreApplication.translate("DateTimeSubsetDialog", u"Use data within range", None))
        self.allStartLabel.setText(QCoreApplication.translate("DateTimeSubsetDialog", u"Start Time (UTC):", None))
        self.allStart.setText(QCoreApplication.translate("DateTimeSubsetDialog", u"1/1/2000 12:00:00 AM", None))
        self.allEndLabel.setText(QCoreApplication.translate("DateTimeSubsetDialog", u"End Time (UTC):", None))
        self.allEnd.setText(QCoreApplication.translate("DateTimeSubsetDialog", u"1/1/2000 12:00:00 AM", None))
        self.allDurationLabel.setText(QCoreApplication.translate("DateTimeSubsetDialog", u"Duration:", None))
        self.allDuration.setText(QCoreApplication.translate("DateTimeSubsetDialog", u"0 s", None))
    # retranslateUi

