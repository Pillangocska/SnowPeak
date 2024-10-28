from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from ski_lift.core.sensor.factory.base_sensor import SensorReading

# This is our base Observer interface
class SensorObserver(ABC):
    """Base interface for all sensor data handlers.

    Any class that wants to do something with sensor data should implement this interface.
    Examples could be:
    - Saving to a database
    - Sending to RabbitMQ
    - Writing to a file
    - Displaying on a dashboard
    """
    @abstractmethod
    def update(self, reading: SensorReading) -> None:
        pass
