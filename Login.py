""" Import """
from PyQt5 import QtCore, QtGui, QtWidgets
from Image import Image as Image_rc
import sys


""" Object """
class Ui_MainWindow():
    def __init__(self, MainWindow):
        ##############################          Variable          ##############################
        self.Type = 0
        self.Data = ["2020", "mdmahikaishar.me@gmail.com", "6244", ""]
        self.Trans = QtCore.QCoreApplication.translate
        ##############################          Window          ##############################
        self.MainWindow = MainWindow
        self.MainWindow.setObjectName("MainWindow")
        self.MainWindow.resize(800, 500)
        self.MainWindow.setWindowTitle(self.Trans("MainWindow", "Login"))
        self.centralwidget = QtWidgets.QWidget(self.MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.MainWindow.setCentralWidget(self.centralwidget)
        ### Background
        self.Bg = QtWidgets.QLabel(self.centralwidget)
        self.Bg.setGeometry(QtCore.QRect(0, 0, 800, 500))
        self.Bg.setPixmap(QtGui.QPixmap(":/Image/Back.jpg"))
        self.Bg.setScaledContents(True)
        self.Bg.setObjectName("Bg")
        ### User
        self.User = QtWidgets.QLabel(self.centralwidget)
        self.User.setGeometry(QtCore.QRect(345, 130, 110, 110))
        self.User.setPixmap(QtGui.QPixmap(":/Image/User.png"))
        self.User.setScaledContents(True)
        self.User.setObjectName("User")
        ### Copyright
        self.Copyright = QtWidgets.QLabel(self.centralwidget)
        self.Copyright.setGeometry(QtCore.QRect(725, 482, 68, 10))
        self.Copyright.setObjectName("Copyright")
        self.Copyright.setText(self.Trans("MainWindow", "©Uriel Saenz"))
        ### Call
        self.FLogin()        


    ### Login InterFace
    def FLogin(self):
        ### Password
        self.Password = QtWidgets.QLineEdit(self.centralwidget)
        self.Password.setGeometry(QtCore.QRect(300, 250, 200, 20))
        self.Password.setMaxLength(10)
        self.Password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.Password.setObjectName("Password")
        self.Password.setPlaceholderText(self.Trans("MainWindow", " Password"))
        self.Password.setStyleSheet("border-radius: 10px;\n"
                                    "font: 14px\"Arial\";")
        ### Forget
        self.ForgetPassword = QtWidgets.QPushButton(self.centralwidget)
        self.ForgetPassword.setGeometry(QtCore.QRect(310, 272, 70, 10))
        self.ForgetPassword.setObjectName("Forget")
        self.ForgetPassword.clicked.connect(self.FForgetPassword)
        self.ForgetPassword.setStyleSheet("QPushButton#Forget{\n"
                                  "    background-image: url(:/Image/Forget.png);\n"
                                  "    border: none;\n""}\n"
                                  "QPushButton#Forget:focus:pressed{    \n"
                                  "    background-image: url(:/Image/ForgetC.png);\n"
                                  "    border: none;\n""}\n"
                                  "QPushButton#Forget:hover{\n"
                                  "    background-image: url(:/Image/ForgetH.png);\n"
                                  "    border: none;\n"
                                  "}")
        ### Submit
        self.FSubmit(lambda: self.FLoginSubmit(str(self.Password.text())))
        ### Show
        self.Password.show()
        self.ForgetPassword.show()
        self.Submit.show()
        ### Connect
        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)
        

    ### Forget Password Step1 Email
    def FForgetPassword(self):
        ### Checking Step
        if self.Type == 0:
            self.FFEmail()
            self.Type = 1
        elif self.Type == 1:
            self.FFSecurityPin()
            self.Type = 2
        elif self.Type == 2:
            self.FFNewPassword()
            self.Type = 3
        else:
            self.FFRePassword()
            self.Type = 0
        ### Connect
        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)


    ### Forget Password Step1 Email
    def FFEmail(self):
        ### Hide
        self.Password.hide()
        self.Submit.hide()
        self.ForgetPassword.hide()
        ### Email
        self.Email = QtWidgets.QLineEdit(self.centralwidget)
        self.Email.setGeometry(QtCore.QRect(300, 250, 200, 20))
        self.Email.setMaxLength(40)
        self.Email.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.Email.setObjectName("Email")
        self.Email.setPlaceholderText(self.Trans("MainWindow", " Email"))
        self.Email.setStyleSheet("border-radius: 10px;\n"
                                 "font: 14px\"Arial\";")
        ### Submit and Step
        self.FSubmit(lambda: self.FFEmailSubmit(str(self.Email.text())))
        self.FStep(1)
        ### Show
        self.Email.show()
        self.Submit.show()
        self.Step.show()
        ### Connect
        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)
        

    ### Forget Password Step2 SecurityPin
    def FFSecurityPin(self):
        ### Hide
        self.Email.hide()
        self.Submit.hide()
        self.Step.hide()
        ### Security Pin
        self.SecurityPin = QtWidgets.QLineEdit(self.centralwidget)
        self.SecurityPin.setGeometry(QtCore.QRect(300, 250, 200, 20))
        self.SecurityPin.setMaxLength(10)
        self.SecurityPin.setEchoMode(QtWidgets.QLineEdit.Password)
        self.SecurityPin.setObjectName("SecurityPin")
        self.SecurityPin.setPlaceholderText(self.Trans("MainWindow", " Security Pin"))
        self.SecurityPin.setStyleSheet("border-radius: 10px;\n"
                                       "font: 14px\"Arial\";")
        ### Submit and Step
        self.FSubmit(lambda: self.FFSecurityPinSubmit(str(self.SecurityPin.text())))
        self.FStep(2)
        ### Show
        self.SecurityPin.show()
        self.Submit.show()  
        self.Step.show()      
        ### Connect
        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)


    ### Forget Password Step3 NewPassword
    def FFNewPassword(self):
        ### Hide
        self.SecurityPin.hide()
        self.Submit.hide()
        self.Step.hide()
        ### New Password
        self.NewPassword = QtWidgets.QLineEdit(self.centralwidget)
        self.NewPassword.setGeometry(QtCore.QRect(300, 250, 200, 20))
        self.NewPassword.setMaxLength(10)
        self.NewPassword.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.NewPassword.setObjectName("NewPassword")
        self.NewPassword.setPlaceholderText(self.Trans("MainWindow", " New Password"))
        self.NewPassword.setStyleSheet("border-radius: 10px;\n"
                                    "font: 14px\"Arial\";")
        ### Submit and Step
        self.FSubmit(lambda: self.FFNewPasswordSubmit(str(self.NewPassword.text())))
        self.FStep(3)
        ### Show
        self.NewPassword.show()
        self.Submit.show()
        self.Step.show()
        ### Connect
        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)

    
    ### Forget Password Step3 RePassword
    def FFRePassword(self):
        ### Hide
        self.NewPassword.hide()
        self.Submit.hide()
        self.Step.hide()
        ### Re Password
        self.RePassword = QtWidgets.QLineEdit(self.centralwidget)
        self.RePassword.setGeometry(QtCore.QRect(300, 250, 200, 20))
        self.RePassword.setMaxLength(10)
        self.RePassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.RePassword.setObjectName("RePassword")
        self.RePassword.setPlaceholderText(self.Trans("MainWindow", " Re Password"))
        self.RePassword.setStyleSheet("border-radius: 10px;\n"
                                    "font: 14px\"Arial\";")
        ### Submit and Step
        self.FSubmit(lambda: self.FFRePasswordSubmit(str(self.RePassword.text())))
        self.FStep(4)
        ### Show
        self.RePassword.show()
        self.Submit.show()
        self.Step.show()
        ### Connect
        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)


    def FSubmit(self, With):
        self.Submit = QtWidgets.QPushButton(self.centralwidget)
        self.Submit.setGeometry(QtCore.QRect(480, 250, 20, 20))
        self.Submit.setObjectName("Submit")
        self.Submit.setShortcut("Return")
        self.Submit.clicked.connect(With)
        self.Submit.setStyleSheet("QPushButton#Submit{\n"
                                  "    background-image: url(:/Image/Submit.png);\n"
                                  "    border: none;\n""}\n"
                                  "QPushButton#Submit:focus:pressed{\n"
                                  "    background-image: url(:/Image/SubmitC.png);\n"
                                  "    border: none;\n""}\n"
                                  "QPushButton#Submit:hover{\n"
                                  "    background-image: url(:/Image/SubmitH.png);\n"
                                  "    border: none;\n"
                                  "}")
        ### Connect
        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)


    def FStep(self, i):
        self.Step = QtWidgets.QLabel(self.centralwidget)
        self.Step.setGeometry(QtCore.QRect(445, 272, 45, 13))
        self.Step.setObjectName("Step")
        self.Step.setText(self.Trans("MainWindow", "Step "+str(i)+"/4"))


    def FLoginSubmit(self, Password):
        if Password == self.Data[0]:
            self.MainWindow.close()
    

    def FFEmailSubmit(self, Email):
        if Email == self.Data[1]:
            self.FForgetPassword()


    def FFSecurityPinSubmit(self, SecurityPin):
        if SecurityPin == self.Data[2]:
            self.FForgetPassword()


    def FFNewPasswordSubmit(self, NewPassword):
        self.Data[3] = NewPassword
        self.FForgetPassword()


    def FFRePasswordSubmit(self, RePassword):
        if RePassword == self.Data[3]:
            self.Data[0] = RePassword
            self.Data[3] = ""
            self.RePassword.hide()
            self.Submit.hide()
            self.Step.hide()
            self.FLogin()


if __name__ == "__main__":
    App = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    Ui = Ui_MainWindow(MainWindow)
    MainWindow.show()
    sys.exit(App.exec_())