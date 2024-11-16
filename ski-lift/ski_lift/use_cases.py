"""Ski lift use cases."""

import os
from threading import Thread
from typing import List

import pika

from ski_lift.app.entity import SkiLiftAuthorizer, SkiLiftController
from ski_lift.core.auth import BaseAuthenticator, InMemoryAuthenticator
from ski_lift.core.command.descriptor.serializer import (
    JSONBytesDescriptorSerializer, PrettyStringDescriptorSerializer)
from ski_lift.core.command.result.serializer import (
    JSONBytesResultSerializer, PrettyResultStringSerializer)
from ski_lift.core.controller import Controller
from ski_lift.core.engine import Engine
from ski_lift.core.math.erlang_c import ErlangCModel
from ski_lift.core.monitor.logger import (FileCommandLogger,
                                          RabbitMQCommandLogger)
from ski_lift.core.sensor import RabbitMQObserver, SensorDataGenerator
from ski_lift.core.remote import PikaConsumer, PikaProducer, RabbitMQCommunicator


def attach_loggers_to(controller: Controller, producer: PikaProducer) -> None:
    """Attach loggers to the controller.

    Args:
        controller (Controller): controller to attach to
        producer (PikaProducer): producer that is used by some loggers
    """
    attach_file_logger_to(controller)
    attach_rabbit_mq_logger_to(controller, producer)


def attach_file_logger_to(controller: Controller):
    """Attach a file logger to the given controller.

    Args:
        controller (Controller): controller to attach to.
    """
    command_logger = FileCommandLogger(PrettyStringDescriptorSerializer(), PrettyResultStringSerializer())
    command_logger.attach_to(controller)

def attach_rabbit_mq_logger_to(controller: Controller, producer: PikaProducer):
    """Attach a rabbit mq based command logger to the given controller.

    Args:
        controller (Controller): controller to attach to.
        producer (PikaProducer): _description_
    """
    rabbit_logger = RabbitMQCommandLogger(
        descriptor_serializer=JSONBytesDescriptorSerializer(),
        result_serializer=JSONBytesResultSerializer(),
        pika_producer=producer,
        lift_id=controller.lift_id,
    )
    rabbit_logger.attach_to(controller)



def create_controller(lift_id: str, producer: PikaProducer) -> Controller:
    """Create a controller with an authorizer."""
    return SkiLiftController(
        lift_id=lift_id,
        engine=Engine(),
        authorizer=SkiLiftAuthorizer(authenticator=create_authenticate_from_env()),
        remote_communicator=RabbitMQCommunicator(producer=producer),
        queue_status=create_erlang_c_model(),
    )


def create_erlang_c_model() -> ErlangCModel:
    return ErlangCModel(
        start_lat=float(os.environ.get('START_LAT', 45.5)),
        start_lon=float(os.environ.get('START_LON', 73.5)),
        start_elevation=float(os.environ.get('START_ELEVATION', 1200)),
        end_lat=float(os.environ.get('END_LAT', 45.52)),
        end_lon=float(os.environ.get('END_LON', 73.48)),
        end_elevation=float(os.environ.get('END_ELEVATION', 2200)),
        arrival_rate=float(os.environ.get('ARRIVAL_RATE', 1000)),          
        line_speed=float(os.environ.get('LINE_SPEED', 4)),
        carrier_capacity=float(os.environ.get('CARRIER_CAPACITY', 4)),
        carrier_spacing=float(os.environ.get('CARRIER_SPACING', 15)),
        carriers_loading=float(os.environ.get('CARRIERS_LOADING', 1)),
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
    return PikaProducer(
        exchange='topic_skilift',
        exchange_type='topic',
        connection_parameters=create_pika_connection_parameters(),
    )


def setup_sensor(lift_id: str, pika_producer:PikaProducer) -> None:
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


def create_pika_consumer(exchange_name: str, exchange_type: str, lift_id: str) -> PikaConsumer:
    return PikaConsumer(
        exchange=exchange_name,
        exchange_type=exchange_type,
        route_key=lift_id,
        connection_parameters=create_pika_connection_parameters(),
    )


def create_pika_connection_parameters() -> pika.ConnectionParameters:
    return pika.ConnectionParameters(
        host=os.environ.get('RABBITMQ_HOST', 'localhost'),
        port=int(os.environ.get('RABBITMQ_PORT', 5672)),
        credentials=pika.PlainCredentials(
            username=os.environ.get('RABBITMQ_USER', 'guest'),
            password=os.environ.get('RABBITMQ_PASSWORD', 'guest'),
        ),
    )