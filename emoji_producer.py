from kafka import KafkaProducer
import json
import time
import random
from datetime import datetime

# Kafka configuration
KAFKA_BROKER = 'localhost:9092'  # Replace with your Kafka broker address
LINGER_MS = 500  # Set flush interval for Kafka producer

# Initialize the Kafka producer
producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BROKER],
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    linger_ms=LINGER_MS
)

def send_emoji_data(user_id, emoji_type, timestamp):
    """Send emoji data to Kafka topic."""
    data = {
        "user_id": user_id,
        "emoji_type": emoji_type,
        "timestamp": timestamp
    }
    producer.send("emoji_topic", value=data)

if __name__ == "__main__":
    while True:
        start_time = time.time()
        
        # Send 100 messages in a single second
        for _ in range(100):
            user_id = random.randint(1, 100)
            emoji_type = random.choice(["😀", "😢", "🔥", "💯"])
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Current system time in human-readable format
            
            send_emoji_data(user_id, emoji_type, timestamp)
            print(f"Sent emoji data: {user_id}, {emoji_type}, {timestamp}")
        
        # Ensure it waits until one second has passed since start of loop
        elapsed_time = time.time() - start_time
        if elapsed_time < 1:
            time.sleep(1 - elapsed_time)
