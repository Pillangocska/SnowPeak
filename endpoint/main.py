from sensor.sensor_data_generator import SensorDataGenerator
from model.lift import Lift
from controller.lift_logic import LiftSimulator
from view.lift_view import LiftView
import threading

def generate_sensor_data(lift_id):
    data_generator = SensorDataGenerator(lift_id)
    while True:
        data_generator.send_sensor_data()

def main():
    lift = Lift(start_lat=45.5, start_lon=-73.5, start_elevation=800, end_lat=45.52, end_lon=-73.48, end_elevation=3000, num_seats=4)
    print(f"Endpoint started -> {lift}")

    # Sensor data generation in a separate thread
    sensor_thread = threading.Thread(target=generate_sensor_data, args=(lift.lift_id,))
    sensor_thread.start()

    simulator = LiftSimulator(lift)

    # Initialize view
    view = LiftView(simulator)
    view.run()

if __name__ == "__main__":
    main()
