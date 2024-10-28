"""Base implementation for ski lift sensors."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List

@dataclass
class SensorReading:
    """Data transfer object for sensor readings.

    This class encapsulates all the data associated with a single sensor reading.
    It provides a standardized format for sensor data that can be used across
    the entire system.

    Attributes:
        lift_id: Unique identifier for the ski lift
        sensor_type: Type of the sensor (e.g., 'sensor.temperature', 'sensor.wind')
        location: Location of the sensor on the lift (e.g., 'base', 'peak')
        value: The measured value from the sensor
        timestamp: When the measurement was taken
    """
    lift_id: str
    sensor_type: str
    location: str
    value: float
    timestamp: datetime

class SensorObserver(ABC):
    """Abstract base class for sensor observers.

    This class defines the interface for observer objects that want to be notified
    of new sensor readings. Observers can include message publishers, loggers,
    data stores, etc.
    """
    @abstractmethod
    def update(self, reading: SensorReading) -> None:
        pass

class BaseSensor(ABC):
    """Abstract base class for all sensor types.

    Implements the observable part of the Observer pattern. Derived sensor classes
    should implement the generate_data method according to their specific sensing
    requirements.

    Attributes:
        lift_id: Unique identifier of the ski lift
        sensor_type: Type of sensor (e.g., 'sensor.temperature', 'sensor.wind')
        location: Physical location of the sensor (e.g., 'base', 'peak')
        _observers: List of registered observers to be notified of new readings
    """
    def __init__(self, lift_id: str, sensor_type: str, location: str):
        self.lift_id = lift_id
        self.sensor_type = sensor_type
        self.location = location
        self._observers: List[SensorObserver] = []

    def attach(self, observer: SensorObserver) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: SensorObserver) -> None:
        self._observers.remove(observer)

    def notify(self, value: float, timestamp: datetime) -> None:
        reading = SensorReading(
            lift_id=self.lift_id,
            sensor_type=self.sensor_type,
            location=self.location,
            value=float(value),
            timestamp=timestamp
        )
        for observer in self._observers:
            observer.update(reading)

    @abstractmethod
    def generate_data(self, num_points: int) -> tuple[List[float], List[datetime]]:
        pass
