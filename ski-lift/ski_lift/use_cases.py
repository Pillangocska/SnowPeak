"""Ski lift use cases."""

import os
from typing import List

from ski_lift.app.entity import SkiLiftAuthorizer, SkiLiftController
from ski_lift.core.auth import BaseAuthenticator, InMemoryAuthenticator
from ski_lift.core.controller import Controller
from ski_lift.core.engine import Engine
from ski_lift.core.remote import PikaProducer
import pika
from ski_lift.core.sensor import RabbitMQObserver, SensorDataGenerator
from threading import Thread
from ski_lift.core.monitor.logger import FileCommandLogger, RabbitMQCommandLogger
from ski_lift.core.command.descriptor.serializer import PrettyStringDescriptorSerializer, JSONBytesDescriptorSerializer
from ski_lift.core.command.result.serializer import PrettyResultStringSerializer, JSONBytesResultSerializer
from ski_lift.core.remote.communicator.rabbit_mq import RabbitMQCommunicator


def attach_loggers_to(controller: Controller, producer: PikaProducer):
    attach_file_logger_to(controller)
    attach_rabbit_mq_logger_to(controller, controller.lift_id, producer)


def attach_file_logger_to(controller: Controller):
    command_logger = FileCommandLogger(PrettyStringDescriptorSerializer(), PrettyResultStringSerializer())
    command_logger.attach_to(controller)

def attach_rabbit_mq_logger_to(controller: Controller, lift_id: str, producer: PikaProducer):
    rabbit_logger = RabbitMQCommandLogger(
        descriptor_serializer=JSONBytesDescriptorSerializer(),
        result_serializer=JSONBytesResultSerializer(),
        pika_producer=producer,
        lift_id=lift_id,
    )
    rabbit_logger.attach_to(controller)



def create_controller(lift_id: str, producer: PikaProducer) -> Controller:
    """Create a controller with an authorizer."""
    return SkiLiftController(
        lift_id=lift_id,
        engine=Engine(),
        authorizer=SkiLiftAuthorizer(authenticator=create_authenticate_from_env()),
        remote_communicator=RabbitMQCommunicator(lift_id=lift_id, producer=producer)
    )


def create_authenticate_from_env() -> BaseAuthenticator:
    """Create authenticator from users defined in env variables."""
    workers_str: str = os.getenv('WORKER_OPERATORS', 'secret')
    workers: List[str] = workers_str.split(',')
    
    authenticator: BaseAuthenticator = InMemoryAuthenticator()
    for worker in workers:
        authenticator.add(worker)
    return authenticator


def create_pika_producer() -> PikaProducer:
    """Create a dedicated pika producer.

    Returns:
        PikaProducer: dedicated pika producer
    """
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
    return pika_producer


def setup_sensor(lift_id: str, pika_producer: PikaProducer) -> None:
    """Setup sensor."""
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