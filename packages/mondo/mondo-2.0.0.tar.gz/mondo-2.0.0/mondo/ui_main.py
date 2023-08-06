# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
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


class Ui_MondoMainWindow(object):
    def setupUi(self, MondoMainWindow):
        if not MondoMainWindow.objectName():
            MondoMainWindow.setObjectName(u"MondoMainWindow")
        MondoMainWindow.resize(617, 351)
        self.actionAbout = QAction(MondoMainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.actionExit = QAction(MondoMainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.actionAboutLibraries = QAction(MondoMainWindow)
        self.actionAboutLibraries.setObjectName(u"actionAboutLibraries")
        self.actionUpdateLatestStable = QAction(MondoMainWindow)
        self.actionUpdateLatestStable.setObjectName(u"actionUpdateLatestStable")
        self.actionUpdateSpecificBranch = QAction(MondoMainWindow)
        self.actionUpdateSpecificBranch.setObjectName(u"actionUpdateSpecificBranch")
        self.actionUpdateSpecificCommit = QAction(MondoMainWindow)
        self.actionUpdateSpecificCommit.setObjectName(u"actionUpdateSpecificCommit")
        self.actionUpdateCurrentBranch = QAction(MondoMainWindow)
        self.actionUpdateCurrentBranch.setObjectName(u"actionUpdateCurrentBranch")
        self.actionPreferences = QAction(MondoMainWindow)
        self.actionPreferences.setObjectName(u"actionPreferences")
        self.centralwidget = QWidget(MondoMainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_5 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.psdButton = QPushButton(self.groupBox)
        self.psdButton.setObjectName(u"psdButton")
        self.psdButton.setMinimumSize(QSize(175, 0))

        self.verticalLayout.addWidget(self.psdButton)

        self.singleChannelPsdButton = QPushButton(self.groupBox)
        self.singleChannelPsdButton.setObjectName(u"singleChannelPsdButton")

        self.verticalLayout.addWidget(self.singleChannelPsdButton)

        self.singleSlicePsdButton = QPushButton(self.groupBox)
        self.singleSlicePsdButton.setObjectName(u"singleSlicePsdButton")

        self.verticalLayout.addWidget(self.singleSlicePsdButton)

        self.overlaidPsdButton = QPushButton(self.groupBox)
        self.overlaidPsdButton.setObjectName(u"overlaidPsdButton")
        self.overlaidPsdButton.setMinimumSize(QSize(175, 0))

        self.verticalLayout.addWidget(self.overlaidPsdButton)

        self.verticalSpacer = QSpacerItem(20, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.gridLayout.addWidget(self.groupBox, 0, 2, 1, 1)

        self.groupBox_4 = QGroupBox(self.centralwidget)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.verticalLayout_4 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.csvButton = QPushButton(self.groupBox_4)
        self.csvButton.setObjectName(u"csvButton")
        self.csvButton.setMinimumSize(QSize(175, 0))

        self.verticalLayout_4.addWidget(self.csvButton)

        self.csvDownsampledButton = QPushButton(self.groupBox_4)
        self.csvDownsampledButton.setObjectName(u"csvDownsampledButton")
        self.csvDownsampledButton.setMinimumSize(QSize(175, 0))

        self.verticalLayout_4.addWidget(self.csvDownsampledButton)

        self.verticalSpacer_4 = QSpacerItem(20, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_4)


        self.gridLayout.addWidget(self.groupBox_4, 1, 0, 1, 1)

        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.spectrogramButton = QPushButton(self.groupBox_2)
        self.spectrogramButton.setObjectName(u"spectrogramButton")
        self.spectrogramButton.setMinimumSize(QSize(175, 0))

        self.verticalLayout_2.addWidget(self.spectrogramButton)

        self.verticalSpacer_2 = QSpacerItem(20, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)


        self.gridLayout.addWidget(self.groupBox_2, 0, 1, 1, 1)

        self.groupBox_3 = QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.timeButton = QPushButton(self.groupBox_3)
        self.timeButton.setObjectName(u"timeButton")
        self.timeButton.setMinimumSize(QSize(175, 0))

        self.verticalLayout_3.addWidget(self.timeButton)

        self.synchronousTimeButton = QPushButton(self.groupBox_3)
        self.synchronousTimeButton.setObjectName(u"synchronousTimeButton")
        self.synchronousTimeButton.setMinimumSize(QSize(175, 0))

        self.verticalLayout_3.addWidget(self.synchronousTimeButton)

        self.overlaidTimeButton = QPushButton(self.groupBox_3)
        self.overlaidTimeButton.setObjectName(u"overlaidTimeButton")
        self.overlaidTimeButton.setMinimumSize(QSize(175, 0))

        self.verticalLayout_3.addWidget(self.overlaidTimeButton)

        self.verticalSpacer_3 = QSpacerItem(20, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_3)


        self.gridLayout.addWidget(self.groupBox_3, 0, 0, 1, 1)

        self.groupBox_5 = QGroupBox(self.centralwidget)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.verticalLayout_6 = QVBoxLayout(self.groupBox_5)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.fileInformationButton = QPushButton(self.groupBox_5)
        self.fileInformationButton.setObjectName(u"fileInformationButton")

        self.verticalLayout_6.addWidget(self.fileInformationButton)

        self.viewSettingsButton = QPushButton(self.groupBox_5)
        self.viewSettingsButton.setObjectName(u"viewSettingsButton")

        self.verticalLayout_6.addWidget(self.viewSettingsButton)

        self.rawExportButton = QPushButton(self.groupBox_5)
        self.rawExportButton.setObjectName(u"rawExportButton")

        self.verticalLayout_6.addWidget(self.rawExportButton)

        self.splitFileButton = QPushButton(self.groupBox_5)
        self.splitFileButton.setObjectName(u"splitFileButton")

        self.verticalLayout_6.addWidget(self.splitFileButton)

        self.verticalSpacer_6 = QSpacerItem(20, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer_6)


        self.gridLayout.addWidget(self.groupBox_5, 1, 1, 1, 1)


        self.verticalLayout_5.addLayout(self.gridLayout)

        self.verticalSpacer_5 = QSpacerItem(20, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_5)

        self.verticalLayout_5.setStretch(1, 1)
        MondoMainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MondoMainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 617, 21))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        self.menuCheckForUpdates = QMenu(self.menuHelp)
        self.menuCheckForUpdates.setObjectName(u"menuCheckForUpdates")
        self.menuSettings = QMenu(self.menubar)
        self.menuSettings.setObjectName(u"menuSettings")
        MondoMainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionExit)
        self.menuHelp.addAction(self.menuCheckForUpdates.menuAction())
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionAbout)
        self.menuHelp.addAction(self.actionAboutLibraries)
        self.menuCheckForUpdates.addAction(self.actionUpdateLatestStable)
        self.menuCheckForUpdates.addAction(self.actionUpdateCurrentBranch)
        self.menuCheckForUpdates.addAction(self.actionUpdateSpecificBranch)
        self.menuCheckForUpdates.addAction(self.actionUpdateSpecificCommit)
        self.menuSettings.addAction(self.actionPreferences)

        self.retranslateUi(MondoMainWindow)
        self.actionExit.triggered.connect(MondoMainWindow.close)

        QMetaObject.connectSlotsByName(MondoMainWindow)
    # setupUi

    def retranslateUi(self, MondoMainWindow):
        MondoMainWindow.setWindowTitle(QCoreApplication.translate("MondoMainWindow", u"Mondo", None))
        self.actionAbout.setText(QCoreApplication.translate("MondoMainWindow", u"About Mondo...", None))
#if QT_CONFIG(tooltip)
        self.actionAbout.setToolTip(QCoreApplication.translate("MondoMainWindow", u"About Mondo...", None))
#endif // QT_CONFIG(tooltip)
        self.actionExit.setText(QCoreApplication.translate("MondoMainWindow", u"Exit", None))
        self.actionAboutLibraries.setText(QCoreApplication.translate("MondoMainWindow", u"About Libraries...", None))
#if QT_CONFIG(tooltip)
        self.actionAboutLibraries.setToolTip(QCoreApplication.translate("MondoMainWindow", u"About Libraries...", None))
#endif // QT_CONFIG(tooltip)
        self.actionUpdateLatestStable.setText(QCoreApplication.translate("MondoMainWindow", u"Latest Stable", None))
        self.actionUpdateSpecificBranch.setText(QCoreApplication.translate("MondoMainWindow", u"Specific Branch...", None))
        self.actionUpdateSpecificCommit.setText(QCoreApplication.translate("MondoMainWindow", u"Specific Commit..", None))
        self.actionUpdateCurrentBranch.setText(QCoreApplication.translate("MondoMainWindow", u"Latest branch", None))
        self.actionPreferences.setText(QCoreApplication.translate("MondoMainWindow", u"Preferences...", None))
#if QT_CONFIG(tooltip)
        self.actionPreferences.setToolTip(QCoreApplication.translate("MondoMainWindow", u"Preferences...", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox.setTitle(QCoreApplication.translate("MondoMainWindow", u"Frequency Analysis", None))
        self.psdButton.setText(QCoreApplication.translate("MondoMainWindow", u"Power Spectral Density (PSD)", None))
#if QT_CONFIG(tooltip)
        self.singleChannelPsdButton.setToolTip(QCoreApplication.translate("MondoMainWindow", u"Overlaid PSD streamlined for plotting a single channel across multiple time slices", None))
#endif // QT_CONFIG(tooltip)
        self.singleChannelPsdButton.setText(QCoreApplication.translate("MondoMainWindow", u"Single Channel Overlaid PSD", None))
#if QT_CONFIG(tooltip)
        self.singleSlicePsdButton.setToolTip(QCoreApplication.translate("MondoMainWindow", u"Overlaid PSD streamlined for plotting multiple channels in a single time slice", None))
#endif // QT_CONFIG(tooltip)
        self.singleSlicePsdButton.setText(QCoreApplication.translate("MondoMainWindow", u"Single Time Slice Overlaid PSD", None))
#if QT_CONFIG(tooltip)
        self.overlaidPsdButton.setToolTip(QCoreApplication.translate("MondoMainWindow", u"Ovelaid PSD for plotting arbitrary channels and time slices ", None))
#endif // QT_CONFIG(tooltip)
        self.overlaidPsdButton.setText(QCoreApplication.translate("MondoMainWindow", u"Overlaid PSD", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MondoMainWindow", u"Raw Data", None))
        self.csvButton.setText(QCoreApplication.translate("MondoMainWindow", u"CSV Output", None))
        self.csvDownsampledButton.setText(QCoreApplication.translate("MondoMainWindow", u"CSV Downsampled Output", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MondoMainWindow", u"Time/Frequency Analysis", None))
        self.spectrogramButton.setText(QCoreApplication.translate("MondoMainWindow", u"Spectrogram", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MondoMainWindow", u"Time Analysis", None))
        self.timeButton.setText(QCoreApplication.translate("MondoMainWindow", u"Time Data", None))
        self.synchronousTimeButton.setText(QCoreApplication.translate("MondoMainWindow", u"Synchronous Time Data", None))
        self.overlaidTimeButton.setText(QCoreApplication.translate("MondoMainWindow", u"Overlaid Time Data", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("MondoMainWindow", u"File Manipulation", None))
        self.fileInformationButton.setText(QCoreApplication.translate("MondoMainWindow", u"Device Information", None))
        self.viewSettingsButton.setText(QCoreApplication.translate("MondoMainWindow", u"View Device Settings", None))
        self.rawExportButton.setText(QCoreApplication.translate("MondoMainWindow", u"Advanced Raw Export", None))
        self.splitFileButton.setText(QCoreApplication.translate("MondoMainWindow", u"Split File", None))
        self.menuFile.setTitle(QCoreApplication.translate("MondoMainWindow", u"File", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MondoMainWindow", u"Help", None))
        self.menuCheckForUpdates.setTitle(QCoreApplication.translate("MondoMainWindow", u"Check for Updates", None))
        self.menuSettings.setTitle(QCoreApplication.translate("MondoMainWindow", u"Settings", None))
    # retranslateUi

