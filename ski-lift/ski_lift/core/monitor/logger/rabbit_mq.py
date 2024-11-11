"""RabbitMQ command logger."""


from ski_lift.core.monitor.logger.base import BaseCommandLogger
from ski_lift.core.command.descriptor.serializer.base import BaseDescriptorSerializer
from ski_lift.core.command.result.serializer.base import BaseResultSerializer
from ski_lift.core.command.descriptor.object import CommandDescriptor
from ski_lift.core.command.result.object import CommandResult
from ski_lift.core.remote.rabbitmq.pika_producer import PikaProducer



class RabbitMQCommandLogger(BaseCommandLogger):
    """RabbitMQ command logger."""

    def __init__(
        self,
        descriptor_serializer: BaseDescriptorSerializer,
        result_serializer: BaseResultSerializer,
        pika_producer: PikaProducer,
        lift_id: str,
    ) -> None:
        self._pika_producer: PikaProducer = pika_producer
        self._lift_id: str = lift_id
        super().__init__(descriptor_serializer=descriptor_serializer, result_serializer=result_serializer)


    def process_descriptor_universally(self, command: CommandDescriptor) -> None:
        pass

    def process_result_universally(self, result: CommandResult) -> None:
        outcome: str = 'successful' if result.is_successful else 'failed'
        self._pika_producer.publish_message(
            routing_key=f'skilift.{self._lift_id}.logs.command.{outcome}',
            message=self.serialize_result(result),
            headers={'lift_id': self._lift_id}
        )
