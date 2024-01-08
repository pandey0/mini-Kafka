import socket
import threading
import json
import time
import random

class MiniZookeeper:
    def __init__(self):
        self.brokers = []
        self.leader = None

# You can add more functionality to KafkaBroker class as per your requirements
class KafkaBroker:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.topics = {}
        self.is_leader = False
        self.last_heartbeat = time.time()

def handle_client(client, mini_zookeeper):
    try:
        while True:
            data = client.recv(1024).decode('utf-8')
            if not data:
                break

            message = json.loads(data)

            if message['type'] == 'register_broker':
                broker = KafkaBroker(message['host'], message['port'])
                mini_zookeeper.brokers.append(broker)
                print(f"Registered Broker: {broker.host}:{broker.port}")

                if mini_zookeeper.leader is None:
                    broker.is_leader = True
                    mini_zookeeper.leader = broker

                # Send current leader info to the new broker
                client.send(json.dumps({'type': 'leader_info', 'leader': mini_zookeeper.leader.__dict__}).encode('utf-8'))

            elif message['type'] == 'heartbeat':
                broker = next(b for b in mini_zookeeper.brokers if b.host == message['host'] and b.port == message['port'])
                broker.last_heartbeat = time.time()

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client.close()

def leader_election(mini_zookeeper):
    while True:
        time.sleep(5)

        current_time = time.time()
        for broker in mini_zookeeper.brokers:
            if current_time - broker.last_heartbeat > 10:
                # Assume broker is dead, trigger leader election
                print(f"Broker {broker.host}:{broker.port} is presumed dead. Initiating Leader Election.")
                mini_zookeeper.brokers.remove(broker)

                if broker.is_leader:
                    mini_zookeeper.leader = None
                    for other_broker in mini_zookeeper.brokers:
                        other_broker.is_leader = True
                        mini_zookeeper.leader = other_broker
                        print(f"New Leader: {other_broker.host}:{other_broker.port}")
                        break  # Assign leadership to the first available broker

def main():
    mini_zookeeper = MiniZookeeper()

    host = '127.0.0.1'
    port = 55555
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()

    # Start the leader election thread
    election_thread = threading.Thread(target=leader_election, args=(mini_zookeeper,))
    election_thread.start()

    try:
        while True:
            client, address = server.accept()
            print(f"Connection from {address}")
            client_handler = threading.Thread(target=handle_client, args=(client, mini_zookeeper))
            client_handler.start()
    except KeyboardInterrupt:
        print("Server shutting down.")
    finally:
        server.close()

if __name__ == "__main__":
    main()
