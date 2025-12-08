import socket

HOST = 'localhost'
PORT = 5555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
server.bind((HOST, PORT))
server.listen(1)

print('Ожидание пилота')
conn, addr = server.accept()
print(f'Пилот подключился:', {addr})

while True:
    msg = input('Введите сообщение для пилота: ')
    conn.sendall(msg.encode('utf-8'))

    if msg.lower() == 'пока':
        print('Завершение сеанса')
        break
    
    elif msg.lower() == 'прием!':
        while True:
            print('Ожидание ответа пилота...')
            data = conn.recv(1024).decode()
            print('Ответ пилота:', data)
            
            if data.lower() == 'пока':
                print('Пилот завершили сеанс')
                break
            if data.lower() == 'прием!':
                break

conn.close()
