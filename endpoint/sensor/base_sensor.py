class BaseSensor:
    def __init__(self, lift_id, sensor_type, location, rabbitmq_client):
        self.lift_id = lift_id
        self.sensor_type = sensor_type
        self.location = location
        self.rabbitmq_client = rabbitmq_client

    def send_data(self, value, timestamp):
        self.rabbitmq_client.send_message(self.sensor_type, {
            'lift_id': self.lift_id,
            'location': self.location,
            'value': float(value),
            'timestamp': str(timestamp)
        })
