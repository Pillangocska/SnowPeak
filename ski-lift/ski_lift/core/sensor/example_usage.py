from ski_lift.core.sensor.observer.print_observer import PrintObserver
from ski_lift.core.sensor.observer.rabbitmq_observer import RabbitMQObserver
from ski_lift.core.sensor.sensor_data_generator import SensorDataGenerator

sensor_config = {
        'base_temperature': {'mean_temp': -5, 'amplitude': 3},
        'peak_temperature': {'mean_temp': -15, 'amplitude': 3},
        'base_wind': {'base_speed': 12, 'randomness': 1.5},
        'peak_wind': {'base_speed': 20, 'randomness': 2}
    }

generator = SensorDataGenerator('lift_1', sensor_config)

print_observer = PrintObserver()
for sensor in generator.sensors.values():
    sensor.attach(print_observer)

try:
    generator.generate_continuous_data(interval_seconds=15)
except KeyboardInterrupt:
    print("Stopping sensor data generation...")

# And if we want to use RabbitMQ just simply inside the for loop
# sensor.attach(rabbitmq_observer)
# For this we need to create it first before the loop:
# rabbitmq_client = RabbitMQClient()
# rabbitmq_observer = RabbitMQObserver(rabbitmq_client)
