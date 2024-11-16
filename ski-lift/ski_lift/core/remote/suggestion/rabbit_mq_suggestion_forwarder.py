"""RabbitMQ suggestion forwarder."""

import os
from typing import TYPE_CHECKING

import pika

from ski_lift.core.remote.rabbitmq.pika_consumer import PikaConsumer
from ski_lift.core.remote.suggestion.suggestion import Suggestion
from ski_lift.core.remote.suggestion.suggestion_forwarder import \
    SuggestionForwarder

if TYPE_CHECKING:
    from ski_lift.core.view.base_view import BaseView


class RabbitMQSuggestionForwarder(SuggestionForwarder):

    def __init__(self, view: 'BaseView') -> None:
        self._consumer: PikaConsumer = PikaConsumer(
            exchange='direct_suggestions',
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
        self._consumer.register_message_callback(self.suggestion_callback)
        super().__init__(view=view)

    def start_handling_suggestions(self) -> None:
        self._consumer.start()

    def stop_handling_suggestions(self):
        self._consumer.stop()

    def suggestion_callback(self, ch, method, properties, body):
        self._view.display_suggestion(Suggestion.from_json(body.decode('utf-8')))