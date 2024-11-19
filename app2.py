from flask import Flask, request, jsonify, render_template
from kafka import KafkaProducer
import json
from datetime import datetime

# Kafka configuration
KAFKA_BROKER = 'localhost:9092'
TOPIC = "emoji_topic"

# Initialize the Kafka producer
producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BROKER],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Initialize Flask app
app = Flask(__name__)

# Serve the HTML frontend
@app.route('/')
def index():
    return render_template('index2.html')

# API endpoint to send emoji data to Kafka
@app.route('/send-emoji', methods=['POST'])
def send_emoji():
    data = request.json
    if not data or not all(k in data for k in ("user_id", "emoji_type")):
        return jsonify({"error": "Invalid data format"}), 400

    # Add timestamp in the desired format
    data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Send data to Kafka
    producer.send(TOPIC, value=data)
    return jsonify({"message": "Emoji sent to Kafka", "data": data})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
