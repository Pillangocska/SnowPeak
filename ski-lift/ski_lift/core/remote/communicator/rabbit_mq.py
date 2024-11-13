"""RabbitMQ communicator."""

from ...command.descriptor.object import MessageReportCommandDescriptor
from ski_lift.core.remote.communicator.base import RemoteCommunicator
from ski_lift.core.remote.rabbitmq.pika_producer import PikaProducer
import json


class RabbitMQCommunicator(RemoteCommunicator):
    """Rabbit mq based remote communicator."""

    def __init__(self, lift_id: str, producer: PikaProducer) -> None:
        self._lift_id = lift_id
        self._producer = producer

    def send_message_report(self, report: MessageReportCommandDescriptor):
        message_dict = {
            'messageKind': 'messageReport',
            'severity': report.severity.name,
            'timestamp': report.time.isoformat(),
            'user': report.user_card,
            'message': report.message,
        }

        self._producer.publish_message(
            routing_key=f'skilift.{self._lift_id}.logs.message_report',
            message=json.dumps(message_dict).encode('utf-8'),
            headers={'lift_id': self._lift_id}
        )
    