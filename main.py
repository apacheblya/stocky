import sys
import os
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, \
    QLabel, QListWidget, QMenuBar, QMenu, QFileDialog, QDialog
from PyQt5.QtGui import QIcon  # Импортируем QIcon для установки иконки

version = 0.1

class Shop:
    def __init__(self):
        self.products = []  # Список товаров

    def load_from_json(self, filename):
        """Загружает товары из файла JSON."""
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                self.products = json.load(f)
            return True
        return False

    def save_to_json(self, filename):
        """Сохраняет товары в файл JSON."""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.products, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            print(f"Ошибка при сохранении в JSON: {e}")
            return False

    def add_product(self, name, price, quantity):
        """Добавляет новый товар в список и сохраняет в JSON."""
        if any(product['name'] == name for product in self.products):
            return f"Ошибка: Товар {name} уже существует."
        else:
            self.products.append({'name': name, 'price': price, 'quantity': quantity})
            return f"Товар {name} с ценой {price}грн. и количеством {quantity}шт. добавлен."

    def delete_product(self, name):
        """Удаляет товар из списка и сохраняет изменения в JSON."""
        self.products = [product for product in self.products if product['name'] != name]
        return f"Товар {name} был успешно удален."

    def read_products(self):
        """Возвращает список всех товаров."""
        return self.products

class HelpDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Помощь")

        # Создание вертикального layout для размещения лейблов
        layout = QVBoxLayout()

        # Добавление лейблов с информацией
        layout.addWidget(QLabel("Dev: apache1337"))
        layout.addWidget(QLabel("TG: @vl8dysl8v"))
        layout.addWidget(QLabel("DS: @.apache1337"))
        layout.addWidget(QLabel(f"Версия: {version}"))

        # Устанавливаем layout для диалогового окна
        self.setLayout(layout)
        self.resize(200, 100)


class ShopApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Stocky")
        self.setGeometry(100, 100, 400, 600)
        self.setWindowIcon(QIcon('icon.ico'))

        # Инициализация Shop
        self.shop = Shop()
        self.db_name = None  # Хранит название файла JSON

        self.init_ui()

    def init_ui(self):
        # Создание меню
        menubar = self.menuBar()

        file_menu = menubar.addMenu("Файл")
        open_action = file_menu.addAction("Открыть файл")
        open_action.triggered.connect(self.open_json_file)

        help_menu = menubar.addMenu("Помощь")
        self.setWindowIcon(QIcon('icon.ico'))
        help_action = help_menu.addAction("Контактные данные")
        help_action.triggered.connect(self.show_help_dialog)

        # Main Layout
        main_layout = QVBoxLayout()

        # Ввод имени файла
        db_name_layout = QHBoxLayout()
        self.db_name_entry = QLineEdit(self)
        self.db_name_entry.setPlaceholderText("Введите имя файла JSON")
        db_name_layout.addWidget(self.db_name_entry)

        # Добавление кнопки "Создать"
        self.create_db_button = QPushButton("Создать файл JSON", self)
        self.create_db_button.clicked.connect(self.create_json_file)
        db_name_layout.addWidget(self.create_db_button)

        # Name Input Layout
        product_layout = QHBoxLayout()
        self.add_product_entry = QLineEdit(self)
        self.add_product_entry.setPlaceholderText("Введите название товара")
        product_layout.addWidget(self.add_product_entry)

        # Price Input Layout
        price_layout = QHBoxLayout()
        self.add_price_entry = QLineEdit(self)
        self.add_price_entry.setPlaceholderText("Введите цену товара")
        price_layout.addWidget(self.add_price_entry)

        # Quantity Input Layout
        quantity_layout = QHBoxLayout()
        self.add_quantity_entry = QLineEdit(self)
        self.add_quantity_entry.setPlaceholderText("Введите количество товара")
        quantity_layout.addWidget(self.add_quantity_entry)

        # Buttons
        self.add_button = QPushButton("Добавить товар", self)
        self.delete_button = QPushButton("Удалить товар", self)
        self.save_button = QPushButton("Сохранить список", self)

        # Connecting buttons to functions
        self.add_button.clicked.connect(self.on_add_product)
        self.delete_button.clicked.connect(self.on_delete_product)
        self.save_button.clicked.connect(self.on_save_products)

        # Product List Layout with Scroll Area
        self.product_list_widget = QListWidget(self)
        self.product_list_widget.setMinimumHeight(200)

        # Info Label
        self.add_info_label = QLabel("INFO", self)

        # Add layouts to the main layout
        main_layout.addLayout(db_name_layout)  # Добавляем поле ввода имени файла
        main_layout.addLayout(product_layout)
        main_layout.addLayout(price_layout)
        main_layout.addLayout(quantity_layout)
        main_layout.addWidget(self.add_button)
        main_layout.addWidget(self.delete_button)
        main_layout.addWidget(self.save_button)
        main_layout.addWidget(self.product_list_widget)
        main_layout.addWidget(self.add_info_label)

        # Set central widget
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def create_json_file(self):
        """Создает новый файл JSON."""
        file_name = self.db_name_entry.text().strip()
        if file_name:
            if not file_name.endswith('.json'):
                file_name += '.json'
            if not os.path.exists(file_name):
                self.db_name = file_name
                self.shop.save_to_json(file_name)
                self.add_info_label.setText(f"Файл {file_name} успешно создан!")
            else:
                self.add_info_label.setText(f"Ошибка: Файл {file_name} уже существует.")
        else:
            self.add_info_label.setText("Ошибка: Имя файла не указано.")

    def open_json_file(self):
        """Открывает файл JSON и отображает его содержимое в списке."""
        file_name, _ = QFileDialog.getOpenFileName(self, "Выберите файл", "", "JSON Files (*.json)")
        if file_name:
            self.db_name = file_name  # Сохраняем имя файла
            if self.shop.load_from_json(file_name):  # Загружаем товары из файла
                self.add_info_label.setText(f"Файл {file_name} успешно загружен!")
                self.on_read_products()  # Обновляем список товаров в виджете
            else:
                self.add_info_label.setText(f"Ошибка при загрузке файла {file_name}.")

    def show_help_dialog(self):
        """Открытие окна с контактной информацией."""
        help_dialog = HelpDialog()
        help_dialog.exec_()

    def on_add_product(self):
        """Добавление нового товара в файл JSON."""
        name = self.add_product_entry.text()
        price = self.add_price_entry.text()
        quantity = self.add_quantity_entry.text()

        try:
            price = float(price)  # Преобразуем цену в число с плавающей запятой
            quantity = int(quantity)  # Преобразуем количество в целое число
            message = self.shop.add_product(name, price, quantity)  # Добавляем товар в базу данных

            # Проверка на существование пути до файла перед сохранением
            if self.db_name:
                # Попробуем сохранить изменения в файл JSON
                if self.shop.save_to_json(self.db_name):
                    self.add_info_label.setText(message)
                else:
                    self.add_info_label.setText(f"Ошибка при сохранении в файл {self.db_name}.")
            else:
                self.add_info_label.setText("Ошибка: Файл не выбран.")

        except ValueError:
            self.add_info_label.setText("Ошибка: Цена и количество должны быть числами.")

        # Обновляем список товаров после добавления
        self.on_read_products()

    def on_read_products(self):
        """Чтение всех товаров из файла JSON и отображение их в списке."""
        products = self.shop.read_products()
        if not products:
            self.add_info_label.setText("Товары не найдены в файле.")
        else:
            self.product_list_widget.clear()
            for product in products:
                self.product_list_widget.addItem(
                    f"Название: {product['name']}, Цена: {product['price']}грн., Количество: {product['quantity']}шт.")

    def on_delete_product(self):
        """Удаление выбранного товара."""
        selected_product = self.product_list_widget.currentItem()
        if selected_product:
            product_name = selected_product.text().split(',')[0].replace('Название: ', '')
            message = self.shop.delete_product(product_name)

            # Сохраняем изменения в JSON после удаления товара
            if self.db_name:
                if self.shop.save_to_json(self.db_name):
                    self.add_info_label.setText(message)
                else:
                    self.add_info_label.setText(f"Ошибка при сохранении в файл {self.db_name}.")
            else:
                self.add_info_label.setText("Ошибка: Файл не выбран.")

            # Обновляем список товаров после удаления
            self.on_read_products()
        else:
            self.add_info_label.setText("Ошибка: Пожалуйста, выберите товар для удаления.")

    def on_save_products(self):
        """Сохранить весь список товаров в файл JSON."""
        file_name = self.db_name_entry.text().strip()
        if file_name:
            if not file_name.endswith('.json'):
                file_name += '.json'
            if self.shop.save_to_json(file_name):
                self.add_info_label.setText(f"Список товаров успешно сохранен в {file_name}.")
            else:
                self.add_info_label.setText(f"Ошибка при сохранении в файл {file_name}.")
        else:
            self.add_info_label.setText("Ошибка: Имя файла не указано.")

    def closeEvent(self, event):
        """Закрытие программы."""
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ShopApp()
    window.show()
    sys.exit(app.exec_())
