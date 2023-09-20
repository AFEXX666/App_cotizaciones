from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QLabel, QScrollArea, QDialog, QGridLayout, QLineEdit, QHBoxLayout, QVBoxLayout, QWidget, QStackedWidget, QSizePolicy, QSpacerItem
from PyQt5.QtCore import Qt
import mysql.connector
import icons_rc
from PyQt5.QtGui import QPixmap
import sys
from functools import partial
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
        self.cot = []
        self.info = []
        con = get_database_connection()
        cursor = con.cursor()
        sql = "SELECT * FROM cotizaciones;"
        cursor.execute(sql)
        self.cot = cursor.fetchall()
        print(self.cot)
        con.close()
        
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        
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

        self.grid_layout = QGridLayout()
        self.cards_container.setLayout(self.grid_layout)

        self.card_widgets = []

        for index, data in enumerate(self.cot):
            card_info = self.create_card(index, data[1], "icons/coin.png")
            self.card_widgets.append(card_info)
            
            # Utiliza functools.partial para crear una función lambda con el valor correcto de index
            card_info["widget"].clicked.connect(partial(self.redirect_to_page, data[0]))


        self.setLayout(self.layout)
        
        self.search_input.textChanged.connect(self.filter_cards)

    def create_card(self, index, name, image_path):
        image_label = QLabel()
        pixmap = QPixmap(image_path)
        pixmap = pixmap.scaledToWidth(300)
        image_label.setPixmap(pixmap)

        name_label = QLabel(name)

        card_layout = QVBoxLayout()
        card_layout.addWidget(image_label, alignment=Qt.AlignCenter)
        card_layout.addWidget(name_label, alignment=Qt.AlignCenter)

        card_widget = QPushButton()
        card_widget.setFixedSize(320, 300)
        card_widget.setStyleSheet(
            "QPushButton {"
            "    background-color: white;"
            "    border-radius: 10px;"
            "    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.5);"
            "}"
        )
        card_widget.setCursor(Qt.PointingHandCursor)
        card_widget.setLayout(card_layout)

        row = index // 5
        col = index % 5
        self.grid_layout.addWidget(card_widget, row, col)

        return {"widget": card_widget, "name": name, "image_path": image_path}

    def filter_cards(self):
        search_text = self.search_input.text().strip().lower()
        for card_info in self.card_widgets:
            card_widget = card_info["widget"]
            card_text = card_info["name"].lower()
            if search_text in card_text:
                card_widget.setVisible(True)
            else:
                card_widget.setVisible(False)
        if not search_text:
            for card_info in self.card_widgets:
                card_widget = card_info["widget"]
                card_widget.setVisible(True)

    def redirect_to_page(self, index):
        print(f"Tarjeta {str(index)} fue clicada. Redirigir a la página correspondiente.")
        con = get_database_connection()
        cursor = con.cursor()
        sql = f"SELECT * FROM cotizaciones WHERE idCot = {index};"
        cursor.execute(sql)
        self.cot = cursor.fetchall()
        print(self.cot)




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

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setGeometry(self.screen_geometry)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        header = QtWidgets.QWidget()
        header.setStyleSheet("background-color: #db5e5e;")
        header.setFixedSize(self.screen_geometry.width(), 100)

        header_layout = QtWidgets.QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)

        company_label = QtWidgets.QLabel("     Ingeniería Integral y Servicios")
        company_label.setStyleSheet("color: rgb(231, 231, 231); font: 15pt \"Verdana\"; font-weight: 900;")

        redirect_layout = QtWidgets.QHBoxLayout()
        redirect_layout.setContentsMargins(0, 0, 0, 0)
        redirect = ["Inicio", "Cotizaciones", "Precios"]
        
        # Lista de botones de redirección
        self.redirect_buttons = []

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
            redirect_button.setCursor(QtCore.Qt.PointingHandCursor)
            redirect_button.clicked.connect(lambda _, i=i: self.change_page(i))
            redirect_layout.addWidget(redirect_button, alignment=QtCore.Qt.AlignRight)

            # Agregar el botón a la lista
            self.redirect_buttons.append(redirect_button)

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

        header_layout.addWidget(company_label, alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        header_layout.addStretch(1)
        header_layout.addLayout(redirect_layout)
        header_layout.addWidget(close_button, alignment=QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)

        layout.addWidget(header)

        self.page_container = QStackedWidget()
        self.page_container.addWidget(HomePage())
        self.page_container.addWidget(CotizacionesPage())
        self.page_container.addWidget(PreciosPage())

        self.page_container.setCurrentIndex(0)

        body_layout = QtWidgets.QVBoxLayout()
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.addWidget(self.page_container, stretch=2)

        layout.addLayout(body_layout)

        # Establecer el estilo inicial de los botones
        self.update_redirect_buttons(0)

    def show_exit_dialog(self):
        dialog = ExitDialog(self)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.close()

    def change_page(self, index):
        self.page_container.setCurrentIndex(index)
        self.update_redirect_buttons(index)

    def update_redirect_buttons(self, current_index):
        for i, button in enumerate(self.redirect_buttons):
            if i == current_index:
                button.setStyleSheet("""
                    QPushButton {
                        border-style: outset;
                        border-radius: 0px;
                        padding: 6px;
                        color: hsl(0, 0%, 65%);; 
                        font: 13pt "Verdana";
                    }
                """)
            else:
                button.setStyleSheet("""
                    QPushButton {
                        border-style: outset;
                        border-radius: 0px;
                        padding: 6px;
                        color: white; 
                        font: 13pt "Verdana";
                    }
                """)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainSlide()
    window.show()
    sys.exit(app.exec_())
