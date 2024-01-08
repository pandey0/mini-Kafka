import socket
import json
import time

def register_producer(host, port, topic):
    producer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    producer_socket.connect(('127.0.0.1', 55555))

    message = {
        'type': 'register_producer',
        'host': host,
        'port': port,
        'topic': topic
    }

    producer_socket.send(json.dumps(message).encode('utf-8'))
    producer_socket.close()

def send_message(producer_socket, message):
    producer_socket.send(json.dumps({'type': 'publish', 'message': message}).encode('utf-8'))

def main():
    host = '127.0.0.1'
    port = 55556  # Change this to a unique port for each producer
    topic = 'example_topic'

    register_producer(host, port, topic)
    producer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    producer_socket.connect(('127.0.0.1', 55555))

    try:
        while True:
            message = f"Message from Producer at {host}:{port} - {time.time()}"
            send_message(producer_socket, message)
            time.sleep(5)
    except KeyboardInterrupt:
        print("Producer shutting down.")
    finally:
        producer_socket.close()

if __name__ == "__main__":
    main()
