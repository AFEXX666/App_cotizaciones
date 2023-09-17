from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QLabel
import mysql.connector
import icons_rc
from db_consulta import get_database_connection

class MainSlide(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.row = []
        con = get_database_connection()
        cursor = con.cursor()
        sql = "SELECT * FROM cliente;"
        cursor.execute(sql)
        self.row = cursor.fetchone()
        con.close()
        self.mains()

    def mains(self):
        desktop = QtWidgets.QApplication.desktop()
        screen_geometry = desktop.screenGeometry()

        # Main window setup
        self.setStyleSheet(".QWidget{background-color: rgb(20, 20, 40);}")
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setGeometry(screen_geometry)
        self.setWindowTitle("Your Window Title")  # Set your window title here
        self.initUI()

    def initUI(self):
        layout = QtWidgets.QVBoxLayout(self)

        # Header setup
        header = QtWidgets.QWidget()
        header.setStyleSheet("background-color: rgba(0, 0, 0, 0.2);")

        header_layout = QtWidgets.QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)

        company_label = QtWidgets.QLabel("Ingeniería Integral y Servicios", alignment=QtCore.Qt.AlignHCenter)
        company_label.setStyleSheet("color: rgb(231, 231, 231); font: 15pt \"Verdana\";")

        close_button = QtWidgets.QPushButton("X")
        close_button.setStyleSheet("""
            QPushButton {
                border-style: outset;
                border-radius: 0px;
                padding: 6px;
                color: white; 
                font: 13pt \"Verdana\";
            }
            QPushButton:hover {
                background-color: #FF0000;
                border-style: inset;
            }
            QPushButton:pressed {
                background-color: #FF0000;
                border-style: inset;
            }
        """)
        close_button.setMinimumSize(QtCore.QSize(35, 25))
        close_button.setMaximumSize(QtCore.QSize(35, 25))
        close_button.clicked.connect(self.close)

        header_layout.addWidget(company_label, alignment=QtCore.Qt.AlignHCenter)
        header_layout.addWidget(close_button, alignment=QtCore.Qt.AlignRight)

        layout.addWidget(header)
        layout.addStretch(1)  # Add flexible space to push content downward

        # Add your content widgets here (e.g., labels, buttons, etc.)
        content_label = QtWidgets.QLabel("Your Content Goes Here", alignment=QtCore.Qt.AlignHCenter)
        content_label.setStyleSheet("color: white; font: 14pt \"Verdana\";")

        layout.addWidget(content_label, alignment=QtCore.Qt.AlignHCenter)
        layout.addStretch(2)  # Add more space at the bottom

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainSlide()
    window.show()
    sys.exit(app.exec_())
