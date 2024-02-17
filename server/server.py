import socket
import threading
import json
import logging
from queue import Queue

class Server:
    def __init__(self, host='127.0.0.1', port=8888):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = {}
        self.addresses = {}
        self.queue = Queue()
        logging.basicConfig(level=logging.INFO)

    def start(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(10)
        logging.info("Server started and listening on {}:{}".format(self.host, self.port))
        accept_thread = threading.Thread(target=self.accept_incoming_connections)
        accept_thread.start()
        accept_thread.join()
        self.socket.close()

    def accept_incoming_connections(self):
        while True:
            client, client_address = self.socket.accept()
            logging.info("{} has connected.".format(client_address))
            self.queue.put(client)
            threading.Thread(target=self.handle_client, args=(client,)).start()

    def handle_client(self, client):
        try:
            while True:
                msg = client.recv(1024).decode("utf8")
                if msg != "":
                    logging.info("Received message: {}".format(msg))
                    self.broadcast(msg, client)
                else:
                    raise Exception("Client disconnected")
        except Exception as e:
            logging.error("Error handling client: {}".format(e))
            client.close()
            self.remove_client(client)

    def broadcast(self, msg, sender):
        for client in self.queue.queue:
            if client != sender:
                try:
                    client.send(msg.encode("utf8"))
                except Exception as e:
                    logging.error("Error broadcasting to {}: {}".format(client, e))
                    client.close()
                    self.remove_client(client)

    def remove_client(self, client):
        if client in self.queue.queue:
            self.queue.queue.remove(client)

if __name__ == "__main__":
    server = Server()
    server.start_server()
