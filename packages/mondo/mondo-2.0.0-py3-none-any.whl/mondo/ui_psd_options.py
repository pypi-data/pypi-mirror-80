# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'psd_options.ui'
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


class Ui_PSDOptionsWidget(object):
    def setupUi(self, PSDOptionsWidget):
        if not PSDOptionsWidget.objectName():
            PSDOptionsWidget.setObjectName(u"PSDOptionsWidget")
        PSDOptionsWidget.resize(208, 191)
        self.formLayout = QFormLayout(PSDOptionsWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName(u"formLayout")
        self.fftPointsLabel = QLabel(PSDOptionsWidget)
        self.fftPointsLabel.setObjectName(u"fftPointsLabel")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.fftPointsLabel)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_4)

        self.fftPoints = QComboBox(PSDOptionsWidget)
        self.fftPoints.setObjectName(u"fftPoints")

        self.horizontalLayout_4.addWidget(self.fftPoints)


        self.formLayout.setLayout(0, QFormLayout.FieldRole, self.horizontalLayout_4)

        self.durationLabel = QLabel(PSDOptionsWidget)
        self.durationLabel.setObjectName(u"durationLabel")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.durationLabel)

        self.duration = QLabel(PSDOptionsWidget)
        self.duration.setObjectName(u"duration")
        self.duration.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.duration)

        self.resolutionLabel = QLabel(PSDOptionsWidget)
        self.resolutionLabel.setObjectName(u"resolutionLabel")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.resolutionLabel)

        self.resolution = QLabel(PSDOptionsWidget)
        self.resolution.setObjectName(u"resolution")
        self.resolution.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.resolution)

        self.overlapPercentLabel = QLabel(PSDOptionsWidget)
        self.overlapPercentLabel.setObjectName(u"overlapPercentLabel")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.overlapPercentLabel)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)

        self.overlapPercent = QDoubleSpinBox(PSDOptionsWidget)
        self.overlapPercent.setObjectName(u"overlapPercent")
        self.overlapPercent.setMinimumSize(QSize(75, 0))
        self.overlapPercent.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.overlapPercent.setDecimals(0)
        self.overlapPercent.setMaximum(95.000000000000000)
        self.overlapPercent.setSingleStep(5.000000000000000)
        self.overlapPercent.setValue(75.000000000000000)

        self.horizontalLayout_3.addWidget(self.overlapPercent)


        self.formLayout.setLayout(3, QFormLayout.FieldRole, self.horizontalLayout_3)

        self.overlapPointsLabel = QLabel(PSDOptionsWidget)
        self.overlapPointsLabel.setObjectName(u"overlapPointsLabel")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.overlapPointsLabel)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_5)

        self.overlapPoints = QSpinBox(PSDOptionsWidget)
        self.overlapPoints.setObjectName(u"overlapPoints")
        self.overlapPoints.setMinimumSize(QSize(75, 0))
        self.overlapPoints.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.overlapPoints)


        self.formLayout.setLayout(4, QFormLayout.FieldRole, self.horizontalLayout_5)

        self.windowCountLabel = QLabel(PSDOptionsWidget)
        self.windowCountLabel.setObjectName(u"windowCountLabel")

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.windowCountLabel)

        self.windowCount = QLabel(PSDOptionsWidget)
        self.windowCount.setObjectName(u"windowCount")
        self.windowCount.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.windowCount)

        self.windowFunctionLabel = QLabel(PSDOptionsWidget)
        self.windowFunctionLabel.setObjectName(u"windowFunctionLabel")

        self.formLayout.setWidget(6, QFormLayout.LabelRole, self.windowFunctionLabel)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.windowFunction = QComboBox(PSDOptionsWidget)
        self.windowFunction.setObjectName(u"windowFunction")

        self.horizontalLayout_2.addWidget(self.windowFunction)


        self.formLayout.setLayout(6, QFormLayout.FieldRole, self.horizontalLayout_2)

        self.detrendMethodLabel = QLabel(PSDOptionsWidget)
        self.detrendMethodLabel.setObjectName(u"detrendMethodLabel")

        self.formLayout.setWidget(7, QFormLayout.LabelRole, self.detrendMethodLabel)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.detrendMethod = QComboBox(PSDOptionsWidget)
        self.detrendMethod.setObjectName(u"detrendMethod")

        self.horizontalLayout.addWidget(self.detrendMethod)


        self.formLayout.setLayout(7, QFormLayout.FieldRole, self.horizontalLayout)


        self.retranslateUi(PSDOptionsWidget)

        QMetaObject.connectSlotsByName(PSDOptionsWidget)
    # setupUi

    def retranslateUi(self, PSDOptionsWidget):
        PSDOptionsWidget.setWindowTitle(QCoreApplication.translate("PSDOptionsWidget", u"PSD Options", None))
        self.fftPointsLabel.setText(QCoreApplication.translate("PSDOptionsWidget", u"FFT Window Size", None))
        self.durationLabel.setText(QCoreApplication.translate("PSDOptionsWidget", u"Window Duration", None))
        self.duration.setText(QCoreApplication.translate("PSDOptionsWidget", u"600 s", None))
        self.resolutionLabel.setText(QCoreApplication.translate("PSDOptionsWidget", u"Frequency Resolution", None))
        self.resolution.setText(QCoreApplication.translate("PSDOptionsWidget", u"0.1 Hz", None))
        self.overlapPercentLabel.setText(QCoreApplication.translate("PSDOptionsWidget", u"Window Overlap Percent", None))
        self.overlapPercent.setSuffix(QCoreApplication.translate("PSDOptionsWidget", u" %", None))
        self.overlapPointsLabel.setText(QCoreApplication.translate("PSDOptionsWidget", u"Window Overlap Points", None))
        self.windowCountLabel.setText(QCoreApplication.translate("PSDOptionsWidget", u"Number of Windows", None))
        self.windowCount.setText(QCoreApplication.translate("PSDOptionsWidget", u"1", None))
        self.windowFunctionLabel.setText(QCoreApplication.translate("PSDOptionsWidget", u"Window Function", None))
        self.detrendMethodLabel.setText(QCoreApplication.translate("PSDOptionsWidget", u"Detrend Method", None))
    # retranslateUi

