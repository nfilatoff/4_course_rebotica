import socket

HOST = 'localhost'
PORT = 5555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
client.connect((HOST, PORT))

print('Соединение с диспетчером установлено')

while True:
    data = client.recv(1024).decode()
    print('Сообщение от диспетчера:', data)
    
    if data.lower() == 'пока':
        print('Завершение сеанса')
        break
    if data.lower() == 'прием!':
        while True:
            msg = input('Введите сообщение для диспетчера: ')
            client.sendall(msg.encode('utf-8'))
        
            if msg.lower() == 'пока':
                print('Вы завершили сеанс')
                break
            if msg.lower() == 'прием!':
                print('Ожидание ответа диспетчера...')
                break
client.close()