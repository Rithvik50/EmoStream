from kafka import KafkaConsumer
import json

# Kafka configuration
KAFKA_BROKER = 'localhost:9092'  # Replace with your Kafka broker address

# Initialize the Kafka consumer
consumer = KafkaConsumer(
    'emoji_topic',
    bootstrap_servers=[KAFKA_BROKER],
    auto_offset_reset='latest',  # Start reading from the earliest message
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("Listening for messages on 'emoji_topic'...")

# Consume messages from the topic
for message in consumer:
    data = message.value
    print(f"Received emoji data: {data}")
