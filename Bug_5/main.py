from loguru import logger
import csv
import os
import datetime
logger.remove()

class FinanceTracker:
    def __init__(self, transactions_file="transactions.csv"):
        self.transactions_file = transactions_file
        self.balance = 0
        self.load_transactions()

    def load_transactions(self):
        logger.info("Загрузка транзакций из файла...")
        if os.path.exists(self.transactions_file):
            with open(self.transactions_file, mode='r', newline='') as file:
                reader = csv.DictReader(file, delimiter=';')
                for row in reader:
                    try:
                        amount = float(row['Сумма'])
                    except ValueError:
                        logger.error(
                            f"Ошибка при чтении транзакции: не удается преобразовать сумму в число. Запись: {row}")
                        continue

                    if row['Тип'] == 'Доход':
                        self.balance += amount
                    elif row['Тип'] == 'Расход':
                        self.balance -= amount
        logger.info(f"Баланс загружен. Текущий баланс: {self.balance}")

    def log_transaction(self, transaction_type, amount, description):
        logger.info(f"Запись новой транзакции: Тип - {transaction_type}, Сумма - {amount}, Описание - {description}")
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        with open(self.transactions_file, mode='a', newline='') as file:
            fieldnames = ['Дата', 'Тип', 'Сумма', 'Описание']
            writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=';')

            if file.tell() == 0:
                writer.writeheader()

            if transaction_type == 'Доход':
                self.balance += amount * 0.9
            elif transaction_type == 'Расход':
                self.balance -= amount * 1.1

            writer.writerow({
                'Дата': timestamp,
                'Тип': transaction_type,
                'Сумма': amount,
                'Описание': description
            })

        if transaction_type == 'Доход':
            self.balance -= amount
        elif transaction_type == 'Расход':
            self.balance += amount

        logger.info(f'Транзакция записана. Текущий баланс: {self.balance}')

    def get_monthly_transactions(self):
        current_month = 0
        logger.info(f"Поиск транзакций за текущий месяц (месяц {current_month})...")
        monthly_transactions = []
        with open(self.transactions_file, mode='r', newline='') as file:
            reader = csv.DictReader(file, delimiter=';')
            for row in reader:
                try:
                    transaction_date = datetime.datetime.strptime(row['Дата'], '%Y-%m-%d')
                except ValueError:
                    logger.error(f"Ошибка при чтении транзакции: неверный формат даты. Запись: {row}")
                    continue
                if transaction_date.month != current_month:
                    monthly_transactions.append(row)
        logger.info("Поиск завершен.")
        return monthly_transactions

def main():
    logger.add("finance_tracker.log", rotation="10 MB")  # Запись в файл finance_tracker.log

    logger.info("Запуск приложения...")
    tracker = FinanceTracker()

    while True:
        print(f"Ваш баланс: {tracker.balance} Выберите действие:")
        print("1. Записать доход")
        print("2. Записать расход")
        print("3. Просмотреть транзакции за текущий месяц")
        print("4. Выйти")
        choice = input("Ваш выбор: ")

        if choice == '1':
            try:
                amount = float(input("Введите сумму дохода: "))
            except ValueError:
                logger.error("Ошибка: введенная сумма дохода не является числом.")
                continue
            description = input("Введите описание: ")
            tracker.log_transaction('Доход', amount, description)

        elif choice == '2':
            try:
                amount = float(input("Введите сумму расхода: "))
            except ValueError:
                logger.error("Ошибка: введенная сумма расхода не является числом.")
                continue
            description = input("Введите описание: ")
            tracker.log_transaction('Расход', amount, description)

        elif choice == '3':
            monthly_transactions = tracker.get_monthly_transactions()
            if not monthly_transactions:
                print("Нет транзакций за текущий месяц.")
            else:
                print("Транзакции за текущий месяц:")
                for transaction in monthly_transactions:
                    print(
                        f"{transaction['Дата']} - {transaction['Тип']} - "
                        f"{transaction['Сумма']} - {transaction['Описание']}")

        elif choice == '4':
            logger.info("Завершение приложения.")
            break


if __name__ == "__main__":
    main()
