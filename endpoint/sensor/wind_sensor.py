from sensor.base_sensor import BaseSensor
import numpy as np
from scipy.signal import savgol_filter

class WindSensor(BaseSensor):
    def __init__(self, lift_id, sensor_type, location, base_speed, randomness, rabbitmq_client):
        super().__init__(lift_id, sensor_type, location, rabbitmq_client)
        self.base_speed = base_speed
        self.randomness = randomness

    def generate_wind_speed(self, num_points):
        wind_speed = np.cumsum(np.random.normal(0, self.randomness, num_points))
        slow_variation = 5 * np.sin(np.linspace(0, 4*np.pi, num_points))
        wind_speed += slow_variation
        gust_probability = 0.05
        gusts = np.random.choice([0, 1], size=num_points, p=[1-gust_probability, gust_probability])
        gust_strength = np.random.uniform(2, 5, num_points)
        wind_speed += gusts * gust_strength
        wind_speed = np.clip(wind_speed, 0, 30)
        wind_speed += self.base_speed - np.mean(wind_speed)
        wind_speed = savgol_filter(wind_speed, window_length=31, polyorder=3)
        return wind_speed
