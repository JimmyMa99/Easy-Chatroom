import socket
import threading

def client_thread(conn, addr):
    while True:
        try:
            message = conn.recv(1024).decode()
            if message:
                print(f"Message from {addr}: {message}")
                # 这里可以添加消息转发逻辑
        except:
            conn.close()
            break

def server():
    host = '127.0.0.1'
    port = 12345
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()

    print("Server started, waiting for connections...")
    while True:
        conn, addr = server_socket.accept()
        print(f"Connection from {addr}")
        threading.Thread(target=client_thread, args=(conn, addr)).start()

# 运行服务器
server()
