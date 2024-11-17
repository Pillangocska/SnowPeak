"""RabbitMQ suggestion forwarder."""

from typing import TYPE_CHECKING

from ski_lift.core.remote.suggestion.suggestion import Suggestion
from ski_lift.core.remote.suggestion.suggestion_forwarder import \
    SuggestionForwarder

if TYPE_CHECKING:
    from ski_lift.core.view.base_view import BaseView
    from ski_lift.core.remote.rabbitmq.pika_consumer import PikaConsumer


class RabbitMQSuggestionForwarder(SuggestionForwarder):

    def __init__(self, view: 'BaseView') -> None:
        # todo: refactor code to prevent circular import 
        from ski_lift.use_cases import create_pika_consumer
        self._consumer: 'PikaConsumer' = create_pika_consumer(
            exchange_name='direct_suggestions',
            exchange_type='direct',
            lift_id=view.lift_id,
            callback=self.suggestion_callback,
        )
        super().__init__(view=view)

    def start_handling_suggestions(self) -> None:
        self._consumer.start()

    def stop_handling_suggestions(self):
        self._consumer.stop()

    def suggestion_callback(self, ch, method, properties, body):
        print('received suggestion')
        self._view.display_suggestion(Suggestion.from_json(body.decode('utf-8')))