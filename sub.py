from kafka import KafkaConsumer
import json

# Define Kafka topics (all cluster topics)
CLUSTER_TOPICS = ["cluster_topic_1", "cluster_topic_2", "cluster_topic_3"]
BOOTSTRAP_SERVERS = "localhost:9092"

# Create Kafka consumer to listen to multiple cluster topics
consumer = KafkaConsumer(
    *CLUSTER_TOPICS,  # Subscribing to all cluster topics
    bootstrap_servers=BOOTSTRAP_SERVERS,
    auto_offset_reset="latest",  # Start reading at the latest offset
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode("utf-8")),  # Deserialize JSON
)

print(f"Subscriber listening to {', '.join(CLUSTER_TOPICS)}...")

# Listen for messages from all cluster topics and process them
try:
    for message in consumer:
        print(f"Received message from {message.topic}: {message.value}")
except KeyboardInterrupt:
    print("Subscriber stopped.")
finally:
    consumer.close()
