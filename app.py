from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, emit
from kafka import KafkaProducer, KafkaConsumer
import json
import threading
from datetime import datetime

# Kafka configuration
KAFKA_BROKER = 'localhost:9092'
SEND_TOPIC = "emoji_topic"
CLUSTER_TOPICS = ["cluster_topic_1"]

# Initialize Flask app
app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"
socketio = SocketIO(app, cors_allowed_origins="*")

# Kafka Producer for sending emojis
producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BROKER],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Kafka Consumer for consuming emojis
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
            emoji = message.value.get('emoji_type')
            scaled_count = message.value.get('scaled_count')
            
            if emoji and scaled_count:
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

# API endpoint to send emoji data to Kafka
@app.route('/send-emoji', methods=['POST'])
def send_emoji():
    data = request.json
    if not data or not all(k in data for k in ("user_id", "emoji_type")):
        return jsonify({"error": "Invalid data format"}), 400

    # Add timestamp in the desired format
    data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Send data to Kafka
    producer.send(SEND_TOPIC, value=data)
    return jsonify({"message": "Emoji sent to Kafka", "data": data})

# Route to serve the main page (HTML)
@app.route("/")
def index():
    return render_template("index.html")

# Start Kafka consumer when the Flask app starts
if __name__ == "__main__":
    start_kafka_consumer()
    socketio.run(app, host="0.0.0.0", port=5000)
