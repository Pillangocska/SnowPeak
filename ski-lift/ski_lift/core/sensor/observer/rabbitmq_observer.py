from ski_lift.core.sensor.observer.sensor_observer import SensorObserver
from ski_lift.core.sensor.factory.base_sensor import SensorReading

class RabbitMQObserver(SensorObserver):
    """Sends sensor readings to RabbitMQ."""
    def __init__(self, rabbitmq_client):
        self.rabbitmq_client = rabbitmq_client

    def update(self, reading: SensorReading) -> None:
        message = {
            'lift_id': reading.lift_id,
            'location': reading.location,
            'value': reading.value,
            'timestamp': str(reading.timestamp)
        }
        self.rabbitmq_client.send_message(reading.sensor_type, message)
