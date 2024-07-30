from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit
import os
import threading
from confluent_kafka import Consumer, KafkaException
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

notifications = []

def create_kafka_consumer():
    conf = {
        'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092'),
        'group.id': 'flights_notification_consumer_group',
        'auto.offset.reset': 'earliest'
    }
    consumer = Consumer(conf)
    return consumer

def consume_messages():
    consumer = create_kafka_consumer()
    consumer.subscribe(['flight_notifications'])

    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaException._PARTITION_EOF:
                    print(f"End of partition reached {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")
                else:
                    print(f"Error: {msg.error()}")
            else:
                message = msg.value().decode('utf-8')
                print(f"Received message: {message}")  # Debug print
                notifications.append(message)
                socketio.emit('new_notification', {'message': message})
    except KeyboardInterrupt:
        print("Consumer stopped.")
    finally:
        consumer.close()

@app.route('/')
def index():
    return render_template('index.html', notifications=notifications)

@app.route('/notifications', methods=['GET'])
def get_notifications():
    return jsonify(notifications)

@app.route('/clear_notifications', methods=['POST'])
def clear_notifications():
    notifications.clear()
    return jsonify({'status': 'cleared'})

if __name__ == '__main__':
    consumer_thread = threading.Thread(target=consume_messages, daemon=True)
    consumer_thread.start()
    socketio.run(app, debug=True, port=5001)
