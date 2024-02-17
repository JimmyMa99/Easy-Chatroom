import socket
import threading
import openai

class Client:
    def __init__(self, host='127.0.0.1', port=8888):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.username = input("Enter your username: ")
        openai.api_key = "EMPTY"
        self.base_url = 'http://127.0.0.1:9002/v1/'  # Adjust as necessary
        self.history = []

    def receive_message(self):
        while True:
            try:
                message = self.socket.recv(1024).decode("utf-8")
                if message:
                    print(message)
                    response = self.process_message_with_openai(message)
                    if response:
                        self.send_message('['+self.username+']：'+response, is_response=True)
                    print("AI Response:", response)
                else:
                    print("Disconnected from server")
                    self.socket.close()
                    break
            except Exception as e:
                print("Error receiving message:", e)
                self.socket.close()
                break

    def send_message(self, message=None, is_response=False):
        if not is_response:
            message = input("") if message is None else message
            message = f"[{self.username}] {message}"
        try:
            self.socket.send(message.encode("utf-8"))
        except Exception as e:
            print("Error sending message:", e)
            self.socket.close()

    def process_message_with_openai(self, message):
        client = openai.OpenAI(
            api_key="EMPTY",
            base_url=self.base_url,
        )

        messages = [{'role': 'system', 'content': '你是'+self.username}]  # System message remains at the beginning
        for exchange in self.history:
            messages.append({'role': 'user', 'content': exchange['user']})
            messages.append({'role': 'assistant', 'content': exchange['assistant']})
        
        # Add the current message to the messages list
        messages.append({'role': 'user', 'content': message})

        try:
            completion = client.chat.completions.create(
                model='yi-chat',
                messages=messages,
                temperature=0.5,
                max_tokens=50,
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"Error processing message with OpenAI: {e}"

    def start(self):
        try:
            self.socket.connect((self.host, self.port))
            print("Connected to server.")
            threading.Thread(target=self.receive_message).start()
            self.send_message()
        except Exception as e:
            print("Connection error:", e)
            self.socket.close()

if __name__ == "__main__":
    client = Client()
    client.start()
