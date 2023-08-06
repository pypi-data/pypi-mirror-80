import math
import os
import sys

from PySide2 import QtWidgets, QtGui, QtCore

import xappt

from xappt_qt.gui.ui.browser import Ui_Browser
from xappt_qt.dark_palette import apply_palette
from xappt_qt.constants import *

# noinspection PyUnresolvedReferences
from xappt_qt.gui.resources import icons


class TreeItemDelegate(QtWidgets.QItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._hint_height = None

    def sizeHint(self, option, index):
        hint = super().sizeHint(option, index)
        if self._hint_height is None:
            self._hint_height = int(math.ceil(hint.height() * 1.5))
        hint.setHeight(self._hint_height)
        return hint


class XapptBrowser(QtWidgets.QMainWindow, Ui_Browser):
    ROLE_TOOL_CLASS = QtCore.Qt.UserRole + 1

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(":appicon"))
        self.populate_tools()
        self.treeTools.setItemDelegate(TreeItemDelegate())
        self.treeTools.itemActivated.connect(self.item_activated)
        self.interfaces = []

    def populate_tools(self):
        for tool_name, tool_class in xappt.registered_tools():
            item = QtWidgets.QTreeWidgetItem()
            item.setText(0, tool_name)
            item.setData(0, self.ROLE_TOOL_CLASS, tool_class)
            self.treeTools.addTopLevelItem(item)
        self.treeTools.sortItems(0, QtCore.Qt.AscendingOrder)

    def item_activated(self, item: QtWidgets.QTreeWidgetItem, column: int):
        tool_class = item.data(0, self.ROLE_TOOL_CLASS)
        interface = xappt.get_interface()
        self.interfaces.append(interface)
        interface.invoke(tool_class())

    def closeEvent(self, event: QtGui.QCloseEvent):
        self.interfaces.clear()


def main(args) -> int:
    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication(args)
    apply_palette(app)

    browser = XapptBrowser()
    browser.show()

    app.setProperty(APP_PROPERTY_RUNNING, True)
    return app.exec_()


def entry_point() -> int:
    os.environ[xappt.INTERFACE_ENV] = APP_INTERFACE_NAME
    return main(sys.argv)


if __name__ == '__main__':
    sys.exit(entry_point())
