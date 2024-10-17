from sensor.base_sensor import BaseSensor
import numpy as np

class TemperatureSensor(BaseSensor):
    def __init__(self, lift_id, sensor_type, location, mean_temp, amplitude, rabbitmq_client):
        super().__init__(lift_id, sensor_type, location, rabbitmq_client)
        self.mean_temp = mean_temp
        self.amplitude = amplitude

    def generate_temperature(self, num_points):
        x = np.linspace(0, 2*np.pi, num_points)
        smooth_temp = self.mean_temp + self.amplitude * np.sin(x - np.pi/2)
        noise = np.random.normal(0, 0.05, num_points)
        offset = np.random.uniform(-0.1, 0.1)
        return smooth_temp + noise + offset

    def apply_wind_chill(self, temp, wind_speed):
        return temp - 0.1 * wind_speed
