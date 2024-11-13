from ski_lift.core.sensor.factory.base_sensor import SensorReading
from ski_lift.core.sensor.observer.sensor_observer import SensorObserver


class PrintObserver(SensorObserver):
    """Simply prints sensor readings to console."""
    def update(self, reading: SensorReading) -> None:
        print(f"New {reading.sensor_type} from {reading.location}: {reading.value} at {reading.timestamp}")
