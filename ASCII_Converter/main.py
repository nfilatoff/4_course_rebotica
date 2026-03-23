import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel,
    QSlider, QColorDialog, QFileDialog, QVBoxLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Art Converter")
        self.resize(600, 400)

        self.image_label = QLabel("Здесь будет изображение")

        self.load_btn = QPushButton("Загрузить фото")
        self.save_btn = QPushButton("Сохранить фото")
        self.color_btn = QPushButton("Выбрать цвет")

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(1)
        self.slider.setMaximum(50)
        self.slider.setValue(12)

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.load_btn)
        layout.addWidget(self.slider)
        layout.addWidget(self.color_btn)
        layout.addWidget(self.save_btn)

        self.setLayout(layout)

        self.load_btn.clicked.connect(self.load_image)
        self.color_btn.clicked.connect(self.choose_color)
        self.save_btn.clicked.connect(self.save_image)


    def load_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Открыть изображение")
        if file_name:
            pixmap = QPixmap(file_name)
            self.image_label.setPixmap(pixmap.scaled(300, 300, Qt.KeepAspectRatio))

    def choose_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            print("Цвет:", color.name())

    def save_image(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Сохранить изображение")
        if file_name:
            print("Сохранено:", file_name)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())