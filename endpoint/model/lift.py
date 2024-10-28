import hashlib
from model.lift_state import LiftState

class Lift:
    SECRET_KEY = "pika.pikazdsfgewuztr8to8rgif87732t8rgfge86f4g82g732gf8zg2eizfgozgfzewro8t326tr32tr"

    def __init__(self, start_lat, start_lon, start_elevation, end_lat, end_lon, end_elevation, num_seats):
        self.start_lat = start_lat
        self.start_lon = start_lon
        self.start_elevation = start_elevation
        self.end_lat = end_lat
        self.end_lon = end_lon
        self.end_elevation = end_elevation
        self.num_seats = num_seats
        self.lift_id = self._generate_lift_id()
        self._state = LiftState.STOP

    def _generate_lift_id(self):
        location_string = f"{self.start_lat},{self.start_lon},{self.start_elevation},{self.end_lat},{self.end_lon},{self.end_elevation}"
        data_to_hash = f"{location_string}{self.SECRET_KEY}"
        hash_object = hashlib.sha256(data_to_hash.encode())
        full_hash = hash_object.hexdigest()
        return full_hash[:20]

    @property
    def state(self):
        return self._state

    def get_state(self):
        return self._state

    def set_state(self, new_state):
        if not isinstance(new_state, LiftState):
            raise ValueError("New state must be a LiftState enum value")
        self._state = new_state
        print(f"Lift {self.lift_id} state changed to {self._state.value}")

    def __str__(self):
        return (f"Lift {self.lift_id}: {self.num_seats}-seater, "
                f"Start: ({self.start_lat}, {self.start_lon}, {self.start_elevation}m), "
                f"End: ({self.end_lat}, {self.end_lon}, {self.end_elevation}m), "
                f"State: {self._state.value}")
