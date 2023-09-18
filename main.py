from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QLabel, QScrollArea, QDialog, QGridLayout, QLineEdit, QHBoxLayout, QVBoxLayout, QWidget, QStackedWidget, QSizePolicy, QSpacerItem
from PyQt5.QtCore import Qt
import mysql.connector
import icons_rc
from PyQt5.QtGui import QPixmap
import sys
from db_consulta import get_database_connection

class ExitDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Confirm Exit")
        self.setFixedSize(200, 100)
        self.label = QLabel("¿Estas seguro que quieres salir?")
        self.label.setAlignment(QtCore.Qt.AlignCenter)

        self.confirm_button = QPushButton("Confirmar")
        self.cancel_button = QPushButton("Cancel")

        self.confirm_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.label)
        
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.confirm_button)
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(button_layout)

class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        # Barra de búsqueda
        self.search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_button = QPushButton("Search")

        self.search_input.setFixedWidth(250)
        self.search_input.setFixedHeight(50)
        self.search_button.setFixedWidth(100)
        self.search_button.setFixedHeight(50)
        self.search_input.setStyleSheet("QLineEdit { color: #db5e5e; font: 10pt \"Verdana\"; border: 2px solid #db5e5e; border-bottom-color: #db5e5e; border-radius: 10px; padding: 0 8px; background: rgb(231, 231, 231); selection-background-color: darkgray; }")

        self.search_layout.addWidget(self.search_input)
        self.search_layout.addWidget(self.search_button)
        self.search_layout.setAlignment(Qt.AlignRight | Qt.AlignTop)
        self.layout.addLayout(self.search_layout)

        # Crear un área de desplazamiento para las tarjetas
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet("QScrollArea { border: none; }")
        self.layout.addWidget(scroll_area)

        # Crear un widget contenedor para las tarjetas
        self.cards_container = QWidget()
        scroll_area.setWidget(self.cards_container)

        # Usar un diseño de cuadrícula para organizar las tarjetas en filas y columnas
        self.grid_layout = QGridLayout()
        self.cards_container.setLayout(self.grid_layout)

        # Crear tarjetas de ejemplo
        self.cards = []
        cars = [("uriel", "icons/search.png"), ("saenz", "icons/locks.png")]
        d = 0
        for i in cars:
            card = self.create_card(d, i[0], i[1])  # Cambia el nombre y la imagen según tus necesidades
            d += 1
            self.cards.append(card)

        self.setLayout(self.layout)

        # Conecta el evento de texto cambiado al método de filtrado
        self.search_input.textChanged.connect(self.filter_cards)

    def create_card(self, index, name, image_path):
        # Crear etiqueta para la imagen
        image_label = QLabel()
        pixmap = QPixmap(image_path)
        pixmap = pixmap.scaledToWidth(100)  # Cambiar el ancho de la imagen
        image_label.setPixmap(pixmap)

        # Crear etiqueta para el nombre
        name_label = QLabel(name)

        # Crear un diseño vertical para la tarjeta (imagen arriba, nombre abajo)
        card_layout = QVBoxLayout()
        card_layout.addWidget(image_label, alignment=Qt.AlignCenter)
        card_layout.addWidget(name_label, alignment=Qt.AlignCenter)

        # Agregar la tarjeta al diseño de la cuadrícula
        row = index // 5
        col = index % 5
        self.grid_layout.addLayout(card_layout, row, col)

        return name_label

    def filter_cards(self):
        search_text = self.search_input.text().strip().lower()
        for card in self.cards:
            card_text = card.text().lower()
            card_widget = card.parentWidget()
            if search_text in card_text:
                card_widget.setVisible(True)
            else:
                card_widget.setVisible(False)
        if not search_text:
            for card in self.cards:
                card.parentWidget().setVisible(True)



class CotizacionesPage(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.label = QLabel("Página de Cotizaciones", alignment=QtCore.Qt.AlignHCenter)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

class PreciosPage(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.label = QLabel("Página de Precios", alignment=QtCore.Qt.AlignHCenter)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

class MainSlide(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.clientes = []
        con = get_database_connection()
        cursor = con.cursor()
        sql = "SELECT * FROM cliente;"
        cursor.execute(sql)
        self.clientes = cursor.fetchone()
        con.close()
        self.mains()

    def mains(self):
        desktop = QtWidgets.QApplication.desktop()
        self.screen_geometry = desktop.screenGeometry()

        # Main window setup
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setGeometry(self.screen_geometry)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Header setup
        header = QtWidgets.QWidget()
        header.setStyleSheet("background-color: #db5e5e;")
        header.setFixedSize(self.screen_geometry.width(), 100)

        header_layout = QtWidgets.QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)

        company_label = QtWidgets.QLabel("     Ingeniería Integral y Servicios")
        company_label.setStyleSheet("color: rgb(231, 231, 231); font: 15pt \"Verdana\"; font-weight: 900;")

        # Agregar las redirecciones (botones) en una caja separada
        redirect_layout = QtWidgets.QHBoxLayout()
        redirect_layout.setContentsMargins(0, 0, 0, 0)
        redirect = ["Inicio", "Cotizaciones", "Precios"]
        for i in range(3):
            redirect_button = QtWidgets.QPushButton(redirect[i])
            redirect_button.setStyleSheet("""
                QPushButton {
                    border-style: outset;
                    border-radius: 0px;
                    padding: 6px;
                    color: white; 
                    font: 13pt "Verdana";
                    
                }
            """)
            redirect_button.setCursor(Qt.PointingHandCursor)
            redirect_button.clicked.connect(lambda _, i=i: self.change_page(i))  # Conectar el clic del botón con el cambio de página
            redirect_layout.addWidget(redirect_button, alignment=QtCore.Qt.AlignRight)

        # Botón de cierre (X) en la esquina superior derecha
        close_button = QtWidgets.QPushButton("X")
        close_button.setStyleSheet("""
            QPushButton {
                border-style: outset;
                border-radius: 0px;
                padding: 6px;
                color: white; 
                font: 13pt "Verdana";
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
        close_button.clicked.connect(self.show_exit_dialog)

        # Agregar elementos al encabezado
        header_layout.addWidget(company_label, alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        header_layout.addStretch(1)
        header_layout.addLayout(redirect_layout)
        header_layout.addWidget(close_button, alignment=QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)

        layout.addWidget(header)

        # Crear un contenedor para las páginas (bodies)
        self.page_container = QStackedWidget()
        self.page_container.addWidget(HomePage())  # Agrega la página de inicio
        self.page_container.addWidget(CotizacionesPage())  # Agrega la página de cotizaciones
        self.page_container.addWidget(PreciosPage())  # Agrega la página de precios

        # Cambiar al contenido de la página de inicio por defecto
        self.page_container.setCurrentIndex(0)

        # Agregar el contenedor de páginas al diseño del cuerpo
        body_layout = QtWidgets.QVBoxLayout()  # Diseño vertical para el área de contenido (body)
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.addWidget(self.page_container, stretch=2)

        layout.addLayout(body_layout)  # Agregar el área de contenido a la ventana principal

    def show_exit_dialog(self):
        dialog = ExitDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.close()

    # Agregar un método para cambiar la página actual
    def change_page(self, index):
        self.page_container.setCurrentIndex(index)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainSlide()
    window.show()
    sys.exit(app.exec_())
