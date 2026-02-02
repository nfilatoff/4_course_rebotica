import sys
import csv
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QListWidget, QLabel, QLineEdit,
    QTextEdit, QSpinBox, QMessageBox
)



class Task:
    def __init__(self, title, description, importance=1, status="Новая"):
        self.title = title
        self.description = description
        self.importance = importance
        self.status = status

    def mark_as_done(self):
        self.status = "Завершена"


class TaskManager:
    def __init__(self, tasks_file="tasks.csv"):
        self.tasks_file = tasks_file
        self.tasks = []
        self.completed_tasks = []
        self.load_tasks()

    def load_tasks(self):
        if not os.path.exists(self.tasks_file):
            return

        with open(self.tasks_file, newline="", encoding="cp1251") as file:
            reader = csv.DictReader(file, delimiter=";")
            for row in reader:
                task = Task(
                    row["Title"],
                    row["Description"],
                    int(row["Importance"]),
                    row["Status"]
                )

                if task.status == "Завершена":
                    self.completed_tasks.append(task)
                else:
                    self.tasks.append(task)

    def save_tasks(self):
        with open(self.tasks_file, "w", newline="", encoding="cp1251") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(["Title", "Description", "Importance", "Status"])

            for task in self.tasks + self.completed_tasks:
                writer.writerow([
                    task.title,
                    task.description,
                    task.importance,
                    task.status
                ])

    def add_task(self, task):
        self.tasks.append(task)
        self.save_tasks()

    def mark_task_as_done(self, title):
        for task in self.tasks:
            if task.title == title:
                task.mark_as_done()
                self.tasks.remove(task)
                self.completed_tasks.append(task)
                self.save_tasks()
                return



class TaskManagerGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.manager = TaskManager()

        self.setWindowTitle("Task Manager")
        self.resize(800, 550)


        self.build_ui()
        self.refresh_lists()

    def build_ui(self):
        main_layout = QVBoxLayout()

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Заголовок")

        self.desc_input = QTextEdit()
        self.desc_input.setPlaceholderText("Описание")

        self.importance_input = QSpinBox()
        self.importance_input.setRange(1, 5)
        self.description_view = QTextEdit()
        self.description_view.setReadOnly(True)
        self.description_view.setPlaceholderText("Здесь будет описание задачи...")


        add_btn = QPushButton("Добавить")
        add_btn.clicked.connect(self.add_task)

        main_layout.addWidget(QLabel("Описание выбранной задачи"))
        main_layout.addWidget(self.description_view)
        main_layout.addWidget(QLabel("Новая задача"))
        main_layout.addWidget(self.title_input)
        main_layout.addWidget(self.desc_input)
        main_layout.addWidget(QLabel("Важность"))
        main_layout.addWidget(self.importance_input)
        main_layout.addWidget(add_btn)

        lists_layout = QHBoxLayout()

        self.active_list = QListWidget()
        self.completed_list = QListWidget()

        self.active_list.itemClicked.connect(self.show_description)
        self.active_list.itemDoubleClicked.connect(self.show_popup)

        self.completed_list.itemClicked.connect(self.show_description)
        self.completed_list.itemDoubleClicked.connect(self.show_popup)

        lists_layout.addWidget(self.make_block("Активные", self.active_list))
        lists_layout.addWidget(self.make_block("Завершённые", self.completed_list))

        main_layout.addLayout(lists_layout)

        done_btn = QPushButton("Отметить как выполненную")
        done_btn.clicked.connect(self.mark_done)

        delete_btn = QPushButton("Удалить выполненную")
        delete_btn.clicked.connect(self.delete_completed)

        main_layout.addWidget(done_btn)
        main_layout.addWidget(delete_btn)

        self.setLayout(main_layout)

    def make_block(self, title, widget):
        layout = QVBoxLayout()
        layout.addWidget(QLabel(title))
        layout.addWidget(widget)

        container = QWidget()
        container.setLayout(layout)
        return container

    def find_task_by_title(self, title):
        for task in self.manager.tasks + self.manager.completed_tasks:
            if task.title == title:
                return task
        return None

    def show_description(self, item):
        title = item.text().split(" | ")[0]
        task = self.find_task_by_title(title)

        if task:
            text = (
                f"Заголовок: {task.title}\n"
                f"Важность: {task.importance}\n"
                f"Статус: {task.status}\n\n"
                f"{task.description}"
            )
            self.description_view.setText(text)

    def show_popup(self, item):
        title = item.text().split(" | ")[0]
        task = self.find_task_by_title(title)

        if task:
            QMessageBox.information(
                self,
                task.title,
                task.description or "Описание пустое"
            )

    def refresh_lists(self):
        self.active_list.clear()
        self.completed_list.clear()

        for task in sorted(self.manager.tasks, key=lambda t: t.importance):
            self.active_list.addItem(
                f"{task.title} | {task.importance}"
            )

        for task in self.manager.completed_tasks:
            self.completed_list.addItem(task.title)

    def add_task(self):
        title = self.title_input.text().strip()
        desc = self.desc_input.toPlainText().strip()
        importance = self.importance_input.value()

        if not title:
            QMessageBox.warning(self, "Ошибка", "Введите заголовок")
            return

        task = Task(title, desc, importance)
        self.manager.add_task(task)

        self.title_input.clear()
        self.desc_input.clear()

        self.refresh_lists()

    def mark_done(self):
        item = self.active_list.currentItem()
        if not item:
            return

        title = item.text().split(" | ")[0]
        self.manager.mark_task_as_done(title)
        self.refresh_lists()

    def delete_completed(self):
        item = self.completed_list.currentItem()
        if not item:
            return

        title = item.text()

        self.manager.completed_tasks = [
            t for t in self.manager.completed_tasks if t.title != title
        ]
        self.manager.save_tasks()

        self.refresh_lists()



def main():
    app = QApplication(sys.argv)
    window = TaskManagerGUI()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
