from datetime import datetime, timedelta
from typing import List, Tuple

import numpy as np

from ski_lift.core.sensor.factory.base_sensor import BaseSensor


class TemperatureSensor(BaseSensor):
    """Temperature sensor implementation.

    This class implements a temperature sensor that generates realistic temperature
    data using a sinusoidal pattern with added noise. It simulates daily temperature
    variations and includes wind chill effects when combined with wind speed data.

    The sensor generates temperatures around a mean value with a specified amplitude
    of variation. Random noise and offset are added to make the data more realistic.
    The wind chill effect can be applied to the generated temperatures based on
    wind speed readings.
    """
    def __init__(self, lift_id: str, location: str, mean_temp: float, amplitude: float):
        super().__init__(lift_id, 'sensor.temperature', location)
        self.mean_temp = mean_temp
        self.amplitude = amplitude

    def generate_data(self, num_points: int) -> Tuple[List[float], List[datetime]]:
        x = np.linspace(0, 2*np.pi, num_points)
        smooth_temp = self.mean_temp + self.amplitude * np.sin(x - np.pi/2)
        noise = np.random.normal(0, 0.05, num_points)
        offset = np.random.uniform(-0.1, 0.1)
        temperatures = smooth_temp + noise + offset

        now = datetime.now()
        timestamps = [now + timedelta(minutes=5*i) for i in range(num_points)]

        return temperatures.tolist(), timestamps

    def apply_wind_chill(self, temp: float, wind_speed: float) -> float:
        return temp - 0.1 * wind_speed
