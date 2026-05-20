import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel,
    QSlider, QColorDialog, QFileDialog, QVBoxLayout, QHBoxLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from art_color import ArtConverter

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Art Converter")
        self.resize(600, 400)

        self.image_label = QLabel("Здесь будет изображение")
        self.image_label.setFixedSize(350,350)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("border: 1px solid black;")
        
        self.converted_image_label = QLabel("Здесь будет ASCII-арт")
        self.converted_image_label.setFixedSize(350,350)
        self.converted_image_label.setAlignment(Qt.AlignCenter)
        self.converted_image_label.setStyleSheet("border: 1px solid black;")
        

        self.load_btn = QPushButton("Загрузить фото")
        self.save_btn = QPushButton("Сохранить фото")
        self.color_btn = QPushButton("Выбрать цвет")

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(1)
        self.slider.setMaximum(50)
        self.slider.setValue(12)


        #self.setLayout(layout)
        
        images_layout = QHBoxLayout()
        images_layout.addWidget(self.image_label)
        images_layout.addWidget(self.converted_image_label)

        
        main_layout = QVBoxLayout()
        main_layout.addLayout(images_layout)
        main_layout.addWidget(self.load_btn)
        main_layout.addWidget(self.slider)
        main_layout.addWidget(self.color_btn)
        main_layout.addWidget(self.save_btn)
        
        self.setLayout(main_layout)
        
        
        #self.path = self.load_btn.clicked.connect(self.load_image)
        self.load_btn.clicked.connect(self.load_image)
        self.color_btn.clicked.connect(self.choose_color)
        self.save_btn.clicked.connect(self.save_image)

        self.ConverterApp = ArtConverter()
        #self.rgb_image, self.gray_image = self.ConverterApp.get_image(self.path)

    def load_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Открыть изображение")
        if file_name:
            pixmap = QPixmap(file_name)
            self.image_label.setPixmap(
                pixmap.scaled(300, 300, Qt.KeepAspectRatio)
            )

            # Загружаем изображение в converter
            self.ConverterApp.get_image(file_name)
            ascii_path = self.ConverterApp.save_ascii_art()
            self.load_converted_image(ascii_path)

            print("Изображение загружено:", file_name)


    def load_converted_image(self, path):
        try:
            pixmap = QPixmap(path)
            self.converted_image_label.setPixmap(
                pixmap.scaled(300, 300, Qt.KeepAspectRatio)
            )
        except Exception as e:
            print("Ошибка при загрузке ASCII изображения:", e)

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