from PyQt5 import QtWidgets, QtGui, QtCore
import PyQt5
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QLabel, QScrollArea, QDialog, QGridLayout, QLineEdit, QHBoxLayout, QVBoxLayout, QWidget, QStackedWidget, QSizePolicy, QSpacerItem, QStyledItemDelegate, QStyle
from PyQt5.QtCore import Qt, QSize  
import requests
from api import get_image_url
import icons_rc
from PyQt5.QtGui import QPixmap, QIcon, QPainter, QColor
import sys
from functools import partial
from db_consulta import get_database_connection
import datetime
import locale
import random


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
        sql = "SELECT idCot, token, SUM(precio_final) as precio_total, nombre FROM cotizaciones GROUP BY token;"
        cursor.execute(sql)
        self.coti = cursor.fetchall()
        print(self.coti)
        con.close()
        
        self.initUI()

    def update_data(self):
        print("Actualizando datos en HomePage")
        con = get_database_connection()
        cursor = con.cursor()
        sql = "SELECT idCot, token, SUM(precio_final) as precio_total, nombre FROM cotizaciones GROUP BY token;"
        cursor.execute(sql)
        self.coti = cursor.fetchall()
        con.close()
        print("Datos actualizados en HomePage:", self.coti)
        self.recreate_cards()

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
            card_info = self.create_card(index, data[3], "icons/coin.png", data[2], data[1])
            self.card_widgets.append(card_info)
            
        
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

    def create_card(self, index, name, image_path, price, token):
        locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')
        image_label = QLabel()
        pixmap = QPixmap(image_path)
        pixmap = pixmap.scaledToWidth(300)
        image_label.setPixmap(pixmap)

        name_label = QLabel(name)
        formatted_price = locale.format_string("%d", price, grouping=True)
        price_label = QLabel(f"${formatted_price}")  # Muestra el precio formateado
        price_label.setStyleSheet("color: #db5e5e; font: 8pt \"Verdana\";font-weight: 900;")

        # Crear botones de borrar, ver y editar con iconos
        ver_icon = QIcon("icons/edit2.png")

        # Obtener imágenes de los iconos y redimensionarlas al tamaño deseado
        ver_image = ver_icon.pixmap(80, 80)

        ver_button = QPushButton()
        ver_button.setIcon(QIcon(ver_image))

        # Establecer tamaños fijos para los botones
        button_size = QSize(60, 60)
        button_style = """
            QPushButton {
                border-style: outset;
                border-radius: 0px;
                color: #db5e5e;
            }
            QPushButton:hover {
                background-color: #E6E6E6;
                border-style: inset;
                color: #fff;
            }
        """
        ver_button.setStyleSheet(button_style)

        ver_button.setFixedSize(button_size)

        ver_button.setCursor(Qt.PointingHandCursor)

        # Conectar los botones a las funciones correspondientes
        ver_button.clicked.connect(lambda: self.redirect_to_page(token))

        button_layout = QHBoxLayout()
        button_layout.addWidget(ver_button)
        button_layout.setAlignment(Qt.AlignCenter)

        card_layout = QVBoxLayout()
        card_layout.addWidget(image_label, alignment=Qt.AlignCenter)
        card_layout.addWidget(name_label, alignment=Qt.AlignCenter)
        card_layout.addWidget(price_label, alignment=Qt.AlignCenter)  # Agregar el precio
        card_layout.addLayout(button_layout)


        card_widget = QPushButton()
        card_widget.setFixedSize(320, 300)
        card_widget.setStyleSheet(
            "QPushButton {"
            "    background-color: white;"
            "    border-radius: 10px;"
            "}"
        )
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

    def redirect_to_page(self, token):  # Reemplaza esto con la función para obtener los datos de la carta
        card_info_dialog = CardInfoDialog(token)
        card_info_dialog.exec_()  # Muestra la ventana emergente con la información de la carta


    def recreate_cards(self):
        # Elimina las cartas existentes
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Crea las cartas nuevamente con los datos actualizados
        for index, data in enumerate(self.coti):
            card_info = self.create_card(index, data[3], "icons/coin.png", data[2], data[1])
            self.card_widgets.append(card_info)
            card_info["widget"].clicked.connect(partial(self.redirect_to_page, data[0]))

class CotizacionesPage(QWidget):
    def __init__(self):
        super().__init__()
        self.cot = []
        con = get_database_connection()
        cursor = con.cursor()
        sql = "SELECT idCot, token, SUM(precio_final) as precio_total, nombre FROM cotizaciones GROUP BY token;"  # Reemplaza 'token' con el nombre real de tu columna de token
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
            card_info = self.create_card(index, data[3], "icons/coin.png", data[2], data[1])
            self.card_widgets.append(card_info)


        self.setLayout(self.layout)

        self.search_input.textChanged.connect(self.filter_cards)

    def create_card(self, index, name, image_path, price, id):
        locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')
        image_label = QLabel()
        pixmap = QPixmap(image_path)
        pixmap = pixmap.scaledToWidth(300)
        image_label.setPixmap(pixmap)

        name_label = QLabel(name)
        name_label.setStyleSheet("color: #db5e5e; font: 10pt \"Verdana\"; font-weight: 900;")
        formatted_price = locale.format_string("%d", price, grouping=True)
        price_label = QLabel(f"${formatted_price}")  # Muestra el precio formateado
        price_label.setStyleSheet("color: #db5e5e; font: 8pt \"Verdana\";font-weight: 900;")

        # Crear botones de borrar, ver y editar con iconos
        delete_icon = QIcon("icons/delete.png")
        edit_icon = QIcon("icons/ver.png")

        # Obtener imágenes de los iconos y redimensionarlas al tamaño deseado
        delete_image = delete_icon.pixmap(80, 80)
        edit_image = edit_icon.pixmap(60, 60)

        delete_button = QPushButton()
        delete_button.setIcon(QIcon(delete_image))
        edit_button = QPushButton()
        edit_button.setIcon(QIcon(edit_image))

        # Establecer tamaños fijos para los botones
        button_size = QSize(60, 60)
        button_style = """
            QPushButton {
                border-style: outset;
                border-radius: 0px;
                color: #db5e5e;
            }
            QPushButton:hover {
                background-color: #E6E6E6;
                border-style: inset;
                color: #fff;
            }
        """
        delete_button.setStyleSheet(button_style)
        edit_button.setStyleSheet(button_style)

        delete_button.setFixedSize(button_size)
        edit_button.setFixedSize(button_size)

        delete_button.setCursor(Qt.PointingHandCursor)
        edit_button.setCursor(Qt.PointingHandCursor)

        # Conectar los botones a las funciones correspondientes
        delete_button.clicked.connect(lambda: self.delete_card(id))
        edit_button.clicked.connect(lambda: self.show_formulario(id))

        button_layout = QHBoxLayout()
        button_layout.addWidget(delete_button)
        button_layout.addWidget(edit_button)
        button_layout.setAlignment(Qt.AlignCenter)

        card_layout = QVBoxLayout()
        card_layout.addWidget(image_label, alignment=Qt.AlignCenter)
        card_layout.addWidget(name_label, alignment=Qt.AlignCenter)
        card_layout.addWidget(price_label, alignment=Qt.AlignCenter)  # Agregar el precio
        card_layout.addLayout(button_layout)


        card_widget = QPushButton()
        card_widget.setFixedSize(320, 300)
        card_widget.setStyleSheet(
            "QPushButton {"
            "    background-color: white;"
            "    border-radius: 10px;"
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

    def delete_card(self, index):
        print(f"Eliminar tarjeta {str(index)}")
        con = get_database_connection()
        cursor = con.cursor()

        # Utiliza una consulta DELETE para eliminar el registro específico en función del índice
        sql = f"DELETE FROM cotizaciones WHERE token = {index};"
        
        try:
            cursor.execute(sql)
            con.commit()
            print(f"Tarjeta {str(index)} eliminada con éxito.")
        except Exception as e:
            con.rollback()
            print(f"Error al eliminar tarjeta {str(index)}:", str(e))
        finally:
            con.close()

        self.update_elements()


    def show_formulario(self):
        if self.formulario is None:
            self.formulario = FormularioCot(self)
        #self.formulario.show()
        self.formulario.exec_()
        self.formulario.update_data()  # Mostrar el formulari

    def update_elements(self):
        # Lógica para actualizar la lista de elementos (self.cot) aquí
        con = get_database_connection()
        cursor = con.cursor()
        sql = "SELECT idCot, token, SUM(precio_final) as precio_total, nombre FROM cotizaciones GROUP BY token;"
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
            card_info = self.create_card(index, data[3], "icons/coin.png", data[2], data[1])
            self.card_widgets.append(card_info)

        # Verifica si hay cartas presentes o no
        if not self.card_widgets:
            # Crear un contenedor vertical para el mensaje
            message_container = QVBoxLayout()

            # Crear un icono (ajusta la ruta del archivo a tu icono)
            icon_label = QLabel()
            pixmap = QPixmap("icons/cot.png")
            # Redimensionar la imagen a un ancho y alto específicos (en este caso, 90x90)
            resized_pixmap = pixmap.scaled(160, 160, Qt.KeepAspectRatio)
            icon_label.setPixmap(resized_pixmap)
            icon_label.setAlignment(Qt.AlignCenter)

            # Crear el mensaje de texto
            self.message_label = QLabel("Para agregar una refaccion preciona el icono + que esta arriva a la izquierda.")
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

            # Limpiar cualquier contenido anterior y agregar el widget del mensaje al widget contenedor del QScrollArea
            for i in reversed(range(self.cards_container.layout().count())):
                widget = self.cards_container.layout().itemAt(i).widget()
                if widget:
                    widget.deleteLater()
            self.cards_container.setLayout(QVBoxLayout())
            self.cards_container.layout().addWidget(message_widget)

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
            card_info = self.create_card(index, data[1], data[3], data[0], data[2])
            self.card_widgets.append(card_info)

        if not self.card_widgets:
            print("gooooool")
            
            # Crear un contenedor vertical para el mensaje
            message_container = QVBoxLayout()
            
            # Crear un icono (ajusta la ruta del archivo a tu icono)
            icon_label = QLabel()
            pixmap = QPixmap("icons/cot.png")
            # Redimensionar la imagen a un ancho y alto específicos (en este caso, 90x90)
            resized_pixmap = pixmap.scaled(160, 160, Qt.KeepAspectRatio)
            icon_label.setPixmap(resized_pixmap)
            icon_label.setAlignment(Qt.AlignCenter)

            
            # Crear el mensaje de texto
            self.message_label = QLabel("Para agregar una refaccion preciona el icono + que esta arriva a la izquierda.")
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

    def create_card(self, index, name, image_url, id, price):
        locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')
        image_label = QLabel()

        try:
            response = requests.get(image_url)
            if response.status_code == 200:
                image_data = response.content
                original_image = QPixmap()
                original_image.loadFromData(image_data)

                # Redimensionar la imagen al tamaño deseado (por ejemplo, 300x300)
                resized_image = original_image.scaled(300, 300, Qt.KeepAspectRatio)

                image_label.setPixmap(resized_image)
            else:
                image_label.setText("Imagen no disponible")
        except Exception as e:
            image_label.setText("Error al cargar la imagen")

        name_label = QLabel(name)
        name_label.setStyleSheet("color: #db5e5e; font: 10pt \"Verdana\"; font-weight: 900;")
        formatted_price = locale.format_string("%d", price, grouping=True)
        price_label = QLabel(f"${formatted_price}")  # Muestra el precio formateado
        price_label.setStyleSheet("color: #db5e5e; font: 8pt \"Verdana\";font-weight: 900;")

        # Crear botones de borrar, ver y editar con iconos
        delete_icon = QIcon("icons/delete.png")
        edit_icon = QIcon("icons/ver.png")

        # Obtener imágenes de los iconos y redimensionarlas al tamaño deseado
        delete_image = delete_icon.pixmap(80, 80)
        edit_image = edit_icon.pixmap(60, 60)

        delete_button = QPushButton()
        delete_button.setIcon(QIcon(delete_image))
        edit_button = QPushButton()
        edit_button.setIcon(QIcon(edit_image))

        # Establecer tamaños fijos para los botones
        button_size = QSize(60, 60)
        button_style = """
            QPushButton {
                border-style: outset;
                border-radius: 0px;
                color: #db5e5e;
            }
            QPushButton:hover {
                background-color: #E6E6E6;
                border-style: inset;
                color: #fff;
            }
        """
        delete_button.setStyleSheet(button_style)
        edit_button.setStyleSheet(button_style)

        delete_button.setFixedSize(button_size)
        edit_button.setFixedSize(button_size)

        delete_button.setCursor(Qt.PointingHandCursor)
        edit_button.setCursor(Qt.PointingHandCursor)

        # Conectar los botones a las funciones correspondientes
        delete_button.clicked.connect(lambda: self.delete_card(id))
        edit_button.clicked.connect(lambda: self.show_formulario(id))

        button_layout = QHBoxLayout()
        button_layout.addWidget(delete_button)
        button_layout.addWidget(edit_button)
        button_layout.setAlignment(Qt.AlignCenter)

        card_layout = QVBoxLayout()
        card_layout.addWidget(image_label, alignment=Qt.AlignCenter)
        card_layout.addWidget(name_label, alignment=Qt.AlignCenter)
        card_layout.addWidget(price_label, alignment=Qt.AlignCenter)  # Agregar el precio
        card_layout.addLayout(button_layout)

        card_widget = QPushButton()
        card_widget.setFixedSize(320, 350)
        card_widget.setStyleSheet(
            "QPushButton {"
            "    background-color: white;"
            "    border-radius: 10px;"
            "}"
        )
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
    
    def delete_card(self, index):
        print(f"Eliminar tarjeta {str(index)}")
        con = get_database_connection()
        cursor = con.cursor()

        # Utiliza una consulta DELETE para eliminar el registro específico en función del índice
        sql = f"DELETE FROM precios WHERE idPrecio = {index};"
        
        try:
            cursor.execute(sql)
            con.commit()
            print(f"Tarjeta {str(index)} eliminada con éxito.")
        except Exception as e:
            con.rollback()
            print(f"Error al eliminar tarjeta {str(index)}:", str(e))
        finally:
            con.close()

        self.update_elements()

    

    def show_formulario(self, index=''):
        # Cerrar la instancia anterior antes de abrir una nueva
        if self.formulario:
            self.formulario.close()
        self.formulario = Formulario(self, index)
        self.formulario.exec_()


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
            card_info = self.create_card(index, data[1], data[3], data[0], data[2])
            self.card_widgets.append(card_info)

        # Verifica si hay cartas presentes o no
        if not self.card_widgets:
            # Crear un contenedor vertical para el mensaje
            message_container = QVBoxLayout()

            # Crear un icono (ajusta la ruta del archivo a tu icono)
            icon_label = QLabel()
            pixmap = QPixmap("icons/cot.png")
            # Redimensionar la imagen a un ancho y alto específicos (en este caso, 90x90)
            resized_pixmap = pixmap.scaled(160, 160, Qt.KeepAspectRatio)
            icon_label.setPixmap(resized_pixmap)
            icon_label.setAlignment(Qt.AlignCenter)

            # Crear el mensaje de texto
            self.message_label = QLabel("Para agregar una refaccion preciona el icono + que esta arriva a la izquierda.")
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

            # Limpiar cualquier contenido anterior y agregar el widget del mensaje al widget contenedor del QScrollArea
            for i in reversed(range(self.cards_container.layout().count())):
                widget = self.cards_container.layout().itemAt(i).widget()
                if widget:
                    widget.deleteLater()
            self.cards_container.setLayout(QVBoxLayout())
            self.cards_container.layout().addWidget(message_widget)

class Formulario(QtWidgets.QDialog):
    def __init__(self, precios_page, index=''):
        super().__init__()
        self.precios_page = precios_page
        self.index = index
        print(f"self.index: {self.index}")
        self.initUI()

    def initUI(self):
        """Setup the login form.
        """
        self.resize(480, 340)
        # remove the title bar
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self.setStyleSheet(
            """
            border: 2px solid #db5e5e; /* Borde */
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
                border: none;
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

        self.pushButton_3.clicked.connect(lambda: self.close())
        self.pushButton_3.clicked.connect(lambda: self.reset())


        self.verticalLayout_2.addWidget(self.pushButton_3, 0, QtCore.Qt.AlignRight)

        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setContentsMargins(-1, 15, -1, -1)

        spacer_top = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacer_top)

        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setContentsMargins(50, 30, 59, -1)

        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setStyleSheet("color: #db5e5e;\n"
                                   "font: 15pt \"Verdana\"; border: none;")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_2)

        self.lineEdit = QtWidgets.QLineEdit(self.widget)
        self.lineEdit.setMinimumSize(QtCore.QSize(0, 40))
        self.lineEdit.setStyleSheet("QLineEdit {\n"
                                    "color: #db5e5e;\n"
                                    "font: 15pt \"Verdana\";\n"
                                    "border: none;\n"
                                    "border-bottom-color: #db5e5e;\n"
                                    "border-radius: 10px;\n"
                                    "padding: 0 8px;\n"
                                    "background: #fff;\n"
                                    "selection-background-color: darkgray;\n"
                                    "}")
        self.lineEdit.setFocus(True)
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit)

        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setStyleSheet("border: none;")
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
        self.error_label.setStyleSheet("color: red; font: 12pt \"Verdana\"; border: none;")
        self.formLayout_2.setWidget(6, QtWidgets.QFormLayout.SpanningRole, self.error_label)
        
        if self.index:
           self.load_data()

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

        self.pushButton.clicked.connect(self.added)

    def load_data(self):
        if self.index:
            con = get_database_connection()
            cursor = con.cursor()
            sql = f"SELECT nombre, precio FROM precios WHERE idPrecio = {self.index};"
            cursor.execute(sql)
            data = cursor.fetchone()
            con.close()

            if data:  # Asegurarse de que se haya encontrado un registro en la base de datos
                nombre, precio = data
                self.lineEdit.setText(nombre)
                self.lineEdit_2.setText(str(precio))

    def reset(self):
        # Restablecer los campos del formulario
        self.lineEdit.setText("")
        self.lineEdit_2.setText("")
        self.error_label.setText("")
        self.index = ""  # Reiniciar el índice a un valor vacío

    def added(self):
        con = get_database_connection()
        nombre = self.lineEdit.text()
        precio = self.lineEdit_2.text()
        link = get_image_url(nombre)
        read = nombre != '' and precio != '' and link != ''

        if read:
            cursor = con.cursor()
            if self.index:  # Si hay un índice, realiza una actualización
                sql = "UPDATE precios SET nombre = %s, precio = %s, link = %s WHERE idPrecio = %s"
                data = (nombre, precio, link, self.index)
            else:  # Si no hay un índice, realiza una inserción
                sql = "INSERT INTO precios (nombre, precio, link) VALUES (%s, %s, %s)"
                data = (nombre, precio, link)
            cursor.execute(sql, data)
            con.commit()
            con.close()
            self.precios_page.update_elements()
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

class CardItemDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        # Set up the card appearance
        color = QColor(255, 255, 255)  # Background color for the card
        border_color = QColor(219, 94, 94)  # Border color
        text_color = QColor(0, 0, 0)  # Text color

        if option.state & QStyle.State_Selected:
            color = QColor(219, 94, 94)  # Change the background color for selected items
            text_color = QColor(255, 255, 255)  # Change text color for selected items

        painter.fillRect(option.rect, color)
        painter.setPen(border_color)
        painter.drawRect(option.rect)

        # Draw the item text
        item_text = index.data(Qt.DisplayRole)
        painter.setPen(text_color)
        painter.drawText(option.rect, Qt.AlignCenter, item_text)

    def sizeHint(self, option, index):
        return QSize(25, 80)  # Set the size of the card items here

class FormularioCot(QtWidgets.QDialog):
    def __init__(self, cotizaciones_page):
        super().__init__()
        self.cotizaciones_page = cotizaciones_page
        self.cot = []
        self.initUI()

    def fetch_precios_from_database(self):
        con = get_database_connection()
        cursor = con.cursor()
        sql = "SELECT * FROM precios;"
        cursor.execute(sql)
        cot = cursor.fetchall()
        con.close()
        return cot

    def update_data(self):
        # Actualiza los datos desde la base de datos
        self.cot = self.fetch_precios_from_database()
                # Limpia y actualiza la vista de la lista
        model = QtGui.QStandardItemModel()
        for option in self.cot:
            item = QtGui.QStandardItem(f"{option[1]} ${str(option[2])}")
            item.setCheckable(True)
            model.appendRow(item)
        self.list_view.setModel(model)

        # Actualiza cualquier otro elemento que necesite cambios
        self.update_total_price()
        self.list_view.selectionModel().selectionChanged.connect(self.update_total_price)

    def initUI(self):
        self.cot = self.fetch_precios_from_database()
        self.resize(580, 620)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setStyleSheet("""
            border: 2px solid #db5e5e; /* Borde */
            background: #fff;
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
        """)

        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        self.widget = QtWidgets.QWidget(self)
        self.widget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.widget.setStyleSheet(".QWidget{background-color: #fff;}")

        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(9, 2, 2, 2)

        self.pushButton_3 = QtWidgets.QPushButton(self.widget)
        self.pushButton_3.setMinimumSize(QtCore.QSize(45, 35))
        self.pushButton_3.setMaximumSize(QtCore.QSize(45, 35))
        self.pushButton_3.setStyleSheet("""
            QPushButton {
                border: none;
                border-style: outset;
                border-radius: 0px;
                padding: 6px;
                color: #000000;
                font: 13pt "Verdana";
                border-radius: 1px;
                opacity: 200;
            }
            QPushButton:hover {
                background-color: #FF0000;
                border-style: inset;
                color: #FFFFFF;
            }
            QPushButton:pressed {
                background-color: #FF0000;
                border-style: inset;
            }
        """)

        self.pushButton_3.clicked.connect(lambda: self.close())
        self.pushButton_3.clicked.connect(lambda: self.reset())

        self.verticalLayout_2.addWidget(self.pushButton_3, 0, QtCore.Qt.AlignRight)

        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setContentsMargins(-1, 15, -1, -1)
        spacer_top = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacer_top)

        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setContentsMargins(50, 30, 59, -1)

        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setStyleSheet("color: #db5e5e; font: 15pt \"Verdana\"; border: none;")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_2)

        self.lineEdit = QtWidgets.QLineEdit(self.widget)
        self.lineEdit.setMinimumSize(QtCore.QSize(0, 40))
        self.lineEdit.setStyleSheet("""
            QLineEdit {
                color: #db5e5e;
                font: 15pt "Verdana";
                border: none;
                border-bottom-color: #db5e5e;
                border-radius: 10px;
                padding: 0 8px;
                background: #fff;
                selection-background-color: darkgray;
            }
        """)
        self.lineEdit.setFocus(True)
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit)

        self.list_view = QtWidgets.QListView(self.widget)
        self.list_view.setStyleSheet("border: none")
        self.list_view.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        model = QtGui.QStandardItemModel()
        for option in self.cot:
            item = QtGui.QStandardItem(option[1].upper())
            item.setCheckable(True)
            model.appendRow(item)
        self.list_view.setModel(model)
        card_delegate = CardItemDelegate()
        self.list_view.setItemDelegate(card_delegate)
        self.formLayout_2.setWidget(8, QtWidgets.QFormLayout.SpanningRole, self.list_view)
        self.price_label = QtWidgets.QLabel(self.widget)
        self.price_label.setAlignment(QtCore.Qt.AlignRight)
        self.formLayout_2.setWidget(10, QtWidgets.QFormLayout.SpanningRole, self.price_label)
        self.update_total_price()  
        self.list_view.selectionModel().selectionChanged.connect(self.update_total_price)


        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setStyleSheet("color: #db5e5e; font: 15pt \"Verdana\"; border: none;")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_3)

        self.lineEdit_2 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_2.setMinimumSize(QtCore.QSize(0, 40))
        self.lineEdit_2.setStyleSheet("""
            QLineEdit {
                color: #db5e5e;
                font: 15pt "Verdana";
                border: None;
                border-bottom-color: #db5e5e;
                border-radius: 10px;
                padding: 0 8px;
                background: #fff;
                selection-background-color: darkgray;
            }
        """)
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.lineEdit_2)

        self.label_4 = QtWidgets.QLabel(self.widget)
        self.label_4.setStyleSheet("color: #db5e5e; font: 15pt \"Verdana\"; border: none;")
        self.formLayout_2.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.label_4)

        self.lineEdit_empresa = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_empresa.setMinimumSize(QtCore.QSize(0, 40))
        self.lineEdit_empresa.setStyleSheet("""
            QLineEdit {
                color: #db5e5e;
                font: 15pt "Verdana";
                border: none;
                border-bottom-color: #db5e5e;
                border-radius: 10px;
                padding: 0 8px;
                background: #fff;
                selection-background-color: darkgray;
            }
        """)
        self.formLayout_2.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.lineEdit_empresa)

        self.line = QtWidgets.QFrame(self.widget)
        self.line.setStyleSheet("border: 2px solid #db5e5e;")
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.SpanningRole, self.line)

        self.line_2 = QtWidgets.QFrame(self.widget)
        self.line_2.setStyleSheet("border: 2px solid #db5e5e;")
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.formLayout_2.setWidget(5, QtWidgets.QFormLayout.SpanningRole, self.line_2)

        self.line_3 = QtWidgets.QFrame(self.widget)
        self.line_3.setStyleSheet("border: 2px solid #db5e5e;")
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.formLayout_2.setWidget(7, QtWidgets.QFormLayout.SpanningRole, self.line_3)

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
                color: #db5e5e;
                font: 17pt "Verdana";
                border: 2px solid #db5e5e;
                padding: 5px;
                border-radius: 3px;
                opacity: 200;
            }
            QPushButton:hover {
                background-color: #db5e5e;
                border-style: inset;
                color: #fff;
            }
        """)

        self.pushButton.setAutoDefault(True)
        self.formLayout_2.setWidget(12, QtWidgets.QFormLayout.SpanningRole, self.pushButton)

        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout_2.setItem(11, QtWidgets.QFormLayout.SpanningRole, spacerItem)
        self.verticalLayout_3.addLayout(self.formLayout_2)

        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem1)
        self.verticalLayout_2.addLayout(self.verticalLayout_3)

        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.addWidget(self.widget)
        self.horizontalLayout_3.setStretch(0, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        spacer_bottom = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacer_bottom)

        self.error_label = QtWidgets.QLabel(self.widget)
        self.error_label.setStyleSheet("color: red; font: 12pt \"Verdana\"; border: none;")
        self.formLayout_2.setWidget(9, QtWidgets.QFormLayout.SpanningRole, self.error_label)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

        self.pushButton.clicked.connect(self.added)
    
    def reset(self):
        # Restablecer los campos del formulario
        self.lineEdit.setText("")
        self.lineEdit_2.setText("")
        self.error_label.setText("")
        self.index = ""  # Reiniciar el índice a un valor vacío

    def added(self):
        con = get_database_connection()
        nombre = self.lineEdit.text()
        cliente = self.lineEdit_2.text()
        empresa = self.lineEdit_empresa.text()
        print(empresa)
        read = nombre != '' and cliente != ''
        fecha_actual = datetime.date.today()
        token = ''.join(random.choice('0123456789') for _ in range(10))
        # Obtener los elementos seleccionados en la lista
        selected_indexes = self.list_view.selectedIndexes()
        selected_cot = [self.cot[index.row()] for index in selected_indexes]

        # Realizar alguna acción con los elementos seleccionados, si es necesario
        print(selected_cot)
        for item in selected_cot:
            print(f"Elemento seleccionado: {item[1]} - ${item[2]}")


        if read:
            for cot in selected_cot:
                cursor = con.cursor()
                sql = "INSERT INTO cotizaciones (nombre, cliente, fecha, pieza, precio_final, token) VALUES (%s, %s, %s, %s, %s, %s)"
                data = (nombre, cliente, fecha_actual, cot[1], cot[2], token)
                cursor.execute(sql, data)
                con.commit()
            con.close()
            self.cotizaciones_page.update_elements()
            self.close()
        else:
            self.error_label.setText("Llena todos los campos")

    def update_total_price(self):
        # Esta función actualiza el precio total basado en los elementos seleccionados
        total_price = 0
        selected_indexes = self.list_view.selectedIndexes()
        for index in selected_indexes:
            total_price += self.cot[index.row()][2]
        self.price_label.setText(f"Precio Total: ${total_price:.2f}")
        self.price_label.setStyleSheet("color: #db5e5e; font: 10pt \"Verdana\"; border: none;")

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "Form"))
        self.pushButton_3.setText(_translate("Form", "X"))
        self.label_2.setText(_translate("Form", "<html><head/><body><p><img src=\"icons/work.png\"/></p></body></html>"))
        self.label_3.setText(_translate("Form", "<html><head/><body><p><img src=\"icons/user.png\"/></p></body></html>"))
        self.label_4.setText(_translate("Form", "<html><head/><body><p><img src=\"icons/builds.png\"/></p></body></html>"))
        self.pushButton.setText(_translate("Form", "Agregar"))
        self.lineEdit.setPlaceholderText(_translate("Form", "Trabajo"))
        self.lineEdit_2.setPlaceholderText(_translate("Form", "Nombre del Cliente"))
        self.lineEdit_empresa.setPlaceholderText(_translate("Form", "Nombre de la Empresa"))

class CardInfoDialog(QtWidgets.QDialog):
    def __init__(self, token):
        super().__init__()
        self.token = token
        self.cot = []
        self.initUI()
    
    def cotizaciones(self):
        con = get_database_connection()
        cursor = con.cursor()
        sql = f"SELECT * FROM cotizaciones WHERE token = {self.token};"
        cursor.execute(sql)
        cot = cursor.fetchall()
        con.close()
        return cot

    
    def initUI(self):
        self.cot = self.cotizaciones()
        print(self.cot)
        self.setFixedSize(900, 700)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setStyleSheet('''
            border: 2px solid #db5e5e; /* Borde */
        ''')
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        header = QtWidgets.QWidget()
        header.setStyleSheet("background-color: #db5e5e;")
        header.setFixedSize(900, 120)

        header_layout = QtWidgets.QVBoxLayout(header)  # Cambia de QHBoxLayout a QVBoxLayout

        company_label = QtWidgets.QLabel(self.cot[0][2])
        company_label.setStyleSheet("color: rgb(231, 231, 231); font: 15pt \"Verdana\"; font-weight: 900;")

        subtitle_label = QtWidgets.QLabel(f"Cotizacion para: {self.cot[0][1]}")
        subtitle_label.setStyleSheet("color: rgb(231, 231, 231); font: 12pt \"Verdana\";")  # Establecer estilo

        close_button = QtWidgets.QPushButton("X")
        close_button.setStyleSheet("""
            QPushButton {
                border: none;
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
        close_button.clicked.connect(lambda: self.close())

        header_layout.addWidget(close_button, alignment=QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)
        header_layout.addWidget(company_label, alignment=QtCore.Qt.AlignCenter)  
        header_layout.addWidget(subtitle_label, alignment=QtCore.Qt.AlignCenter)  
        
        layout.addWidget(header)
        
        body_layout = QtWidgets.QVBoxLayout()
        body_layout.setContentsMargins(15, 15, 15, 15)

        # Aquí se crean las tres cajas de texto
        # Crear etiquetas para mostrar información
        info_labels = []  # Crear una lista para las etiquetas
        info_labelsF = []  # Crear una lista para las etiquetas

        

        for idx, cos in enumerate(self.cot):
            print(cos[5])
            label = QtWidgets.QLabel(f"{cos[6]}      ${cos[7]}")
            label.setStyleSheet("font: 10pt \"Verdana\"; border: none; color: #db5e5e;")
            label.setObjectName(f"label_{idx}")  # Establecer un nombre único para la etiqueta
            info_labels.append(label)

        for idx, cos in enumerate(self.cot):
            idx = idx + 20
            label2 = QtWidgets.QLabel(f"Fecha: {cos[4]}")
            label2.setStyleSheet("font: 10pt \"Verdana\"; border: none;")
            label2.setObjectName(f"label_{idx}")
            info_labelsF.append(label2)  
        

        # Títulos
        title_labels = []
        titles = ["Piezas", "Fecha"]

        for index, title in enumerate(titles):
            label = QtWidgets.QLabel(title)
            label.setStyleSheet("font: 12pt \"Verdana\"; font-weight: 700; border: none;")
            title_labels.append(label)
        

        # Agregar las etiquetas de títulos y de información al diseño del cuerpo
        body_layout.addWidget(title_labels[0], alignment=QtCore.Qt.AlignLeft)
        for  idx, label in enumerate(info_labels):
            body_layout.addWidget(info_labels[idx], alignment=QtCore.Qt.AlignLeft)
        body_layout.addWidget(title_labels[1], alignment=QtCore.Qt.AlignLeft)
        body_layout.addWidget(info_labelsF[0], alignment=QtCore.Qt.AlignLeft)
        totalCot = 0
        for  idx, label in enumerate(self.cot):
            totalCot = totalCot + label[7]
        labelCot = QtWidgets.QLabel(f"Total: ${str(totalCot)}")
        labelCot.setStyleSheet("font: 12pt \"Verdana\"; font-weight: 700; border: none;")
        body_layout.addWidget(labelCot, alignment=QtCore.Qt.AlignRight)


        layout.addLayout(body_layout)

    def showEvent(self, event):
        # Esta función se llama cuando la ventana se muestra
        screen_geometry = QtWidgets.QDesktopWidget().screenGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)

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
        if index == 0:  # Página de inicio
            home_page = self.page_container.widget(index)  # Obtener la instancia de HomePage
            home_page.update_data()  # Llamar a la función de actualización de datos
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



