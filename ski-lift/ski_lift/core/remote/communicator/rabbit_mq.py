"""RabbitMQ communicator."""

from ...command.descriptor.object import MessageReportCommandDescriptor
from ski_lift.core.remote.communicator.base import RemoteCommunicator
from ski_lift.core.remote.rabbitmq.pika_producer import PikaProducer
import json
from datetime import datetime


class RabbitMQCommunicator(RemoteCommunicator):
    """Rabbit mq based remote communicator."""

    def __init__(self, producer: PikaProducer, *args, **kwargs) -> None:
        self._producer = producer
        super().__init__(*args, **kwargs)

    def send_message_report(self, report: MessageReportCommandDescriptor):
        message_dict = {
            'messageKind': 'messageReport',
            'severity': report.severity.name,
            'timestamp': report.time.isoformat(),
            'user': report.user_card,
            'message': report.message,
        }

        self._producer.publish_message(
            routing_key=f'skilift.{self.lift_id}.logs.message_report',
            message=json.dumps(message_dict).encode('utf-8'),
            headers={'lift_id': self.lift_id}
        )

    def send_status_update(self) -> None:
        message_dict = {
            'messageKind': 'status_update',
            'timestamp': datetime.now().isoformat(),
            'waitingTime': self._controller.queue_time,
            'skiLiftState': self._controller.engine_state.name,
        }

        self._producer.publish_message(
            routing_key=f'skilift.{self.lift_id}.logs.status_update',
            message=json.dumps(message_dict).encode('utf-8'),
            headers={'lift_id': self.lift_id}
        )
    