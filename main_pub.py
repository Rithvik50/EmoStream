from kafka import KafkaConsumer
import json

# Define the topic and bootstrap server
TOPIC = "aggregated_emoji_topic"
BOOTSTRAP_SERVERS = "localhost:9092"

# Create a Kafka consumer for the main publisher
consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=BOOTSTRAP_SERVERS,
    auto_offset_reset="latest",  # Start reading at the latest offset
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode("utf-8")),  # Deserialize JSON
)

print(f"Listening for messages on topic '{TOPIC}'...")

# Listen for messages and forward to Cluster Publisher
try:
    for message in consumer:
        print(f"Received message: {message.value}")
        # Forward the message to cluster publishers
        # This step is implemented in the Cluster Publisher below
        # Add your forwarding logic here
except KeyboardInterrupt:
    print("Consumer stopped.")
finally:
    consumer.close()
