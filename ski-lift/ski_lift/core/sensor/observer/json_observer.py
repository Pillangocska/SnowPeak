import json

from ski_lift.core.sensor.factory.base_sensor import SensorReading
from ski_lift.core.sensor.observer.sensor_observer import SensorObserver


class JsonFileObserver(SensorObserver):
    """Saves sensor readings to a JSON file."""
    def __init__(self, filename: str):
        self.filename = filename

    def update(self, reading: SensorReading) -> None:
        with open(self.filename, 'a') as f:
            json.dump({
                'lift_id': reading.lift_id,
                'location': reading.location,
                'value': reading.value,
                'timestamp': str(reading.timestamp)
            }, f)
            f.write('\n')
