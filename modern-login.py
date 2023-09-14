# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtWidgets

import icons_rc  # pylint: disable=unused-import
from customized import PasswordEdit
from main import MainSlide



# TODO: Improve readability


class LoginForm(QtWidgets.QWidget):
    """Basic login form.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Data = {"user": "2134", "email": "uriel@gmail.com", "password": "6244", "slide_index": 1}
        self.setup_ui()

    def setup_ui(self):
        """Setup the login form.
        """
        self.resize(480, 600)
        # remove the title bar
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self.setStyleSheet(
            """
            QPushButton {
                border-style: outset;
                border-radius: 0px;
                padding: 6px;
            }
            QPushButton:hover {
                background-color: #FF0000;
                border-style: inset;
            }
            QPushButton:pressed {
                background-color: #FF0000;
                border-style: inset;
            }
            """
        )

        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()

        self.widget = QtWidgets.QWidget(self)
        self.widget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.widget.setStyleSheet(".QWidget{background-color: rgb(20, 20, 40);}")

        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(9, 0, 0, 0)

        self.pushButton_3 = QtWidgets.QPushButton(self.widget)
        self.pushButton_3.setMinimumSize(QtCore.QSize(35, 25))
        self.pushButton_3.setMaximumSize(QtCore.QSize(35, 25))
        self.pushButton_3.setStyleSheet("color: white;\n"
                                        "font: 13pt \"Verdana\";\n"
                                        "border-radius: 1px;\n"
                                        "opacity: 200;\n")
        self.pushButton_3.clicked.connect(self.close)
        self.verticalLayout_2.addWidget(self.pushButton_3, 0, QtCore.Qt.AlignRight)

        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setContentsMargins(-1, 15, -1, -1)

        #Label del icono de perfil
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setMinimumSize(QtCore.QSize(150, 150))
        self.label.setMaximumSize(QtCore.QSize(150, 150))
        self.label.setStyleSheet("image: url(icons/perfil_32x32.png);")
        self.verticalLayout_3.addWidget(self.label, 0, QtCore.Qt.AlignHCenter)
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setMinimumSize(QtCore.QSize(50, 50))
        self.label.setMaximumSize(QtCore.QSize(50, 50))

        #Label del nombre de la compañia
        self.company = QtWidgets.QLabel(self)
        self.company_2 = QtWidgets.QLabel(self) # Aumenta la altura máxima para que el texto pueda acomodarse abajo
        self.company.setText("Ingeniería Integral")
        self.company.setStyleSheet("color: rgb(231, 231, 231); font: 15pt \"Verdana\"; text-align: center;")
        self.company_2.setText("y Servicios")
        self.company_2.setStyleSheet("color: rgb(231, 231, 231); font: 15pt \"Verdana\"; text-align: center;")
        self.verticalLayout_3.addWidget(self.company, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout_3.addWidget(self.company_2, 0, QtCore.Qt.AlignHCenter)

        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setContentsMargins(50, 30, 59, -1)

        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setStyleSheet("color: rgb(231, 231, 231);\n"
                                   "font: 15pt \"Verdana\";")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_2)

        self.lineEdit = QtWidgets.QLineEdit(self.widget)
        self.lineEdit.setMinimumSize(QtCore.QSize(0, 40))
        self.lineEdit.setStyleSheet("QLineEdit {\n"
                                    "color: rgb(231, 231, 231);\n"
                                    "font: 15pt \"Verdana\";\n"
                                    "border: None;\n"
                                    "border-bottom-color: white;\n"
                                    "border-radius: 10px;\n"
                                    "padding: 0 8px;\n"
                                    "background: rgb(20, 20, 40);\n"
                                    "selection-background-color: darkgray;\n"
                                    "}")
        self.lineEdit.setFocus(True)
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit)

        self.label_3 = QtWidgets.QLabel(self.widget)
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_3)

        self.lineEdit_2 = PasswordEdit(self.widget)
        self.lineEdit_2.setMinimumSize(QtCore.QSize(0, 40))
        self.lineEdit_2.setStyleSheet("QLineEdit {\n"
                                      "color: orange;\n"
                                      "font: 15pt \"Verdana\";\n"
                                      "border: None;\n"
                                      "border-bottom-color: white;\n"
                                      "border-radius: 10px;\n"
                                      "padding: 0 8px;\n"
                                      "background: rgb(20, 20, 40);\n"
                                      "selection-background-color: darkgray;\n"
                                      "}")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.lineEdit_2)
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)

        self.line = QtWidgets.QFrame(self.widget)
        self.line.setStyleSheet("border: 2px solid white;")
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.SpanningRole, self.line)

        self.line_2 = QtWidgets.QFrame(self.widget)
        self.line_2.setStyleSheet("border: 2px solid orange;")
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.formLayout_2.setWidget(5, QtWidgets.QFormLayout.SpanningRole, self.line_2)

        self.pushButton = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())

        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setMinimumSize(QtCore.QSize(0, 60))
        self.pushButton.setAutoFillBackground(False)
        self.pushButton.setStyleSheet("color: rgb(231, 231, 231);\n"
                                      "font: 17pt \"Verdana\";\n"
                                      "border: 2px solid orange;\n"
                                      "padding: 5px;\n"
                                      "border-radius: 3px;\n"
                                      "opacity: 200;\n"
                                      "")
        self.pushButton.setAutoDefault(True)
        self.formLayout_2.setWidget(8, QtWidgets.QFormLayout.SpanningRole, self.pushButton)

        """self.pushButton_2 = QtWidgets.QPushButton(self.widget)
        self.pushButton_2.setMinimumSize(QtCore.QSize(0, 60))
        self.pushButton_2.setStyleSheet("color: rgb(231, 231, 231);\n"
                                        "font: 17pt \"Verdana\";\n"
                                        "border: 2px solid orange;\n"
                                        "padding: 5px;\n"
                                        "border-radius: 3px;\n"
                                        "opacity: 200;\n"
                                        "")
        self.pushButton_2.setDefault(False)
        self.pushButton_2.setFlat(False)
        self.formLayout_2.setWidget(8, QtWidgets.QFormLayout.SpanningRole, self.pushButton_2)
        """

        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout_2.setItem(7, QtWidgets.QFormLayout.SpanningRole, spacerItem)
        self.verticalLayout_3.addLayout(self.formLayout_2)

        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem1)
        self.verticalLayout_2.addLayout(self.verticalLayout_3)

        self.horizontalLayout_3.addWidget(self.widget)
        self.horizontalLayout_3.setStretch(0, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        #Error de contraseña y/o incorrectas
        self.error_label = QtWidgets.QLabel(self.widget)
        self.error_label.setStyleSheet("color: red; font: 12pt \"Verdana\";")
        self.formLayout_2.setWidget(6, QtWidgets.QFormLayout.SpanningRole, self.error_label)


        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

        self.pushButton.clicked.connect(self.login)

    def login(self):
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        read = username != '' and password != ''
        answer = username == self.Data["user"] and password == self.Data["password"]

        if read:
            if answer:
                self.main_slide = MainSlide()
                self.main_slide.show()
                self.close()
            else:
                self.error_label.setText("Usuario y/o contraseña incorrectos")
        else:
            self.error_label.setText("Rellena todos los campos")



    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "Form"))
        self.pushButton_3.setText(_translate("Form", "X"))
        self.label_2.setText(_translate(
            "Form",
            "<html><head/><body><p><img src=\":/icons/icons/user_32x32.png\"/></p></body></html>"))
        self.label_3.setText(_translate(
            "Form",
            "<html><head/><body><p><img src=\":/icons/icons/lock_or_32x32.png\"/></p></body></html>"))
        self.pushButton.setText(_translate("Form", "Entrar"))
        self.lineEdit.setPlaceholderText(_translate("Form", "Usuario"))
        self.lineEdit_2.setPlaceholderText(_translate("Form", "Contraseña"))
        #self.pushButton_2.setText(_translate("Form", "Register"))



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    login_form = LoginForm()
    login_form.show()

    sys.exit(app.exec_())
