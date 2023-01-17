import sys
from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *


class Page2(QWizardPage):
    def __init__(self):
        super(Page2, self).__init__()
        self.setTitle("class Page2(QWizardPage):")
        self.setSubTitle("`setSubTitle` - class Page2(QWizardPage): ")


class Page3(QWizardPage):
    def __init__(self):
        super(Page3, self).__init__()

        self.setTitle("class Page3(QWizardPage):")
        self.setSubTitle("`setSubTitle` - class Page3(QWizardPage): ")


class AccountPage(QWizardPage):
    def __init__(self, parent=None):
        super(AccountPage, self).__init__(parent)

        self.setTitle("Account Information")
        self.setSubTitle("`setSubTitle` - ...")

        self.enterLabel    = QLabel("&LineEdit:")
        self.enter_token_box = QLineEdit()
        self.enterLabel.setBuddy(self.enter_token_box)
        #self.enter_token_box.setFocus()
        #self.setFocusProxy(self.enter_token_box)
        self.enter_token_box.setFocus()
        self.setFocusPolicy(Qt.StrongFocus)

        self.btnLabel = QLabel("&PushButton:")
        self.btn = QPushButton('OK')
        self.btnLabel.setBuddy(self.btn)
        #self.btn.setDefault(False)

        self.btn.clicked.connect(self._EnterToken)
        self.enter_token_box.returnPressed.connect(self._EnterToken)

        # Если имя заканчивается звездочкой (*), поле является обязательным.
        # Когда страница имеет обязательные поля, кнопки Next и / или Finish
        # активируются только при заполнении всех обязательных полей.
        self.registerField('Name*', self.enter_token_box)


        layout = QGridLayout(self)
        layout.addWidget(self.enterLabel,     0, 0)
        layout.addWidget(self.enter_token_box,  0, 1)
        layout.addWidget(self.btnLabel,    1, 0)
        layout.addWidget(self.btn, 1, 1)

    def setMB(self):
        print('\ndef setMB(self):', self)

    def _EnterToken(self):
        print('\ndef setMB(self):', self)
        print("self.sender()-->`{}`".format(self.sender().text()))


class Window(QWizard):
    def __init__(self):
        super(Window, self).__init__()

        self.accoutPage = AccountPage()
        self.secondPage = Page2()
        self.thirdPage  = Page3()
        self.addPage(self.accoutPage)
        self.addPage(self.secondPage)
        self.addPage(self.thirdPage)

        self.button(QWizard.NextButton).clicked.connect(self.accoutPage.setMB)
        self.buttons = [self.button(t) for t in (QWizard.NextButton, QWizard.FinishButton)]

        for btn in self.buttons:
            btn.installEventFilter(self)

    def eventFilter(self, obj, event):
        if obj in self.buttons and event.type() == QEvent.Show:
            obj.setDefault(False)
        return super(Window, self).eventFilter(obj, event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.setWizardStyle(1)
    window.show()
    sys.exit(app.exec_())