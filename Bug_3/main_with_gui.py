import sys
import csv
from loguru import logger
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QMessageBox
)


class Room:
    def __init__(self, name, length, width, height,
                 wall_cost, ceiling_cost, floor_cost):
        self.name = name
        self.length = length
        self.width = width
        self.height = height
        self.wall_cost = wall_cost
        self.ceiling_cost = ceiling_cost
        self.floor_cost = floor_cost

    def wall_area(self):
        return 2 * (self.length + self.width) * self.height

    def ceiling_area(self):
        return self.length * self.width

    def floor_area(self):
        return self.length * self.width

    def total_cost(self):
        return (
            self.wall_area() * self.wall_cost +
            self.ceiling_area() * self.ceiling_cost +
            self.floor_area() * self.floor_cost
        )


class Apartment:
    def __init__(self):
        self.rooms = []

    def add_room(self, room):
        self.rooms.append(room)

    def total_cost(self):
        return sum(room.total_cost() for room in self.rooms)


class ApartmentApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Расчёт стоимости ремонта")
        self.apartment = Apartment()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Название
        layout.addWidget(QLabel("Название комнаты"))
        self.name_input = QLineEdit()
        layout.addWidget(self.name_input)

        # Размеры
        dim_layout = QHBoxLayout()
        self.length_input = QLineEdit()
        self.width_input = QLineEdit()
        self.height_input = QLineEdit()

        dim_layout.addWidget(QLabel("Длина"))
        dim_layout.addWidget(self.length_input)
        dim_layout.addWidget(QLabel("Ширина"))
        dim_layout.addWidget(self.width_input)
        dim_layout.addWidget(QLabel("Высота"))
        dim_layout.addWidget(self.height_input)

        layout.addLayout(dim_layout)

        # Цены комнаты
        cost_layout = QHBoxLayout()
        self.wall_cost = QLineEdit()
        self.ceiling_cost = QLineEdit()
        self.floor_cost = QLineEdit()

        cost_layout.addWidget(QLabel("Стены (м²)"))
        cost_layout.addWidget(self.wall_cost)
        cost_layout.addWidget(QLabel("Потолок (м²)"))
        cost_layout.addWidget(self.ceiling_cost)
        cost_layout.addWidget(QLabel("Пол (м²)"))
        cost_layout.addWidget(self.floor_cost)

        layout.addLayout(cost_layout)

        add_btn = QPushButton("Добавить комнату")
        add_btn.clicked.connect(self.add_room)
        layout.addWidget(add_btn)

        # Таблица
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(
            ["Комната", "Стены м²", "Потолок м²", "Пол м²", "Стоимость"]
        )
        layout.addWidget(self.table)

        self.result_label = QLabel("Итого: 0")
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def add_room(self):
        try:
            room = Room(
                self.name_input.text(),
                float(self.length_input.text()),
                float(self.width_input.text()),
                float(self.height_input.text()),
                float(self.wall_cost.text()),
                float(self.ceiling_cost.text()),
                float(self.floor_cost.text())
            )
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Проверьте введённые данные")
            return

        self.apartment.add_room(room)

        row = self.table.rowCount()
        self.table.insertRow(row)

        self.table.setItem(row, 0, QTableWidgetItem(room.name))
        self.table.setItem(row, 1, QTableWidgetItem(f"{room.wall_area():.2f}"))
        self.table.setItem(row, 2, QTableWidgetItem(f"{room.ceiling_area():.2f}"))
        self.table.setItem(row, 3, QTableWidgetItem(f"{room.floor_area():.2f}"))
        self.table.setItem(row, 4, QTableWidgetItem(f"{room.total_cost():.2f}"))

        self.update_total()
        self.clear_inputs()

    def update_total(self):
        total = self.apartment.total_cost()
        self.result_label.setText(f"Итого: {total:.2f}")
        self.save_csv(total)

    def save_csv(self, total):
        with open("results.csv", "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(["Комната", "Стены м²", "Потолок м²", "Пол м²", "Стоимость"])
            for r in self.apartment.rooms:
                writer.writerow([
                    r.name,
                    r.wall_area(),
                    r.ceiling_area(),
                    r.floor_area(),
                    r.total_cost()
                ])
            writer.writerow(["Итого", "", "", "", total])

    def clear_inputs(self):
        self.name_input.clear()
        self.length_input.clear()
        self.width_input.clear()
        self.height_input.clear()
        self.wall_cost.clear()
        self.ceiling_cost.clear()
        self.floor_cost.clear()


if __name__ == "__main__":
    logger.add("app.log")
    app = QApplication(sys.argv)
    window = ApartmentApp()
    window.show()
    sys.exit(app.exec_())
