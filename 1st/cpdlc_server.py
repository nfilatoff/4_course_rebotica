import socket
from loguru import logger

HOST = 'localhost'
PORT = 5555

logger.info("Запуск сервера")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
server.bind((HOST, PORT))
server.listen(1)

logger.info("Ожидание пилота")
print("Ожидание пилота")

conn, addr = server.accept()
logger.info(f"Пилот подключился: {addr}")
print(f"Пилот подключился: {addr}")

while True:
    msg = input("Введите сообщение для пилота: ")
    logger.info(f"Отправка пилоту: {msg}")
    conn.sendall(msg.encode("utf-8"))

    if msg.lower() == "пока":
        logger.warning("Диспетчер завершил сеанс")
        print("Завершение сеанса")
        break

    elif msg.lower() == "прием!":
        while True:
            logger.info("Ожидание ответа пилота")
            print("Ожидание ответа пилота...")
            data = conn.recv(1024).decode()

            logger.info(f"Ответ пилота: {data}")
            print("Ответ пилота:", data)

            if data.lower() == "пока":
                logger.warning("Пилот завершил сеанс")
                print("Пилот завершил сеанс")
                break

            if data.lower() == "прием!":
                logger.info("Пилот передал управление диспетчеру")
                break

conn.close()
logger.info("Соединение закрыто")
