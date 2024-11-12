from ski_lift.app.entity.ski_lift_authorizer import SkiLiftAuthorizer
from ski_lift.app.entity.ski_lift_controller import SkiLiftController
from ski_lift.core.auth.authenticator.in_memory_authenticator import InMemoryAuthenticator
from ski_lift.core.engine import Engine
from ski_lift.core.monitor.logger.file import FileCommandLogger
from ski_lift.core.monitor.logger.rabbit_mq import RabbitMQCommandLogger
from ski_lift.core.view.cli_view import CommandLineInterfaceView
import sys
from ski_lift.core.command.descriptor.serializer.pretty_string import PrettyStringDescriptorSerializer
from ski_lift.core.command.descriptor.serializer.json_bytes import JSONBytesDescriptorSerializer
from ski_lift.core.command.result.serializer.pretty_string import PrettyResultStringSerializer
from ski_lift.core.command.result.serializer.json_bytes import JSONBytesResultSerializer
from ski_lift.core.remote.rabbitmq.pika_producer import PikaProducer
import pika
from ski_lift.core.remote.suggestion.rabbit_mq_suggestion_forwarder import RabbitMQSuggestionForwarder
import os
from ski_lift.core.sensor.sensor_data_generator import SensorDataGenerator
from ski_lift.core.sensor.observer.rabbitmq_observer import RabbitMQObserver
from threading import Thread
from ski_lift.core.utils import get_lift_id_or_exit


def setup_sensor(lift_id: str, pika_producer: PikaProducer) -> None:
    sensor_config = {
        'base_temperature': {'mean_temp': -5, 'amplitude': 3},
        'peak_temperature': {'mean_temp': -15, 'amplitude': 3},
        'base_wind': {'base_speed': 12, 'randomness': 1.5},
        'peak_wind': {'base_speed': 20, 'randomness': 2}
    }
    generator = SensorDataGenerator(lift_id=lift_id, sensor_config=sensor_config)
    observer: RabbitMQObserver = RabbitMQObserver(pika_producer=pika_producer)
    for sensor in generator.sensors.values():
        sensor.attach(observer)
    Thread(target=generator.generate_continuous_data, daemon=True).start()


def create_pika_producer() -> PikaProducer:
    pika_producer = PikaProducer(
        exchange='topic_skilift',
        exchange_type='topic',
        connection_parameters=pika.ConnectionParameters(
            host=os.environ.get('RABBITMQ_HOST', 'localhost'),
            port=int(os.environ.get('RABBITMQ_PORT', 5672)),
            credentials=pika.PlainCredentials(
                username=os.environ.get('RABBITMQ_USER', 'guest'),
                password=os.environ.get('RABBITMQ_PASSWORD', 'guest'),
            )
        )
    )
    pika_producer.start()
    return pika_producer



def main() -> int:
    lift_id: str = get_lift_id_or_exit()

    # create an example authenticator and register a card number
    authenticator = InMemoryAuthenticator()
    authenticator.add('secret')

    # create a controller which needs an engine and an authorizer
    controller = SkiLiftController(engine=Engine(), authorizer=SkiLiftAuthorizer(authenticator=authenticator))
    command_logger = FileCommandLogger(PrettyStringDescriptorSerializer(), PrettyResultStringSerializer())
    command_logger.attach_to(controller)

    pika_producer: PikaProducer = create_pika_producer()
    setup_sensor(lift_id=lift_id, pika_producer=pika_producer)

    rabbit_logger = RabbitMQCommandLogger(
        descriptor_serializer=JSONBytesDescriptorSerializer(),
        result_serializer=JSONBytesResultSerializer(),
        pika_producer=pika_producer,
        lift_id=lift_id,
    )
    rabbit_logger.attach_to(controller)

    cli = CommandLineInterfaceView(controller=controller)

    controller.start()
    cli.start_handling_user_inputs()
    controller.stop()
    pika_producer.stop()
    return 0


if __name__ == '__main__':
    sys.exit(main())