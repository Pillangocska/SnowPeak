import time
from datetime import datetime, timedelta
from sensor.temperature_sensor import TemperatureSensor
from sensor.wind_sensor import WindSensor
from communication.rabbitmq_client import RabbitMQClient
import pandas as pd

class SensorDataGenerator:
    def __init__(self, lift_id):
        self.lift_id = lift_id
        self.base_elevation = 800
        self.peak_elevation = 3000
        self.rabbitmq_client = RabbitMQClient()

        # init sensors
        self.base_temp_sensor = TemperatureSensor(lift_id,'sensor.temperature', 'base', mean_temp=-5, amplitude=3, rabbitmq_client=self.rabbitmq_client)
        self.peak_temp_sensor = TemperatureSensor(lift_id, 'sensor.temperature', 'peak', mean_temp=-15, amplitude=3, rabbitmq_client=self.rabbitmq_client)
        self.base_wind_sensor = WindSensor(lift_id, 'sensor.wind', 'base', base_speed=12, randomness=1.5, rabbitmq_client=self.rabbitmq_client)
        self.peak_wind_sensor = WindSensor(lift_id, 'sensor.wind', 'peak', base_speed=20, randomness=2, rabbitmq_client=self.rabbitmq_client)

    def generate_day_data(self):
        date = datetime.now()
        timestamps = pd.date_range(start=date, end=date + timedelta(days=1), freq='5min')[:-1]
        num_points = len(timestamps)

        base_temp = self.base_temp_sensor.generate_temperature(num_points)
        peak_temp = self.peak_temp_sensor.generate_temperature(num_points)
        base_wind = self.base_wind_sensor.generate_wind_speed(num_points)
        peak_wind = self.peak_wind_sensor.generate_wind_speed(num_points)

        base_temp = self.base_temp_sensor.apply_wind_chill(base_temp, base_wind)
        peak_temp = self.peak_temp_sensor.apply_wind_chill(peak_temp, peak_wind)

        return timestamps, base_temp, peak_temp, base_wind, peak_wind

    def send_sensor_data(self):
        timestamps, base_temp, peak_temp, base_wind, peak_wind = self.generate_day_data()

        for i, timestamp in enumerate(timestamps):
            # send temperature data
            self.base_temp_sensor.send_data(base_temp[i], timestamp)
            self.peak_temp_sensor.send_data(peak_temp[i], timestamp)

            # send wind data
            self.base_wind_sensor.send_data(base_wind[i], timestamp)
            self.peak_wind_sensor.send_data(peak_wind[i], timestamp)

            # (5 second = 5 minutes in simulation)
            time.sleep(5)
