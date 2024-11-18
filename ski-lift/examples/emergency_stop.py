"""Consume ski lift messages example."""

import sys
import pika
import os
import json
from datetime import datetime
from time import sleep


def main() -> int:
    if len(sys.argv) < 2:
        print('Usage: emergency_stop.py <lift_id>')
        return 1
    
    exchange_name = 'direct_emergency_stop'
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
    
    print(f'Sending emergency stop ...')
    channel.basic_publish(
        exchange=exchange_name,
        routing_key=routing_key,
        body=json.dumps({
            "user": "abc123",
            "timestamp": datetime.now().isoformat(),
            "message": "This is an emergency stop.",
            "abortTime": 15
        }).encode('utf-8'),
        
    )
    return 0


if __name__ == '__main__':
    sys.exit(main())