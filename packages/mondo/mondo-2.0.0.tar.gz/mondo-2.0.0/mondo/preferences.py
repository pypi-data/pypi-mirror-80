from PySide2 import QtCore, QtGui, QtWidgets

from hyperborea.preferences import read_bool_setting, write_bool_setting

from .ui_preferences import Ui_PreferencesDialog


original_palette = None


def set_style(app, dark_mode=True):
    app.setStyle("Fusion")

    global original_palette
    if original_palette is None:
        original_palette = app.palette()

    # Now use a palette to switch to dark colors:
    if dark_mode:
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor(53, 53, 53))
        palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette.Base, QtGui.QColor(25, 25, 25))
        palette.setColor(QtGui.QPalette.AlternateBase,
                         QtGui.QColor(53, 53, 53))
        palette.setColor(QtGui.QPalette.ToolTipBase, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette.Text, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette.Button, QtGui.QColor(53, 53, 53))
        palette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)
        palette.setColor(QtGui.QPalette.Link, QtGui.QColor(42, 130, 218))
        palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(42, 130, 218))
        palette.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.black)

        palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText,
                         QtCore.Qt.darkGray)
        palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Text,
                         QtCore.Qt.darkGray)
        palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText,
                         QtCore.Qt.darkGray)
        palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Light,
                         QtCore.Qt.black)

        app.setPalette(palette)
    else:
        app.setPalette(original_palette)


class PreferencesDialog(QtWidgets.QDialog, Ui_PreferencesDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.settings = QtCore.QSettings()

        self.setupUi(self)

        # this is easily forgotten in Qt Designer
        self.tabWidget.setCurrentIndex(0)

        self.accepted.connect(self.write_settings)
        self.darkMode.toggled.connect(self.dark_mode_updated)
        self.lightMode.toggled.connect(self.dark_mode_updated)

        self.read_settings()

    def dark_mode_updated(self, junk=None):
        dark_mode = self.darkMode.isChecked()
        set_style(QtWidgets.QApplication.instance(), dark_mode)

    def read_settings(self):
        self.unitPreferences.read_settings()

        dark_mode = read_bool_setting(self.settings, "DarkMode", True)
        if dark_mode:
            self.darkMode.setChecked(True)
        else:
            self.lightMode.setChecked(True)

    def write_settings(self):
        self.unitPreferences.write_settings()

        dark_mode = self.darkMode.isChecked()
        write_bool_setting(self.settings, "DarkMode", dark_mode)
