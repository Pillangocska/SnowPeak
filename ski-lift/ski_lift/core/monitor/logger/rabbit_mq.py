"""RabbitMQ command logger."""


from ski_lift.core.command.descriptor.object import CommandDescriptor
from ski_lift.core.command.descriptor.serializer.base import \
    BaseDescriptorSerializer
from ski_lift.core.command.result.object import CommandResult
from ski_lift.core.command.result.serializer.base import BaseResultSerializer
from ski_lift.core.monitor.logger.base import BaseCommandLogger
from ski_lift.core.remote.rabbitmq.pika_producer import PikaProducer


class RabbitMQCommandLogger(BaseCommandLogger):
    """RabbitMQ command logger.
    
    This logger uses rabbit mq exchanges to send log messages to subscribed
    nodes.

    By default, it uses the routing key pattern
    `skilift.<lift_id>.logs.command.<outcome>`. Since the exchange is a topic,
    this routing key supports various filtering options.
    """

    def __init__(
        self,
        result_serializer: BaseResultSerializer,
        pika_producer: PikaProducer,
        lift_id: str,
    ) -> None:
        self._pika_producer: PikaProducer = pika_producer
        self._lift_id: str = lift_id
        super().__init__(result_serializer=result_serializer)


    def process_result_universally(self, result: CommandResult) -> None:
        outcome: str = 'successful' if result.is_successful else 'failed'
        self._pika_producer.publish_message(
            routing_key=f'skilift.{self._lift_id}.logs.command.{outcome}',
            message=self.serialize_result(result),
            headers={'lift_id': self._lift_id}
        )
