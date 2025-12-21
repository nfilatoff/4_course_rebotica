import socket
from loguru import logger

HOST = 'localhost'
PORT = 5555

logger.info("Запуск клиента")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
client.connect((HOST, PORT))

logger.info("Соединение с диспетчером установлено")
print("Соединение с диспетчером установлено")

while True:
    data = client.recv(1024).decode()
    logger.info(f"Сообщение от диспетчера: {data}")
    print("Сообщение от диспетчера:", data)

    if data.lower() == "пока":
        logger.warning("Диспетчер завершил сеанс")
        print("Завершение сеанса")
        break

    if data.lower() == "прием!":
        while True:
            msg = input("Введите сообщение для диспетчера: ")
            logger.info(f"Отправка диспетчеру: {msg}")
            client.sendall(msg.encode("utf-8"))

            if msg.lower() == "пока":
                logger.warning("Пилот завершил сеанс")
                print("Вы завершили сеанс")
                break

            if msg.lower() == "прием!":
                logger.info("Передача управления диспетчеру")
                print("Ожидание ответа диспетчера...")
                break

client.close()
logger.info("Соединение закрыто")
