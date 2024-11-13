import json
import os
import time

import pika


class RabbitMQClient:
    def __init__(self):
        self.host = os.environ.get('RABBITMQ_HOST', 'localhost')
        self.port = int(os.environ.get('RABBITMQ_PORT', 5672))
        self.user = os.environ.get('RABBITMQ_USER', 'guest')
        self.password = os.environ.get('RABBITMQ_PASSWORD', 'guest')
        self.connection = None
        self.channel = None
        self.connect()

    def connect(self):
        if not self.connection or self.connection.is_closed:
            credentials = pika.PlainCredentials(self.user, self.password)
            parameters = pika.ConnectionParameters(
                host=self.host,
                port=self.port,
                credentials=credentials
            )
            try:
                self.connection = pika.BlockingConnection(parameters)
                self.channel = self.connection.channel()
                print(f"Connected to RabbitMQ at {self.host}:{self.port}")
                self.channel.queue_declare(queue='sensor_data', durable=True)
            except pika.exceptions.AMQPConnectionError as e:
                print(f"Failed to connect to RabbitMQ: {e}")
                self.connection = None
                self.channel = None

    def send_message(self, queue, message):
        max_retries = 3
        for attempt in range(max_retries):
            if not self.channel or self.channel.is_closed:
                self.connect()
            if self.channel:
                try:
                    self.channel.basic_publish(
                        exchange='',
                        routing_key=queue,
                        body=json.dumps(message),
                        properties=pika.BasicProperties(delivery_mode=2)
                    )
                    print(f"Message sent | queue -> {queue} | content -> {message}")
                    return
                except pika.exceptions.AMQPError as e:
                    print(f"Error sending message: {e}")
                    time.sleep(1)  # Wait before retrying
            else:
                time.sleep(1)  # Wait before retrying
        print(f"Failed to send message after {max_retries} attempts | queue -> {queue} | content -> {message}")

    def receive_message(self, queue, callback):
        if self.channel:
            self.channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)
            print(f"Started consuming from queue: {queue}")
            self.channel.start_consuming()
        else:
            print(f"Simulated message receive from queue {queue}")

    def close(self):
        if self.connection:
            self.connection.close()
            print("RabbitMQ connection closed")

    # TODO right now its listening to 'sensor_data' queue, but we will need this to receive lift state updates from main component
    def start_listening(self, callback):
        while True:
            try:
                if not self.channel or self.channel.is_closed:
                    self.connect()
                if self.channel:
                    self.channel.basic_consume(
                        queue='sensor_data',
                        on_message_callback=callback,
                        auto_ack=True
                    )
                    print("Started listening for messages on 'sensor_data' queue.")
                    self.channel.start_consuming()
                else:
                    print("Cannot start listening, no active RabbitMQ channel. Retrying in 5 seconds...")
                    time.sleep(5)
            except pika.exceptions.AMQPError as e:
                print(f"AMQP error: {e}. Reconnecting...")
                time.sleep(5)
            except Exception as e:
                print(f"Unexpected error: {e}. Reconnecting...")
                time.sleep(5)
