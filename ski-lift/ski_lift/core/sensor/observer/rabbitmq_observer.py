from ski_lift.core.sensor.observer.sensor_observer import SensorObserver
from ski_lift.core.sensor.factory.base_sensor import SensorReading
from ski_lift.core.remote.rabbitmq.pika_producer import PikaProducer
import json

class RabbitMQObserver(SensorObserver):
    """Sends sensor readings to RabbitMQ."""
    def __init__(self, pika_producer: PikaProducer):
        self._pika_producer = pika_producer

    def update(self, reading: SensorReading) -> None:
        reading_type: str = reading.sensor_type.split('.')[1]
        message = {
            'messageKind': 'sensor',
            'type': reading_type,
            'value': reading.value,
            'timestamp': reading.timestamp.isoformat(),
            'location': reading.location,
        }
        self._pika_producer.publish_message(
            routing_key=f'skilift.{reading.lift_id}.logs.sensor.{reading_type}',
            message=json.dumps(message).encode('utf-8'),
            headers={'lift_id': reading.lift_id},
        )
