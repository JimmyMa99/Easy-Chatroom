import socket

def client():
    host = '127.0.0.1'
    port = 12345
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    
    while True:
        message = input("Enter your message: ")
        client_socket.send(message.encode())

# 运行客户端
client()
