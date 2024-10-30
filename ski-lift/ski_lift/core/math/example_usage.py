from ski_lift.core.math.erlang_c import ErlangCModel

model = ErlangCModel(
    start_lat=45.5,
    start_lon=-73.5,
    start_elevation=1200,
    end_lat=45.52,
    end_lon=-73.48,
    end_elevation=2200,
    arrival_rate=1000,          # avg. skiers per hour
    line_speed=4,               # meters per second
    carrier_capacity=4,         # seats per carrier
    carrier_spacing=15,         # meters between carriers
    carriers_loading=1          # number of carriers loading simultaneously
)

metrics = model.get_performance_metrics()

print("System Performance Metrics:")
for key, value in metrics.items():
    if isinstance(value, float):
        print(f"{key}: {value:.2f}")
    else:
        print(f"{key}: {value}")
