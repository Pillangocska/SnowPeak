"""Consume ski lift messages example."""

import sys
import pika
import os
import json
from datetime import datetime
from time import sleep


def main() -> int:
    if len(sys.argv) < 2:
        print('Usage: suggestion.py <lift_id>')
        return 1
    
    exchange_name = 'direct_suggestions'
    routing_key = sys.argv[1]
    
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
    channel.exchange_declare(exchange=exchange_name, exchange_type='direct', durable=True)

    for severity in ['INFO', 'WARNING', 'DANGER']:
        print(f'Sending "{severity}" suggestion ...')
        channel.basic_publish(
            exchange=exchange_name,
            routing_key=routing_key,
            body=json.dumps({
                'messageKind': 'suggestion',
                'user': 'abc123',
                'severity': severity,
                'timestamp': datetime.now().isoformat(),
                'message': 'This is a message.'
            }).encode('utf-8')
        )  
        sleep(5)
    return 0


if __name__ == '__main__':
    sys.exit(main())