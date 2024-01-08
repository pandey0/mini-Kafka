import socket
import json
import time

def register_consumer(host, port, topic):
    consumer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    consumer_socket.connect(('127.0.0.1', 55555))

    message = {
        'type': 'register_consumer',
        'host': host,
        'port': port,
        'topic': topic
    }

    consumer_socket.send(json.dumps(message).encode('utf-8'))
    consumer_socket.close()

def fetch_messages(consumer_socket):
    consumer_socket.send(json.dumps({'type': 'consume'}).encode('utf-8'))
    data = consumer_socket.recv(1024).decode('utf-8')
    messages = json.loads(data)['messages']
    return messages

def main():
    host = '127.0.0.1'
    port = 55557  # Change this to a unique port for each consumer
    topic = 'example_topic'

    register_consumer(host, port, topic)
    consumer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    consumer_socket.connect(('127.0.0.1', 55555))

    try:
        while True:
            messages = fetch_messages(consumer_socket)
            print(f"Consumer at {host}:{port} received messages: {messages}")
            time.sleep(5)
    except KeyboardInterrupt:
        print("Consumer shutting down.")
    finally:
        consumer_socket.close()

if __name__ == "__main__":
    main()
