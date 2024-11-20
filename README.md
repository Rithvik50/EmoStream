# Emoji Stream

This is a concurrent emoji broadcast system built using Kafka, Flask, and Spark in an event-driven architecture. This project enables real-time emoji broadcasting, processing, and aggregation.

## Project Structure

```plaintext
.
├── app.py
├── emoji_consumer.py
├── emoji_producer.py
├── cluster_pub.py
├── main_pub.py
├── requirements.txt
├── spark.py
├── sub.py
└── index.html
```

## Files Overview

- **`app.py`**: Main Flask application with Kafka producer and consumer functionalities
- **`emoji_consumer.py`**: Kafka consumer script for receiving emoji messages
- **`emoji_producer.py`**: Kafka producer script to send emoji messages
- **`cluster_pub.py`**: Kafka consumer and producer script for forwarding messages to cluster topics
- **`main_pub.py`**: Kafka consumer for listening to aggregated emoji messages
- **`requirements.txt`**: List of required Python dependencies
- **`spark.py`**: Spark job for processing and aggregating emoji data from Kafka
- **`sub.py`**: Kafka consumer for listening to multiple cluster topics
- **`index.html`**: HTML webpage to display the emoji stream

## Setup and Installation

### Prerequisites

- Kafka
- Zookeeper
- Spark
- Python 3.x

### Steps to Run

1. Start Zookeeper:
   ```bash
   zookeeper-server-start.sh config/zookeeper.properties
   ```

2. Start Kafka:
   ```bash
   kafka-server-start.sh config/server.properties
   ```

3. Run Flask Applications:
   ```bash
   python app.py
   ```

4. Run Kafka Producer:
   ```bash
   python emoji_producer.py
   ```

5. Run Spark Job:
   ```bash
   python spark.py
   ```

6. Access Web Interface:
   ```
   http://localhost:5000
   ```

## Usage

- Send emoji messages through the web interface
- Watch real-time emoji processing and aggregation
- View aggregated emoji statistics

## Technologies

- Flask: Web framework
- Kafka: Message broker
- Spark: Distributed processing engine
- Zookeeper: Cluster coordination service

## Troubleshooting

- Verify Kafka and Zookeeper are running
- Check terminal logs for errors
- Ensure Kafka is producing messages correctly
