from kafka import KafkaConsumer, KafkaProducer
import json

# Kafka configurations
MAIN_TOPIC = "aggregated_emoji_topic"
CLUSTER_TOPICS = ["cluster_topic_1"]
BOOTSTRAP_SERVERS = "localhost:9092"

# Create Kafka producer to send data to cluster topics
producer = KafkaProducer(
    bootstrap_servers=BOOTSTRAP_SERVERS,
    value_serializer=lambda x: json.dumps(x).encode("utf-8")  # Serialize JSON
)

# Create Kafka consumer to listen to the main publisher topic
consumer = KafkaConsumer(
    MAIN_TOPIC,
    bootstrap_servers=BOOTSTRAP_SERVERS,
    auto_offset_reset="latest",
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode("utf-8")),
)

print(f"Listening for messages on '{MAIN_TOPIC}'...")

# Function to forward the messages to all cluster topics
def forward_to_clusters(message):
    for cluster_topic in CLUSTER_TOPICS:
        producer.send(cluster_topic, value=message)
        print(f"Forwarded message to {cluster_topic}: {message}")

# Consume and forward messages
try:
    for message in consumer:
        print(f"Received message from main topic: {message.value}")
        forward_to_clusters(message.value)  # Forward to each cluster topic
except KeyboardInterrupt:
    print("Cluster Publisher stopped.")
finally:
    consumer.close()
    producer.close()
