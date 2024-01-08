import socket
import threading
import json
import time

class KafkaBroker:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.topics = {}
        self.is_leader = False
        self.last_heartbeat = time.time()

def handle_client(client, broker, mini_zookeeper):
    try:
        while True:
            data = client.recv(1024).decode('utf-8')
            if not data:
                break

            message = json.loads(data)

            if message['type'] == 'leader_info':
                mini_zookeeper.leader = KafkaBroker(**message['leader'])

            elif message['type'] == 'heartbeat':
                broker.last_heartbeat = time.time()

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client.close()

def send_heartbeat(broker, mini_zookeeper):
    while True:
        time.sleep(2)

        if broker.is_leader:
            for other_broker in mini_zookeeper.brokers:
                if other_broker is not broker:
                    try:
                        other_broker_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        other_broker_socket.connect((other_broker.host, other_broker.port))
                        other_broker_socket.send(json.dumps({'type': 'heartbeat', 'host': broker.host, 'port': broker.port}).encode('utf-8'))
                        other_broker_socket.close()
                    except Exception as e:
                        print(f"Failed to send heartbeat to {other_broker.host}:{other_broker.port}: {e}")

def main():
    host = '127.0.0.1'
    port = 55556  # Change this to a unique port for each broker

    broker = KafkaBroker(host, port)
    mini_zookeeper_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mini_zookeeper_socket.connect(('127.0.0.1', 55555))

    message = {
        'type': 'register_broker',
        'host': broker.host,
        'port': broker.port
    }

    mini_zookeeper_socket.send(json.dumps(message).encode('utf-8'))
    leader_info = json.loads(mini_zookeeper_socket.recv(1024).decode('utf-8'))
    mini_zookeeper_socket.close()

    if leader_info['leader'] is not None:
        mini_zookeeper.leader = KafkaBroker(**leader_info['leader'])
        broker.is_leader = broker.host == mini_zookeeper.leader.host and broker.port == mini_zookeeper.leader.port

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()

    # Start the heartbeat thread
    heartbeat_thread = threading.Thread(target=send_heartbeat, args=(broker, mini_zookeeper))
    heartbeat_thread.start()

    try:
        while True:
            client, address = server.accept()
            print(f"Connection from {address}")
            client_handler = threading.Thread(target=handle_client, args=(client, broker, mini_zookeeper))
            client_handler.start()
    except KeyboardInterrupt:
        print("Broker shutting down.")
    finally:
        server.close()

if __name__ == "__main__":
    main()
