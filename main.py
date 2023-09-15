from PyQt5 import QtWidgets, QtGui, QtCore
import icons_rc

class MainSlide(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.piezas = [("motor", 2000), ("llantas", 1000)]
        self.mains()

    def mains(self):
        desktop = QtWidgets.QApplication.desktop()
        screen_geometry = desktop.screenGeometry()
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

        self.widget = QtWidgets.QWidget(self)
        self.widget.setStyleSheet(".QWidget{background-color: rgb(20, 20, 40);}")

        self.gridLayout = QtWidgets.QGridLayout(self.widget)

        self.pushButton_3 = QtWidgets.QPushButton("X", self)
        self.pushButton_3.setMinimumSize(QtCore.QSize(35, 25))
        self.pushButton_3.setMaximumSize(QtCore.QSize(35, 25))
        self.pushButton_3.setStyleSheet("color: white;\n"
                                        "font: 13pt \"Verdana\";\n"
                                        "border-radius: 1px;\n"
                                        "opacity: 200;\n")
        self.pushButton_3.clicked.connect(self.close)

        # Agregar el botón "X" en la esquina superior derecha
        self.gridLayout.addWidget(self.pushButton_3, 0, 1, QtCore.Qt.AlignTop | QtCore.Qt.AlignRight)

        self.verticalLayout.addWidget(self.widget)

        # Establecer el tamaño de la ventana para que ocupe toda la pantalla
        self.setGeometry(screen_geometry)

        for p in self.piezas:
            print(p[1])

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainSlide()
    window.show()
    sys.exit(app.exec_())
