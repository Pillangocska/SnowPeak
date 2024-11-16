"""RabbitMQ based emergency stop handler."""

import json
import os
from datetime import datetime
from typing import TYPE_CHECKING

import pika
from camel_converter import dict_to_snake

from ski_lift.core.remote.emergency_stop.base import RemoteEmergencyStopHandler
from ski_lift.core.remote.rabbitmq.pika_consumer import PikaConsumer
from ski_lift.core.remote.suggestion.suggestion import Suggestion

if TYPE_CHECKING:
    from ski_lift.core.view import BaseView


class RabbitMQEmergencyStopHandler(RemoteEmergencyStopHandler):

    def __init__(self, view: 'BaseView') -> None:
        self._consumer: PikaConsumer = PikaConsumer(
            exchange='direct_emergency_stop',
            exchange_type='direct',
            route_key=view.lift_id,
            connection_parameters=pika.ConnectionParameters(
                host=os.environ.get('RABBITMQ_HOST', 'localhost'),
                port=int(os.environ.get('RABBITMQ_PORT', 5672)),
                credentials=pika.PlainCredentials(
                    username=os.environ.get('RABBITMQ_USER', 'guest'),
                    password=os.environ.get('RABBITMQ_PASSWORD', 'guest'),
                )
            )
        )
        self._consumer.register_message_callback(self.emergency_stop_callback)
        super().__init__(view=view)

    def start_handling_remote_emergency_stops(self) -> None:
        self._consumer.start()

    def stop_handling_remote_emergency_stops(self) -> None:
        self._consumer.stop()

    def emergency_stop_callback(self, ch, method, properties, body):
        try:
            message: dict = dict_to_snake(json.loads(body.decode('utf-8')))
            abort_time: int = message.get('abort_time', 15)
            self._view.display_suggestion(
                suggestion=Suggestion(
                    sender_card_number=message.get('user'),
                    time=datetime.fromisoformat(message.get('timestamp', datetime.now().isoformat())),
                    message=f'Emergency stop in {abort_time} seconds. Reason: {message.get('message')}',
                    category='DANGER',
                ),
            )
            self._view.emergency_stop(delay=abort_time)
        except Exception:
            pass
