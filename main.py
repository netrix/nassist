#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Netrix'

import sys
import PyQt5.QtWidgets as qtwidgets
import PyQt5.QtGui as qtgui
import PyQt5.QtCore as qtcore
import PyQt5.QtNetwork as qtnetwork
import mainwindow
import hotkeythread

#NOTE: http://sourceforge.net/projects/pywin32/files/pywin32/Build%20219/
# +hotkey
# threading - module


class SystemTrayApplication(qtwidgets.QSystemTrayIcon):
    def __init__(self, parent=None):
        super(SystemTrayApplication, self).__init__(parent)
        self.setIcon(qtgui.QIcon("icon.png"))
        self.window = parent

        exitAction = qtwidgets.QAction("&Exit", self)
        exitAction.triggered.connect(parent.close)

        rightClickMenu = qtwidgets.QMenu()
        rightClickMenu.addAction(exitAction)

        self.setContextMenu(rightClickMenu)
        self.show()

        self.hkthread = hotkeythread.HotkeyThread()
        self.hkthread.hotkeySignal.connect(self.hotkeyPressed)
        self.hkthread.start()

    def __del__(self):
        self.hide()

    @qtcore.pyqtSlot()
    def hotkeyPressed(self):
        self.window.show()
        self.window.activateWindow()


if __name__ == "__main__":
    app = qtwidgets.QApplication(sys.argv)
    
    # proxy = qtnetwork.QNetworkProxy()
    # proxy.setType(qtnetwork.QNetworkProxy.HttpProxy)
    # proxy.setHostName("you_proxy_address")
    # proxy.setPort(8080)
    # qtnetwork.QNetworkProxy.setApplicationProxy(proxy)

    window = mainwindow.MainWindow()
    tray = SystemTrayApplication(window)

    window.show()

    sys.exit(app.exec_())
