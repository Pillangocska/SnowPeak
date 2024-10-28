from ski_lift.core.sensor.observer.sensor_observer import SensorObserver
from ski_lift.core.sensor.factory.base_sensor import SensorReading

class PrintObserver(SensorObserver):
    """Simply prints sensor readings to console."""
    def update(self, reading: SensorReading) -> None:
        print(f"New reading from {reading.location}: {reading.value}°C at {reading.timestamp}")
