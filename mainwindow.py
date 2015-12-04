__author__ = 'Netrix'
import PyQt5.QtWidgets as qtwidgets
import PyQt5.QtCore as qtcore
from modules.ExitModule import ExitModule
from modules.TranslatorModule import TranslatorModule
from modules.SjpModule import SjpModule

class MainWindow(qtwidgets.QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent, qtcore.Qt.WindowStaysOnTopHint)
        self.setWindowFlags(qtcore.Qt.WindowTitleHint)
        self.initUI()

        self.modules = {}
        self.modules[ExitModule.name] = ExitModule(self)
        self.modules['ap'] = TranslatorModule(self, 'en', 'pl')
        self.modules['pa'] = TranslatorModule(self, 'pl', 'en')
        self.modules['np'] = TranslatorModule(self, 'de', 'pl')
        self.modules['pn'] = TranslatorModule(self, 'pl', 'de')
        self.modules[SjpModule.name] = SjpModule(self)

        self.__currentModule = None

    def initUI(self):
        # self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('NAssist')

        self.mainTextBox = qtwidgets.QLineEdit()
        self.mainTextBox.textChanged.connect(self.__handleTextChanged)

        verticalLayout = qtwidgets.QVBoxLayout()
        verticalLayout.addWidget(self.mainTextBox)

        self.setLayout(verticalLayout)
        self.__result = None
        self.__mainLayout = verticalLayout

    def addWidget(self, widget):
        self.__mainLayout.addWidget(widget)

    def __handleTextChanged(self, text):
        if not self.hasFocus():
            self.__handleTextChangedOnNoFocus(text)

    def __handleTextChangedOnNoFocus(self, text):
        tmp = text.split(' ')
        command = tmp[0]
        rest = ' '.join(tmp[1:])

        if command in self.modules:
            self.__handleValidCommand(self.modules[command], rest)
        else:
            self.__handleInvalidCommand()


    def __handleValidCommand(self, module, text):
        if module == self.__currentModule:
            self.__currentModule.onTextUpdate(text)
        else:
            self.__handleCommandChanged(module)


    def __handleInvalidCommand(self):
        if self.__currentModule:
            self.__currentModule.onDeactivate()
            self.__currentModule = None
            self.adjustWindowSizeAndPosition()

    def __handleCommandChanged(self, module):
        if self.__currentModule:
            self.__currentModule.onDeactivate()
            self.adjustWindowSizeAndPosition()

        self.__currentModule = module
        module.onActivate()
        self.adjustWindowSizeAndPosition()

    def keyPressEvent(self, event):
        if event.key() == qtcore.Qt.Key_Escape:
            self.hide()
        elif event.key() in (qtcore.Qt.Key_Enter, qtcore.Qt.Key_Return) and qtwidgets.QApplication.keyboardModifiers() == qtcore.Qt.ShiftModifier:
            self.mainTextBox.setText("")
        elif self.__currentModule:
            self.__currentModule.onKeyPress(event)

    def adjustWindowSizeAndPosition(self):
        self.adjustSize()
        self.move(qtwidgets.QApplication.desktop().screen().rect().center() - self.rect().center())

    def show(self):
        super(MainWindow, self).show()
        self.mainTextBox.setFocus()
        self.adjustWindowSizeAndPosition()

    def close(self):
        for a, m in self.modules.items():
            m.onClose()
        super(MainWindow, self).close()

