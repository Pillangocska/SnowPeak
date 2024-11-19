
"""Consume ski lift messages example."""

import sys
import pika
import os
import json
from retry import retry


def callback(channel, method, properties, body):
    print(json.dumps(json.loads(body.decode('utf-8')), indent=4))
    print()


@retry(pika.exceptions.AMQPError, delay=5)
def main() -> int:
    if len(sys.argv) < 1:
        print('Usage: consume.py <lift_id>')
        return 1
    
    exchange_name = 'topic_skilift'
    routing_key = f'skilift.{sys.argv[1]}.logs.message_report' 
    
    print('connecting...')
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
    channel.exchange_declare(exchange=exchange_name, exchange_type='topic', durable=True)
    result = channel.queue_declare('', exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=routing_key)
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)    

    try:
        print('start consuming...')
        print('Ctrl + C to exist')
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
        connection.close()

    return 0


if __name__ == '__main__':
    sys.exit(main())