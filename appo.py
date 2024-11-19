from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from kafka import KafkaConsumer
import json
import threading

# Kafka configuration
KAFKA_BROKER = 'localhost:9092'
CLUSTER_TOPICS = ["cluster_topic_1"]

# Initialize Flask app and SocketIO
app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"
socketio = SocketIO(app, cors_allowed_origins="*")

# Function to consume Kafka messages and emit them to the frontend
def consume_kafka():
    consumer = KafkaConsumer(
        *CLUSTER_TOPICS,
        bootstrap_servers=KAFKA_BROKER,
        auto_offset_reset="latest",
        enable_auto_commit=True,
        value_deserializer=lambda x: json.loads(x.decode("utf-8")),
    )
    print(f"Subscriber listening to {', '.join(CLUSTER_TOPICS)}...")
    
    try:
        for message in consumer:
            # Extract the emoji and its scaled count from the message
            emoji = message.value.get('emoji_type')
            scaled_count = message.value.get('scaled_count')
            
            if emoji and scaled_count:
                # Emit emoji and count to the frontend in real-time via SocketIO
                socketio.emit("new_emoji", {"emoji": emoji, "scaled_count": scaled_count})
    except Exception as e:
        print(f"Error in Kafka consumer: {e}")
    finally:
        consumer.close()

# Start Kafka consumer in a separate thread
def start_kafka_consumer():
    thread = threading.Thread(target=consume_kafka)
    thread.daemon = True
    thread.start()

# Route to serve the main page (HTML)
@app.route("/")
def index():
    return render_template("indexo.html")

# Start Kafka consumer when the Flask app starts
if __name__ == "__main__":
    start_kafka_consumer()
    socketio.run(app, host="0.0.0.0", port=5000)
