# Yet Another Kafka (YaK) - Mini Kafka Implementation

## Overview
This repository contains the implementation of a distributed system based on Apache Kafka for managing topics, coordinating producers and consumers, and ensuring fault-tolerance and recovery. The system consists of three main components:

## Mini-Zookeeper (server.py)

Monitors the health of Kafka Brokers and facilitates leader election.
Listens for incoming connections from Kafka Brokers and Producers/Consumers.
Registers Kafka Brokers when they connect (register_broker message type).
Handles heartbeats from Kafka Brokers to monitor their health (heartbeat message type).
Initiates leader election if a broker is presumed dead.

## Kafka Brokers (broker.py)

Manages topics, coordinates producers and consumers, implements Fault-Tolerance, Recovery, Leader Election, and Partitioning.
Registers with the Mini-Zookeeper during startup (register_broker message type).
Sends heartbeats to the Mini-Zookeeper to indicate their health (heartbeat message type).
Receives leader information from the Mini-Zookeeper (leader_info message type) during registration.
Initiates leader election if the Mini-Zookeeper doesn't detect a heartbeat from the leader.
Coordinates with other Kafka Brokers to handle publish (publish message type) and consume operations.
Manages topics, partitions, and messages.
Handles recovery of messages and partitions after a failure.

## Kafka Producer (producer.py)

Publishes messages to Kafka Topics.
Registers with the Mini-Zookeeper during startup (register_producer message type).
Sends messages to Kafka Brokers (publish message type).
May request the creation of a new topic if it does not exist.

## Kafka Consumer (consumer.py)

Consumes messages from Kafka Topics.
Registers with the Mini-Zookeeper during startup (register_consumer message type).
Requests messages from Kafka Brokers (consume message type).
May request the creation of a new topic if it does not exist.
Supports receiving all messages from the beginning of a topic (--from-beginning flag).

# Overall Working
## Startup:
Mini-Zookeeper starts listening for connections.
Kafka Brokers and Producers/Consumers connect to the Mini-Zookeeper.
3Broker Registration:
Kafka Brokers register with the Mini-Zookeeper during startup.
Mini-Zookeeper sends the current leader information to the new broker.
## Heartbeats:
Kafka Brokers periodically send heartbeats to the Mini-Zookeeper.
If the Mini-Zookeeper detects a lack of heartbeat from the leader, it triggers leader election.
## Leader Election:
If a broker is presumed dead, the Mini-Zookeeper initiates leader election.
New leader information is broadcasted to all brokers.
## Publish Operation:
Kafka Producers send messages to Kafka Brokers.
Kafka Brokers, including the leader, handle the publish operation.
Messages are stored in topics and partitions.
## Consume Operation:
Kafka Consumers request messages from Kafka Brokers.
Kafka Brokers handle the consume operation, providing the requested messages.
## Fault-Tolerance and Recovery:
Brokers handle failures by recovering messages and partitions after a failure.
Leader election is triggered in the absence of heartbeats from the current leader.
This interaction pattern creates a distributed system where Kafka Brokers coordinate with each other and with the Mini-Zookeeper to ensure the reliability and fault-tolerance of the overall system. The system is designed to handle failures, recover messages, and elect leaders dynamically.

## Features

- Mini-Zookeeper for monitoring broker health and leader election.
- Kafka Brokers responsible for managing topics and coordinating producers and consumers.
- Basic Fault-Tolerance and Recovery mechanisms.
- Leader Election to ensure system resilience.
- Simple Partitioning for handling messages.

## Components

1. **server.py (Mini-Zookeeper and Kafka Brokers)**: Handles mini-Zookeeper and Kafka Broker functionalities.

2. **broker.py (Kafka Broker)**: Implementation of Kafka Broker with Leader Election and Heartbeat mechanism.

3. **producer.py (Kafka Producer)**: Implementation of Kafka Producer to publish messages to a specified topic.

4. **consumer.py (Kafka Consumer)**: Implementation of Kafka Consumer to receive messages from a specified topic.

## Setup

1. **Install Python**: Ensure Python is installed on your system.

2. **Clone the Repository**:
3. **Run Mini-Zookeeper and Kafka Brokers**:

    ```bash
    python server.py
    ```

4. **Run Kafka Brokers (One for each broker)**:

    ```bash
    python broker.py
    ```

5. **Run Kafka Producers and Consumers (As needed)**:

    ```bash
    python producer.py
    ```

    ```bash
    python consumer.py
    ```

## Configuration

- Update host and port numbers in the source code as needed.
- Customize the system behavior by modifying the logic in each component.

## Contributing

If you would like to contribute to YaK, please follow the guidelines outlined in [CONTRIBUTING.md](CONTRIBUTING.md).


