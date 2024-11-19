"""RabbitMQ based emergency stop handler."""

import json
from datetime import datetime
from typing import TYPE_CHECKING

from camel_converter import dict_to_snake

from ski_lift.core.remote.emergency_stop.base import RemoteEmergencyStopHandler
from ski_lift.core.remote.suggestion.suggestion import Suggestion

if TYPE_CHECKING:
    from ski_lift.core.remote.rabbitmq.pika_consumer import PikaConsumer
    from ski_lift.core.view import BaseView


class RabbitMQEmergencyStopHandler(RemoteEmergencyStopHandler):
    """RabbitMQ emergency stopper.
    
    This is a concrete implementation of the emergency stopper that utilizes
    RabbitMQ exchanges to receive emergency stop signals.
    """

    def __init__(self, view: 'BaseView') -> None:
        # todo: refactor code to prevent circular import 
        from ski_lift.use_cases import create_pika_consumer
        self._consumer: 'PikaConsumer' = create_pika_consumer(
            exchange_name='direct_emergency_stop',
            exchange_type='direct',
            lift_id=view.lift_id,
            callback=self.emergency_stop_callback,
            observer=view,
        )
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
                    message=f'{message.get('message')}\nEmergency stop in {abort_time} seconds.',
                    category='DANGER',
                ),
                reset_input=False,
            )
            self._view.emergency_stop(delay=abort_time)
        except Exception:
            pass
