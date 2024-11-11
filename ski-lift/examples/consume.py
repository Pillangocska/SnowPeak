"""Consume ski lift messages example."""

import sys
import pika
import os
import json


def callback(channel, method, properties, body):
    print(json.dumps(json.loads(body.decode('utf-8')), indent=4))
    print()


def main() -> int:
    if len(sys.argv) < 3:
        print('Usage: consume.py <exchange_name> <routing_key>')
        return 1
    
    exchange_name = sys.argv[1]
    routing_key = sys.argv[2]
    
    connection = pika.BlockingConnection(
        parameters=pika.ConnectionParameters(
            host=os.environ.get('RABBITMQ_HOST', 'localhost'),
            port=int(os.environ.get('RABBITMQ_PORT', 5672)),
            credentials=pika.PlainCredentials(
                username=os.environ.get('RABBITMQ_USER', 'guest'),
                password=os.environ.get('RABBITMQ_PASSWORD', 'guest'),
            )
        )
    )
    channel = connection.channel()
    channel.exchange_declare(exchange=exchange_name, exchange_type='topic')
    result = channel.queue_declare('', exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=routing_key)
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)    

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
        connection.close()
    return 0


if __name__ == '__main__':
    sys.exit(main())