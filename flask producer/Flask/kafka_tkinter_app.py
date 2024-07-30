import os
import tkinter as tk
from tkinter import scrolledtext
from confluent_kafka import Consumer, KafkaException
from dotenv import load_dotenv

load_dotenv()

# Kafka Configuration
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
KAFKA_TOPIC = 'flight_notifications'
KAFKA_GROUP_ID = 'flights_notification_consumer_group'

# Create Kafka Consumer
def create_kafka_consumer():
    conf = {
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
        'group.id': KAFKA_GROUP_ID,
        'auto.offset.reset': 'earliest'
    }
    consumer = Consumer(conf)
    return consumer

# Kafka Consumer Logic
def consume_messages():
    consumer = create_kafka_consumer()
    consumer.subscribe([KAFKA_TOPIC])

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
                app_window.update_notification(message)
    except KeyboardInterrupt:
        print("Consumer stopped.")
    finally:
        consumer.close()

# Tkinter Application
class AppWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Flight Notifications")

        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20)
        self.text_area.pack(padx=10, pady=10)

        self.clear_button = tk.Button(root, text="Clear Database", command=self.clear_database)
        self.clear_button.pack(pady=10)

    def update_notification(self, message):
        self.text_area.insert(tk.END, f"New notification: {message}\n")
        self.text_area.yview(tk.END)

    def clear_database(self):
        self.text_area.delete(1.0, tk.END)
        print("Database cleared and notifications removed.")

if __name__ == '__main__':
    root = tk.Tk()
    app_window = AppWindow(root)
    
    # Start Kafka Consumer in a separate thread
    import threading
    consumer_thread = threading.Thread(target=consume_messages, daemon=True)
    consumer_thread.start()
    
    root.mainloop()
