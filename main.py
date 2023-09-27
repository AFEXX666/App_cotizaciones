from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QLabel, QScrollArea, QDialog, QGridLayout, QLineEdit, QHBoxLayout, QVBoxLayout, QWidget, QStackedWidget, QSizePolicy, QSpacerItem
from PyQt5.QtCore import Qt
import requests
from api import get_image_url
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
        self.coti = []
        self.info = []
        con = get_database_connection()
        cursor = con.cursor()
        sql = "SELECT * FROM cotizaciones;"
        cursor.execute(sql)
        self.coti = cursor.fetchall()
        print(self.coti)
        con.close()
        
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        
        self.search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_button = QPushButton()
        self.search_button.setStyleSheet("image: url(icons/search.png);")

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

        for index, data in enumerate(self.coti):
            card_info = self.create_card(index, data[1], "icons/coin.png")
            self.card_widgets.append(card_info)
            
            # Utiliza functools.partial para crear una función lambda con el valor correcto de index
            card_info["widget"].clicked.connect(partial(self.redirect_to_page, data[0]))
        
        if not self.card_widgets:
            print("gooooool")
            
            # Crear un contenedor vertical para el mensaje
            message_container = QVBoxLayout()
            
            # Crear un icono (ajusta la ruta del archivo a tu icono)
            icon_label = QLabel()
            pixmap = QPixmap("icons/coin.png")
            icon_label.setPixmap(pixmap)
            icon_label.setAlignment(Qt.AlignCenter)
            
            # Crear el mensaje de texto
            self.message_label = QLabel("Aquí aparecerán las cotizaciones cuando las agregues.")
            self.message_label.setStyleSheet("color: #db5e5e; font: 15pt \"Verdana\"; font-weight: 900;")
            self.message_label.setAlignment(Qt.AlignCenter)

            # Agregar el icono y el mensaje al contenedor vertical
            message_container.addWidget(icon_label)
            message_container.addWidget(self.message_label)

            # Establecer la alineación del contenedor vertical en el centro
            message_container.setAlignment(Qt.AlignCenter)
            
            # Crear un widget para el contenedor del mensaje
            message_widget = QWidget()
            message_widget.setLayout(message_container)

            # Agregar el widget del mensaje al widget contenedor del QScrollArea
            self.cards_container.setLayout(QVBoxLayout())  # Limpia cualquier contenido anterior
            self.cards_container.layout().addWidget(message_widget)

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
        self.coti = cursor.fetchall()
        print(self.coti)

class CotizacionesPage(QWidget):
    def __init__(self):
        super().__init__()
        self.cot = []
        con = get_database_connection()
        cursor = con.cursor()
        sql = "SELECT * FROM cotizaciones;"
        cursor.execute(sql)
        self.cot = cursor.fetchall()
        print(self.cot)
        con.close()
        self.formulario = None
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        self.search_layout = QHBoxLayout()
        
        # Botón de más a la izquierda
        self.plus_button = QPushButton("+")
        self.plus_button.setStyleSheet(
            "QPushButton { font-size: 18px; font-weight: bold; background-color: #db5e5e; color: white; border: none; border-radius: 5px; }"
            "QPushButton:hover { background-color: #c53c3c; }"
        )
        self.plus_button.setFixedSize(50, 50)
        self.plus_button.setCursor(Qt.PointingHandCursor)
        self.plus_button.clicked.connect(self.show_formulario)

        # Espaciador flexible para empujar los elementos a la derecha
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.search_input = QLineEdit()

        # Botón de búsqueda
        self.search_button = QPushButton()
        self.search_button.setStyleSheet("QPushButton { image: url(icons/search.png); }")
        self.search_button.setFixedSize(100, 50)
        self.search_button.setCursor(Qt.PointingHandCursor)

        self.search_input.setFixedHeight(50)
        self.search_input.setFixedWidth(250)
        self.search_input.setStyleSheet("QLineEdit { color: #db5e5e; font: 10pt \"Verdana\"; border: 2px solid #db5e5e; border-bottom-color: #db5e5e; border-radius: 10px; padding: 0 8px; background: rgb(231, 231, 231); selection-background-color: darkgray; }")

        self.search_layout.addWidget(self.plus_button)
        self.search_layout.addSpacerItem(spacer)  # Agregar el espaciador flexible
        self.search_layout.addWidget(self.search_input)
        self.search_layout.addWidget(self.search_button)
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

    def show_formulario(self):
        if self.formulario is None:
            self.formulario = FormularioCot(self)  # Crear una instancia del formulario si aún no existe
        self.formulario.show()  # Mostrar el formulari

class PreciosPage(QWidget):
    def __init__(self):
        super().__init__()
        self.cot = []
        con = get_database_connection()
        cursor = con.cursor()
        sql = "SELECT * FROM precios;"
        cursor.execute(sql)
        self.cot = cursor.fetchall()
        print(self.cot)
        con.close()
        self.formulario = None
        self.initUI()
        
    def initUI(self):
        self.layout = QVBoxLayout()

        self.search_layout = QHBoxLayout()
        
        # Botón de más a la izquierda
        self.plus_button = QPushButton("+")
        self.plus_button.setStyleSheet(
            "QPushButton { font-size: 18px; font-weight: bold; background-color: #db5e5e; color: white; border: none; border-radius: 5px; }"
            "QPushButton:hover { background-color: #c53c3c; }"
        )
        self.plus_button.setFixedSize(50, 50)
        self.plus_button.setCursor(Qt.PointingHandCursor)
        self.plus_button.clicked.connect(self.show_formulario)

        # Espaciador flexible para empujar los elementos a la derecha
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.search_input = QLineEdit()

        # Botón de búsqueda
        self.search_button = QPushButton()
        self.search_button.setStyleSheet("QPushButton { image: url(icons/search.png); }")
        self.search_button.setFixedSize(100, 50)
        self.search_button.setCursor(Qt.PointingHandCursor)

        self.search_input.setFixedHeight(50)
        self.search_input.setFixedWidth(250)
        self.search_input.setStyleSheet("QLineEdit { color: #db5e5e; font: 10pt \"Verdana\"; border: 2px solid #db5e5e; border-bottom-color: #db5e5e; border-radius: 10px; padding: 0 8px; background: rgb(231, 231, 231); selection-background-color: darkgray; }")

        self.search_layout.addWidget(self.plus_button)
        self.search_layout.addSpacerItem(spacer)  # Agregar el espaciador flexible
        self.search_layout.addWidget(self.search_input)
        self.search_layout.addWidget(self.search_button)
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
            card_info = self.create_card(index, data[1], data[3])
            self.card_widgets.append(card_info)

            # Utiliza functools.partial para crear una función lambda con el valor correcto de index
            card_info["widget"].clicked.connect(partial(self.redirect_to_page, data[0]))

        self.setLayout(self.layout)

        self.search_input.textChanged.connect(self.filter_cards)

    def create_card(self, index, name, image_url):
        image_label = QLabel()

        try:
            response = requests.get(image_url)
            if response.status_code == 200:
                image_data = response.content
                pixmap = QPixmap()
                pixmap.loadFromData(image_data)
                pixmap = pixmap.scaledToWidth(300)
                image_label.setPixmap(pixmap)
            else:
                image_label.setText("Imagen no disponible")
        except Exception as e:
            image_label.setText("Error al cargar la imagen")

        name_label = QLabel(name)

        # Crear botones de borrar, ver y editar
        delete_button = QPushButton("Borrar")
        view_button = QPushButton("Ver")
        edit_button = QPushButton("Editar")

        # Establecer tamaños fijos para los botones
        delete_button.setFixedWidth(80)
        view_button.setFixedWidth(80)
        edit_button.setFixedWidth(80)

        # Conecta los botones a las funciones correspondientes
        delete_button.clicked.connect(lambda: self.delete_card(index))
        view_button.clicked.connect(lambda: self.redirect_to_page(index))
        edit_button.clicked.connect(lambda: self.edit_card(index))

        button_layout = QHBoxLayout()
        button_layout.addWidget(delete_button)
        button_layout.addWidget(view_button)
        button_layout.addWidget(edit_button)
        button_layout.setAlignment(Qt.AlignCenter)

        card_layout = QVBoxLayout()
        card_layout.addWidget(image_label, alignment=Qt.AlignCenter)
        card_layout.addWidget(name_label, alignment=Qt.AlignCenter)
        card_layout.addLayout(button_layout)

        card_widget = QPushButton()
        card_widget.setFixedSize(320, 350)
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

        return {"widget": card_widget, "name": name, "image_url": image_url}
    

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
        sql = f"SELECT * FROM precios WHERE idPrecio = {index};"
        cursor.execute(sql)
        self.cot = cursor.fetchall()
        print(self.cot)
    
    def delete_card(self, index):
        print(f"Tarjeta {str(index)} fue clicada. Redirigir a la página correspondiente.")
        con = get_database_connection()
        cursor = con.cursor()
        sql = f"SELECT * FROM precios WHERE idPrecio = {index};"
        cursor.execute(sql)
        self.cot = cursor.fetchall()
        print(self.cot)
    
    def edit_card(self, index):
        print(f"Tarjeta {str(index)} fue clicada. Redirigir a la página correspondiente.")
        con = get_database_connection()
        cursor = con.cursor()
        sql = f"SELECT * FROM precios WHERE idPrecio = {index};"
        cursor.execute(sql)
        self.cot = cursor.fetchall()
        print(self.cot)

    def show_formulario(self):
        if self.formulario is None:
            self.formulario = Formulario(self)  # Crear una instancia del formulario si aún no existe
        self.formulario.show()  # Mostrar el formulari

    def update_elements(self):
        # Lógica para actualizar la lista de elementos (self.cot) aquí
        con = get_database_connection()
        cursor = con.cursor()
        sql = "SELECT * FROM precios;"
        cursor.execute(sql)
        self.cot = cursor.fetchall()
        con.close()

        # Limpia los widgets existentes
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # Crea los nuevos widgets de tarjetas con la lista actualizada
        self.card_widgets = []
        for index, data in enumerate(self.cot):
            card_info = self.create_card(index, data[1], data[3])
            self.card_widgets.append(card_info)
            card_info["widget"].clicked.connect(partial(self.redirect_to_page, data[0]))

class Formulario(QWidget):
    def __init__(self, precios_page):
        super().__init__()
        self.precios_page = precios_page
        self.initUI()

    def initUI(self):
        """Setup the login form.
        """
        self.resize(480, 340)
        # remove the title bar
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self.setStyleSheet(
            """
            QPushButton {
                border-style: outset;
                border-radius: 0px;
                padding: 6px;
                color: #db5e5e;
            }
            QPushButton:hover {
                background-color: #db5e5e;
                border-style: inset;
                color: #fff;
            }
            QPushButton:pressed {
                background-color: #db5e5e;
                border-style: inset;
            }
            """
        )

        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()

        self.widget = QtWidgets.QWidget(self)
        self.widget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.widget.setStyleSheet(".QWidget{background-color: #fff;}")

        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(9, 0, 0, 0)

        self.pushButton_3 = QtWidgets.QPushButton(self.widget)
        self.pushButton_3.setMinimumSize(QtCore.QSize(45, 35))
        self.pushButton_3.setMaximumSize(QtCore.QSize(45, 35))
        self.pushButton_3.setStyleSheet("""
            QPushButton {
                border-style: outset;
                border-radius: 0px;
                padding: 6px;
                color: #000000; /* Color de texto por defecto */
                font: 13pt "Verdana";
                border-radius: 1px;
                opacity: 200;
            }
            QPushButton:hover {
                background-color: #FF0000;
                border-style: inset;
                color: #FFFFFF; /* Cambia el color del texto en hover */
            }
            QPushButton:pressed {
                background-color: #FF0000;
                border-style: inset;
            }
        """)

        self.pushButton_3.clicked.connect(self.close)

        self.verticalLayout_2.addWidget(self.pushButton_3, 0, QtCore.Qt.AlignRight)

        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setContentsMargins(-1, 15, -1, -1)

        spacer_top = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacer_top)

        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setContentsMargins(50, 30, 59, -1)

        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setStyleSheet("color: #db5e5e;\n"
                                   "font: 15pt \"Verdana\";")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_2)

        self.lineEdit = QtWidgets.QLineEdit(self.widget)
        self.lineEdit.setMinimumSize(QtCore.QSize(0, 40))
        self.lineEdit.setStyleSheet("QLineEdit {\n"
                                    "color: #db5e5e;\n"
                                    "font: 15pt \"Verdana\";\n"
                                    "border: None;\n"
                                    "border-bottom-color: #db5e5e;\n"
                                    "border-radius: 10px;\n"
                                    "padding: 0 8px;\n"
                                    "background: #fff;\n"
                                    "selection-background-color: darkgray;\n"
                                    "}")
        self.lineEdit.setFocus(True)
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit)

        self.label_3 = QtWidgets.QLabel(self.widget)
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_3)

        self.lineEdit_2 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_2.setMinimumSize(QtCore.QSize(0, 40))
        self.lineEdit_2.setStyleSheet("QLineEdit {\n"
                                      "color: #db5e5e;\n"
                                      "font: 15pt \"Verdana\";\n"
                                      "border: None;\n"
                                      "border-bottom-color: #db5e5e;\n"
                                      "border-radius: 10px;\n"
                                      "padding: 0 8px;\n"
                                      "background: #fff;\n"
                                      "selection-background-color: darkgray;\n"
                                      "}")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.lineEdit_2)
        

        self.line = QtWidgets.QFrame(self.widget)
        self.line.setStyleSheet("border: 2px solid #db5e5e;")
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.SpanningRole, self.line)

        self.line_2 = QtWidgets.QFrame(self.widget)
        self.line_2.setStyleSheet("border: 2px solid #db5e5e;")
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
        self.pushButton.setStyleSheet("""
            QPushButton {
                color: #db5e5e; /* Color de texto por defecto */
                font: 17pt "Verdana";
                border: 2px solid #db5e5e;
                padding: 5px;
                border-radius: 3px;
                opacity: 200;
            }
            QPushButton:hover {
                background-color: #db5e5e;
                border-style: inset;
                color: #fff; /* Cambia el color del texto en hover */
            }
        """)

        self.pushButton.setAutoDefault(True)
        self.formLayout_2.setWidget(8, QtWidgets.QFormLayout.SpanningRole, self.pushButton)

        """self.pushButton_2 = QtWidgets.QPushButton(self.widget)
        self.pushButton_2.setMinimumSize(QtCore.QSize(0, 60))
        self.pushButton_2.setStyleSheet("color: rgb(231, 231, 231);\n"
                                        "font: 17pt \"Verdana\";\n"
                                        "border: 2px solid #db5e5e;\n"
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
        spacer_bottom = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacer_bottom)

        #Error de contraseña y/o incorrectas
        self.error_label = QtWidgets.QLabel(self.widget)
        self.error_label.setStyleSheet("color: red; font: 12pt \"Verdana\";")
        self.formLayout_2.setWidget(6, QtWidgets.QFormLayout.SpanningRole, self.error_label)


        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

        self.pushButton.clicked.connect(self.added)

    def added(self):
        con = get_database_connection()
        nombre = self.lineEdit.text()
        precio = self.lineEdit_2.text()
        link = get_image_url(nombre)
        read = nombre != '' and precio != '' and link != ''

        if read:
            cursor = con.cursor()
            sql = "INSERT INTO precios (nombre, precio, link) VALUES (%s, %s, %s)"
            data = (nombre, precio, link,)
            cursor.execute(sql, data)
            con.commit()
            con.close()
            self.precios_page.update_elements()  # Utiliza la instancia almacenada para actualizar la página
            self.close()
        else:
            self.error_label.setText("Llena todos los campos")

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "Form"))
        self.pushButton_3.setText(_translate("Form", "X"))
        self.label_2.setText(_translate(
            "Form",
            "<html><head/><body><p><img src=\"icons/cot.png\"/></p></body></html>"))
        self.label_3.setText(_translate(
            "Form",
            "<html><head/><body><p><img src=\"icons/dllar.png\"/></p></body></html>"))
        self.pushButton.setText(_translate("Form", "Agregar"))
        self.lineEdit.setPlaceholderText(_translate("Form", "Nombre"))
        self.lineEdit_2.setPlaceholderText(_translate("Form", "Precio"))
        #self.pushButton_2.setText(_translate("Form", "Register"))

class FormularioCot(QWidget):
    def __init__(self, precios_page):
        super().__init__()
        self.precios_page = precios_page
        self.initUI()

    def initUI(self):
        """Setup the login form.
        """
        self.resize(480, 340)
        # remove the title bar
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self.setStyleSheet(
            """
            QPushButton {
                border-style: outset;
                border-radius: 0px;
                padding: 6px;
                color: #db5e5e;
            }
            QPushButton:hover {
                background-color: #db5e5e;
                border-style: inset;
                color: #fff;
            }
            QPushButton:pressed {
                background-color: #db5e5e;
                border-style: inset;
            }
            """
        )

        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()

        self.widget = QtWidgets.QWidget(self)
        self.widget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.widget.setStyleSheet(".QWidget{background-color: #fff;}")

        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(9, 0, 0, 0)

        self.pushButton_3 = QtWidgets.QPushButton(self.widget)
        self.pushButton_3.setMinimumSize(QtCore.QSize(45, 35))
        self.pushButton_3.setMaximumSize(QtCore.QSize(45, 35))
        self.pushButton_3.setStyleSheet("""
            QPushButton {
                border-style: outset;
                border-radius: 0px;
                padding: 6px;
                color: #000000; /* Color de texto por defecto */
                font: 13pt "Verdana";
                border-radius: 1px;
                opacity: 200;
            }
            QPushButton:hover {
                background-color: #FF0000;
                border-style: inset;
                color: #FFFFFF; /* Cambia el color del texto en hover */
            }
            QPushButton:pressed {
                background-color: #FF0000;
                border-style: inset;
            }
        """)

        self.pushButton_3.clicked.connect(self.close)

        self.verticalLayout_2.addWidget(self.pushButton_3, 0, QtCore.Qt.AlignRight)

        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setContentsMargins(-1, 15, -1, -1)
        #FUCKIN LOVE 
        spacer_top = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacer_top)

        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setContentsMargins(50, 30, 59, -1)

        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setStyleSheet("color: #db5e5e;\n"
                                   "font: 15pt \"Verdana\";")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_2)

        self.lineEdit = QtWidgets.QLineEdit(self.widget)
        self.lineEdit.setMinimumSize(QtCore.QSize(0, 40))
        self.lineEdit.setStyleSheet("QLineEdit {\n"
                                    "color: #db5e5e;\n"
                                    "font: 15pt \"Verdana\";\n"
                                    "border: None;\n"
                                    "border-bottom-color: #db5e5e;\n"
                                    "border-radius: 10px;\n"
                                    "padding: 0 8px;\n"
                                    "background: #fff;\n"
                                    "selection-background-color: darkgray;\n"
                                    "}")
        self.lineEdit.setFocus(True)
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit)

        self.label_3 = QtWidgets.QLabel(self.widget)
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_3)

        self.lineEdit_2 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_2.setMinimumSize(QtCore.QSize(0, 40))
        self.lineEdit_2.setStyleSheet("QLineEdit {\n"
                                      "color: #db5e5e;\n"
                                      "font: 15pt \"Verdana\";\n"
                                      "border: None;\n"
                                      "border-bottom-color: #db5e5e;\n"
                                      "border-radius: 10px;\n"
                                      "padding: 0 8px;\n"
                                      "background: #fff;\n"
                                      "selection-background-color: darkgray;\n"
                                      "}")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.lineEdit_2)
        

        self.line = QtWidgets.QFrame(self.widget)
        self.line.setStyleSheet("border: 2px solid #db5e5e;")
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.SpanningRole, self.line)

        self.line_2 = QtWidgets.QFrame(self.widget)
        self.line_2.setStyleSheet("border: 2px solid #db5e5e;")
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
        self.pushButton.setStyleSheet("""
            QPushButton {
                color: #db5e5e; /* Color de texto por defecto */
                font: 17pt "Verdana";
                border: 2px solid #db5e5e;
                padding: 5px;
                border-radius: 3px;
                opacity: 200;
            }
            QPushButton:hover {
                background-color: #db5e5e;
                border-style: inset;
                color: #fff; /* Cambia el color del texto en hover */
            }
        """)

        self.pushButton.setAutoDefault(True)
        self.formLayout_2.setWidget(8, QtWidgets.QFormLayout.SpanningRole, self.pushButton)

        """self.pushButton_2 = QtWidgets.QPushButton(self.widget)
        self.pushButton_2.setMinimumSize(QtCore.QSize(0, 60))
        self.pushButton_2.setStyleSheet("color: rgb(231, 231, 231);\n"
                                        "font: 17pt \"Verdana\";\n"
                                        "border: 2px solid #db5e5e;\n"
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
        spacer_bottom = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacer_bottom)

        #Error de contraseña y/o incorrectas
        self.error_label = QtWidgets.QLabel(self.widget)
        self.error_label.setStyleSheet("color: red; font: 12pt \"Verdana\";")
        self.formLayout_2.setWidget(6, QtWidgets.QFormLayout.SpanningRole, self.error_label)


        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

        self.pushButton.clicked.connect(self.added)

    def added(self):
        con = get_database_connection()
        nombre = self.lineEdit.text()
        precio = self.lineEdit_2.text()
        link = get_image_url(nombre)
        read = nombre != '' and precio != '' and link != ''

        if read:
            cursor = con.cursor()
            sql = "INSERT INTO precios (nombre, precio, link) VALUES (%s, %s, %s)"
            data = (nombre, precio, link,)
            cursor.execute(sql, data)
            con.commit()
            con.close()
            self.precios_page.update_elements()  # Utiliza la instancia almacenada para actualizar la página
            self.close()
        else:
            self.error_label.setText("Llena todos los campos")

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "Form"))
        self.pushButton_3.setText(_translate("Form", "X"))
        self.label_2.setText(_translate(
            "Form",
            "<html><head/><body><p><img src=\"icons/cot.png\"/></p></body></html>"))
        self.label_3.setText(_translate(
            "Form",
            "<html><head/><body><p><img src=\"icons/dllar.png\"/></p></body></html>"))
        self.pushButton.setText(_translate("Form", "Agregar"))
        self.lineEdit.setPlaceholderText(_translate("Form", "Nombre"))
        self.lineEdit_2.setPlaceholderText(_translate("Form", "Precio"))
        #self.pushButton_2.setText(_translate("Form", "Register"))

class MainSlide(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.clientes = []
        con = get_database_connection()
        cursor = con.cursor()
        sql = "SELECT * FROM cotizaciones;"
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



