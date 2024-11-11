"""RabbitMQ suggestion forwarder."""

from ski_lift.core.remote.suggestion.suggestion_forwarder import SuggestionForwarder
import pika
from ski_lift.core.view.base_view import BaseView
from ski_lift.core.remote.suggestion.suggestion import Suggestion


class RabbitMQSuggestionForwarder(SuggestionForwarder):

    def __init__(self, view: BaseView, lift_id: str) -> None:
        self._connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self._channel = self._connection.channel()
        self._channel.exchange_declare(
            exchange='direct_suggestions',
            exchange_type='direct',
        )
        self._queue = self._channel.queue_declare(lift_id)
        self._channel.queue_bind(exchange='direct_suggestions', queue=lift_id, routing_key=lift_id)
        self._channel.basic_consume(queue=lift_id, on_message_callback=self.suggestion_callback, auto_ack=True)
        super().__init__(view=view)

    def handle_suggestions(self) -> None:
        self._channel.start_consuming()

    def suggestion_callback(self, ch, method, properties, body):
        self._view.display_suggestion(Suggestion.from_json(body.decode('utf-8')))