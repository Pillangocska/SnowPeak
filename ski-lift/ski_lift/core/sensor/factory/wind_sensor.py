from scipy.signal import savgol_filter
from datetime import datetime, timedelta
from typing import List, Tuple
import numpy as np
from ski_lift.core.sensor.factory.base_sensor import BaseSensor

class WindSensor(BaseSensor):
    """Wind sensor implementation.

    This class implements a wind sensor that generates realistic wind speed data
    with features like gusts, slow variations, and smoothing. It uses statistical
    methods to create natural-looking wind patterns that include both sustained
    winds and sudden gusts.

    The sensor generates wind speeds around a base speed with random variations
    and occasional gusts. The data is smoothed using a Savitzky-Golay filter
    to create more realistic transitions between values. The implementation
    ensures that wind speeds remain within realistic bounds and maintain the
    specified base speed on average.
    """
    def __init__(self, lift_id: str, location: str, base_speed: float, randomness: float):
        super().__init__(lift_id, 'sensor.wind', location)
        self.base_speed = base_speed
        self.randomness = randomness

    def generate_data(self, num_points: int) -> Tuple[List[float], List[datetime]]:
        if num_points == 1:
            # Special case for single point generation
            wind_speed = np.array([self.base_speed + np.random.normal(0, self.randomness)])
            # Add possible gust
            if np.random.random() < 0.05:  # 5% chance of gust
                wind_speed += np.random.uniform(2, 5)
            wind_speed = np.clip(wind_speed, 0, 30)
        else:
            # Original implementation for multiple points
            wind_speed = np.cumsum(np.random.normal(0, self.randomness, num_points))
            slow_variation = 5 * np.sin(np.linspace(0, 4*np.pi, num_points))
            wind_speed += slow_variation

            gust_probability = 0.05
            gusts = np.random.choice([0, 1], size=num_points, p=[1-gust_probability, gust_probability])
            gust_strength = np.random.uniform(2, 5, num_points)
            wind_speed += gusts * gust_strength

            wind_speed = np.clip(wind_speed, 0, 30)
            wind_speed += self.base_speed - np.mean(wind_speed)

            # Only apply Savitzky-Golay filter when we have enough points
            if num_points >= 31:
                wind_speed = savgol_filter(wind_speed, window_length=31, polyorder=3)

        now = datetime.now()
        timestamps = [now + timedelta(minutes=5*i) for i in range(num_points)]

        return wind_speed.tolist(), timestamps
