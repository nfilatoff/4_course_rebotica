import sys
import csv
import os
import datetime
from loguru import logger

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QTextEdit,
    QListWidget, QMessageBox
)


logger.remove()
logger.add("finance_tracker.log", rotation="10 MB")

class FinanceTracker:
    def __init__(self, transactions_file="transactions.csv"):
        self.transactions_file = transactions_file
        self.balance = 0
        self.load_transactions()

    def load_transactions(self):
        self.balance = 0

        if not os.path.exists(self.transactions_file):
            return

        with open(self.transactions_file, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=';')

            for row in reader:
                try:
                    amount = float(row['Сумма'])
                except ValueError:
                    continue

                if row['Тип'] == 'Доход':
                    self.balance += amount
                elif row['Тип'] == 'Расход':
                    self.balance -= amount

    def log_transaction(self, transaction_type, amount, description):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

        with open(self.transactions_file, mode='a', newline='', encoding='utf-8') as file:
            fieldnames = ['Дата', 'Тип', 'Сумма', 'Описание']
            writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=';')

            if file.tell() == 0:
                writer.writeheader()

            writer.writerow({
                'Дата': timestamp,
                'Тип': transaction_type,
                'Сумма': amount,
                'Описание': description
            })

        self.load_transactions()

    def get_monthly_transactions(self):
        current_month = datetime.datetime.now().month
        result = []

        if not os.path.exists(self.transactions_file):
            return result

        with open(self.transactions_file, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=';')

            for row in reader:
                try:
                    d = datetime.datetime.strptime(row['Дата'], '%Y-%m-%d %H:%M:%S.%f')
                except ValueError:
                    continue

                if d.month == current_month:
                    result.append(row)

        return result


class FinanceApp(QWidget):
    def __init__(self):
        super().__init__()

        self.tracker = FinanceTracker()

        self.setWindowTitle("Finance Tracker")
        self.resize(500, 600)

        self.build_ui()
        self.update_balance()

    def build_ui(self):
        layout = QVBoxLayout()

        # Баланс
        self.balance_label = QLabel()
        self.balance_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(self.balance_label)

        # Сумма
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Сумма")
        layout.addWidget(self.amount_input)

        # Описание
        self.desc_input = QTextEdit()
        self.desc_input.setPlaceholderText("Описание")
        self.desc_input.setFixedHeight(60)
        layout.addWidget(self.desc_input)

        # Кнопки доход/расход
        btn_layout = QHBoxLayout()

        income_btn = QPushButton("Доход")
        expense_btn = QPushButton("Расход")

        income_btn.clicked.connect(lambda: self.add_transaction('Доход'))
        expense_btn.clicked.connect(lambda: self.add_transaction('Расход'))

        btn_layout.addWidget(income_btn)
        btn_layout.addWidget(expense_btn)

        layout.addLayout(btn_layout)

        # Кнопка показать месяц
        show_btn = QPushButton("Показать транзакции за месяц")
        show_btn.clicked.connect(self.show_monthly)
        layout.addWidget(show_btn)

        # Список транзакций
        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        self.setLayout(layout)


    def update_balance(self):
        self.tracker.load_transactions()
        self.balance_label.setText(f"Баланс: {self.tracker.balance:.2f}")

    def add_transaction(self, t_type):
        try:
            amount = float(self.amount_input.text())
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Введите корректную сумму")
            return

        description = self.desc_input.toPlainText()

        self.tracker.log_transaction(t_type, amount, description)

        self.amount_input.clear()
        self.desc_input.clear()

        self.update_balance()

    def show_monthly(self):
        self.list_widget.clear()

        transactions = self.tracker.get_monthly_transactions()

        if not transactions:
            self.list_widget.addItem("Нет транзакций за текущий месяц")
            return

        for t in transactions:
            text = f"{t['Дата']} | {t['Тип']} | {t['Сумма']} | {t['Описание']}"
            self.list_widget.addItem(text)


def main():
    app = QApplication(sys.argv)
    window = FinanceApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()