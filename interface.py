from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QFormLayout, QWidget, QPushButton, QComboBox
import sys  # Только для доступа к аргументам командной строки


# Подкласс QMainWindow для настройки главного окна приложения
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Конфигуратор')
        self.setFixedSize(QSize(800, 600))
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("Введите ip адрес")
        self.ip_input.setMaxLength(15)
        self.hostname_input = QLineEdit()
        self.hostname_input.setPlaceholderText("Введите Hostname коммутатора")
        self.hostname_input.setMaxLength(15)
        self.vendor_box = QComboBox()
        self.vendor_box.addItems(["Qtech", "Eltex", "SNR"])
        self.model_box = QComboBox()
        self.vendor_box.currentTextChanged.connect(self.chenged_vendor_box)
        self.button = QPushButton("Создать конфигурацию")
        self.button.clicked.connect(self.the_button_was_clicked)
        layout = QFormLayout()
        layout.addRow('IP:', self.ip_input)
        layout.addRow('Hostname:', self.hostname_input)
        layout.addRow('Производитель: ', self.vendor_box)
        layout.addRow('Модель:', self.model_box)
        layout.addWidget(self.button)

        container = QWidget()
        container.setLayout(layout)

        # Устанавливаем центральный виджет Window
        self.setCentralWidget(container)

    def the_button_was_clicked(self):
        print(self.ip_input.text().strip())


    def chenged_vendor_box(self):
        if self.vendor_box.currentText() == 'SNR':
            self.model_box.clear()
            self.model_box.addItems(['1', '2', '3'])
        elif self.vendor_box.currentText() == "Eltex":
            self.model_box.clear()
            self.model_box.addItems(['4', '5', '6'])


app = QApplication(sys.argv)

# Создаём виджет Qt - окно
window = MainWindow()
window.show()  # Важно: окно по умолчанию скрыто.

# Запускаем цикл событий
app.exec()

# Приложение не доберётся сюда, пока вы не выйдете и цикл
# событий не остановится.
