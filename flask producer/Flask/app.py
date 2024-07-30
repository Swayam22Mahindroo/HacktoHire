from flask import Flask, jsonify, request
import sqlite3
import os
from dotenv import load_dotenv
from confluent_kafka import Producer
from flask_cors import CORS  # Import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS
DATABASE = 'flights.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    return conn

def init_db():
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS flights (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                flight_id TEXT NOT NULL,
                status TEXT NOT NULL,
                gate TEXT NOT NULL
            )
        ''')
        db.commit()

def create_kafka_producer():
    conf = {
        'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092'),
        'client.id': 'flights_app_producer'
    }
    producer = Producer(conf)
    return producer

kafka_producer = create_kafka_producer()

def send_notification_to_kafka(message):
    kafka_producer.produce('flight_notifications', value=message)
    kafka_producer.flush()

@app.route('/flights', methods=['GET'])
def get_flights():
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute('SELECT id, flight_id, status, gate FROM flights')
        flights = cursor.fetchall()
        return jsonify([{'id': row[0], 'flight_id': row[1], 'status': row[2], 'gate': row[3]} for row in flights])

@app.route('/flights', methods=['POST'])
def add_flight():
    data = request.json
    flight_id = data.get('flight_id')
    status = data.get('status')
    gate = data.get('gate')

    with get_db() as db:
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO flights (flight_id, status, gate) VALUES (?, ?, ?)
        ''', (flight_id, status, gate))
        db.commit()

    message = f"New flight added: {flight_id}, Status: {status}, Gate: {gate}"
    send_notification_to_kafka(message)

    return jsonify({'message': 'Flight added successfully'}), 201

@app.route('/flights/<int:id>', methods=['GET'])
def get_flight(id):
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute('SELECT id, flight_id, status, gate FROM flights WHERE id = ?', (id,))
        flight = cursor.fetchone()
        if flight:
            return jsonify({'id': flight[0], 'flight_id': flight[1], 'status': flight[2], 'gate': flight[3]})
        else:
            return jsonify({'error': 'Flight not found'}), 404

@app.route('/flights/<int:id>', methods=['PUT'])
def update_flight(id):
    data = request.json
    flight_id = data.get('flight_id')
    status = data.get('status')
    gate = data.get('gate')

    with get_db() as db:
        cursor = db.cursor()
        cursor.execute('''
            UPDATE flights SET flight_id = ?, status = ?, gate = ? WHERE id = ?
        ''', (flight_id, status, gate, id))
        db.commit()

    message = f"Flight updated: ID: {id}, Flight: {flight_id}, Status: {status}, Gate: {gate}"
    send_notification_to_kafka(message)

    return jsonify({'message': 'Flight updated successfully'})

@app.route('/flights/<int:id>', methods=['DELETE'])
def delete_flight(id):
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute('DELETE FROM flights WHERE id = ?', (id,))
        db.commit()

    return jsonify({'message': 'Flight deleted successfully'})

@app.route('/clear', methods=['DELETE'])
def clear_flights():
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute('DELETE FROM flights')
        db.commit()

    return jsonify({'message': 'All flights cleared'})

if __name__ == '__main__':
    if not os.path.exists(DATABASE):
        init_db()
    app.run(debug=True)
