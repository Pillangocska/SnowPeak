"""RabbitMQ command logger."""


from ski_lift.core.monitor.logger.base import BaseCommandLogger
from ski_lift.core.command.descriptor.serializer.base import BaseDescriptorSerializer
from ski_lift.core.command.result.serializer.base import BaseResultSerializer
from ski_lift.core.command.descriptor.object import CommandDescriptor
from ski_lift.core.command.result.object import CommandResult
from ski_lift.core.remote.rabbitmq.pika_client import PikaClient



class RabbitMQCommandLogger(BaseCommandLogger):
    """RabbitMQ command logger."""

    def __init__(
        self,
        descriptor_serializer: BaseDescriptorSerializer,
        result_serializer: BaseResultSerializer,
        pika_client: PikaClient,
    ) -> None:
        self.pika_client = pika_client
        self.pika_client.declare_exchange(exchange='topic_logs', exchange_type='topic')
        super().__init__(descriptor_serializer=descriptor_serializer, result_serializer=result_serializer)


    def process_descriptor_universally(self, command: CommandDescriptor) -> None:
        self.pika_client.send_message(
            exchange='topic_logs',
            routing_key='skilift.logs.command',
            body=self.serialize_command(command),
        )

    def process_result_universally(self, result: CommandResult) -> None:
        self.pika_client.send_message(
            exchange='topic_logs',
            routing_key='skilift.logs.result',
            body=self.serialize_result(result),
        )
