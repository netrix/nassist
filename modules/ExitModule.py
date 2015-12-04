__author__ = 'Netrix'
import PyQt5.QtWidgets as qtwidgets
import PyQt5.QtCore as qtcore
from modules.BaseModule import BaseModule


class ExitModule(BaseModule):
    name = "exit"

    def __init__(self, parent):
        super(ExitModule, self).__init__(parent)
        self.__result = qtwidgets.QTextEdit()
        self.__exitText = "Aby wyjść z aplikacji naciśnij Enter"

    def onKeyPress(self, event):
        if event.key() in (qtcore.Qt.Key_Enter, qtcore.Qt.Key_Return):
            self.parent.close()

    def onTextUpdate(self, text):
        self.__result.setText(self.__exitText + "\n\n" + text)

    def onActivate(self):
        self.parent.addWidget(self.__result)
        self.__result.setText(self.__exitText)

    def onDeactivate(self):
        self.__result.setParent(None)
