import time
from datetime import datetime, timedelta
from typing import Any, Dict, List

from ski_lift.core.sensor.factory.sensor_factory import SensorFactory


class SensorDataGenerator:
    """Main class for generating synchronized sensor data.

    This class coordinates the generation of data from multiple sensors for a
    single ski lift. It manages both temperature and wind sensors at different
    locations (base and peak) and ensures their data is generated in a
    synchronized way.
    """
    def __init__(self, lift_id: str, sensor_config: Dict[str, Dict[str, Any]]):
        self.lift_id = lift_id
        factory = SensorFactory()

        self.sensors = {
            'base_temp': factory.create_temperature_sensor(
                lift_id, 'base', sensor_config['base_temperature']
            ),
            'peak_temp': factory.create_temperature_sensor(
                lift_id, 'peak', sensor_config['peak_temperature']
            ),
            'base_wind': factory.create_wind_sensor(
                lift_id, 'base', sensor_config['base_wind']
            ),
            'peak_wind': factory.create_wind_sensor(
                lift_id, 'peak', sensor_config['peak_wind']
            )
        }

    def generate_single_reading(self) -> None:
        """Generate a single reading from each sensor."""
        # Generate one data point from each sensor
        base_temp, base_temp_times = self.sensors['base_temp'].generate_data(1)
        peak_temp, peak_temp_times = self.sensors['peak_temp'].generate_data(1)
        base_wind, base_wind_times = self.sensors['base_wind'].generate_data(1)
        peak_wind, peak_wind_times = self.sensors['peak_wind'].generate_data(1)

        # Apply wind chill to temperatures
        base_temp[0] = self.sensors['base_temp'].apply_wind_chill(base_temp[0], base_wind[0])
        peak_temp[0] = self.sensors['peak_temp'].apply_wind_chill(peak_temp[0], peak_wind[0])

        # Notify observers with the new readings
        self.sensors['base_temp'].notify(base_temp[0], base_temp_times[0])
        self.sensors['peak_temp'].notify(peak_temp[0], peak_temp_times[0])
        self.sensors['base_wind'].notify(base_wind[0], base_wind_times[0])
        self.sensors['peak_wind'].notify(peak_wind[0], peak_wind_times[0])

    def generate_continuous_data(self, interval_seconds: int = 5) -> None:
        """Generate continuous sensor readings at specified intervals.

        Args:
            interval_seconds (int): Number of seconds to wait between readings.
                                  Defaults to 5 seconds.
        """
        while True:
            self.generate_single_reading()  # Generate one reading per sensor
            time.sleep(interval_seconds)    # Wait for the specified interval

    def generate_day_data(self, num_points: int) -> None:
        """Generate a specific number of readings from each sensor.

        Args:
            num_points (int): Number of readings to generate per sensor.
        """
        base_temp, base_temp_times = self.sensors['base_temp'].generate_data(num_points)
        peak_temp, peak_temp_times = self.sensors['peak_temp'].generate_data(num_points)
        base_wind, base_wind_times = self.sensors['base_wind'].generate_data(num_points)
        peak_wind, peak_wind_times = self.sensors['peak_wind'].generate_data(num_points)

        base_temp = [
            self.sensors['base_temp'].apply_wind_chill(t, w)
            for t, w in zip(base_temp, base_wind)
        ]
        peak_temp = [
            self.sensors['peak_temp'].apply_wind_chill(t, w)
            for t, w in zip(peak_temp, peak_wind)
        ]

        for i in range(num_points):
            self.sensors['base_temp'].notify(base_temp[i], base_temp_times[i])
            self.sensors['peak_temp'].notify(peak_temp[i], peak_temp_times[i])
            self.sensors['base_wind'].notify(base_wind[i], base_wind_times[i])
            self.sensors['peak_wind'].notify(peak_wind[i], peak_wind_times[i])
