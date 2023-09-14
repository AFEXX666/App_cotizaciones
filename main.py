from PyQt5 import QtWidgets, QtGui

class MainSlide(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mains()

    def mains(self):
        desktop = QtWidgets.QApplication.desktop()
        screen_geometry = desktop.screenGeometry()
        
        self.setGeometry(screen_geometry)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainSlide()
    window.show()
    sys.exit(app.exec_())
