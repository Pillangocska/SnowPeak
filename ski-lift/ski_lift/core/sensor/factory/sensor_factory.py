from typing import Any, Dict

from ski_lift.core.sensor.factory.temperature_sensor import TemperatureSensor
from ski_lift.core.sensor.factory.wind_sensor import WindSensor


class SensorFactory:
    """Factory class for creating sensor instances.

    This class implements the Factory pattern for sensor creation. It centralizes
    the instantiation of different sensor types and provides a clean interface
    for creating sensors with specific configurations.

    The factory methods handle the details of sensor creation and configuration,
    making it easier to maintain consistent sensor initialization across the
    system. This approach also makes it easier to add new sensor types in the
    future without modifying existing code.
    """
    @staticmethod
    def create_temperature_sensor(lift_id: str, location: str, config: Dict[str, Any]) -> TemperatureSensor:
        return TemperatureSensor(
            lift_id=lift_id,
            location=location,
            mean_temp=config.get('mean_temp', 0),
            amplitude=config.get('amplitude', 3)
        )

    @staticmethod
    def create_wind_sensor(lift_id: str, location: str, config: Dict[str, Any]) -> WindSensor:
        return WindSensor(
            lift_id=lift_id,
            location=location,
            base_speed=config.get('base_speed', 10),
            randomness=config.get('randomness', 1.5)
        )
