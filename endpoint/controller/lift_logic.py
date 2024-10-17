import random
from model.lift_state import LiftState
from datetime import datetime
from communication.rabbitmq_client import RabbitMQClient

class LiftSeat:
    def __init__(self, capacity, index):
        self.capacity = capacity
        self.passengers = 0
        self.position = index / 30  # Evenly space seats

# TODO - Implement the Erlang-C model to calculate the probability of passengers waiting for the lift
class LiftSimulator:
    def __init__(self, lift):
        self.lift = lift
        self.seats = [LiftSeat(4, i) for i in range(30)]  # 30 seats, each with 4-person capacity
        self.rabbitmq_client = RabbitMQClient()

    def update(self, dt):
        if self.lift.get_state() != LiftState.STOP:
            speed = 0.05 if self.lift.get_state() == LiftState.FULL_STEAM else 0.025
            for seat in self.seats:
                seat.position += speed * dt
                if seat.position >= 1:
                    seat.position -= 1
                    # Passengers depart at high elevation
                    seat.passengers = 0
                elif 0.49 <= seat.position < 0.51:
                    # Passengers board at low elevation
                    seat.passengers = random.randint(0, seat.capacity)

    def set_state(self, state):
        if self.lift.get_state() != state:
            self.lift.set_state(state)
            self.send_state_update()

    def send_state_update(self):
        message = {
            'lift_id': self.lift.lift_id,
            'state': self.lift.get_state().value,
            'timestamp': datetime.now().isoformat()
        }
        self.rabbitmq_client.send_message('lift_state_updates', message)

    def close(self):
        self.rabbitmq_client.close()
