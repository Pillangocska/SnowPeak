import math
from typing import Dict


class ErlangCModel:
    def __init__(self, arrival_rate, line_speed, carrier_capacity,
                 carrier_spacing, carriers_loading,
                 start_lat, start_lon, start_elevation,
                 end_lat, end_lon, end_elevation,
                 efficiency_factor: float = 0.7,
                 min_loading_time: float = 0.5):
        """
        Initialize ski lift queue model.

        Args:
            arrival_rate: Skiers per hour
            line_speed: Meters per second
            carrier_capacity: Seats per carrier
            carrier_spacing: Meters between carriers
            carriers_loading: Number of carriers that can load simultaneously
            start_lat: Starting latitude
            start_lon: Starting longitude
            start_elevation: Starting elevation in meters
            end_lat: Ending latitude
            end_lon: Ending longitude
            end_elevation: Ending elevation in meters
            efficiency_factor: Real-world efficiency factor (0.0 to 1.0)
            min_loading_time: Minimum time needed to load a carrier (in minutes)
        """
        self.arrival_rate = arrival_rate
        self.line_speed = line_speed
        self.carrier_capacity = carrier_capacity
        self.carrier_spacing = carrier_spacing
        self.carriers_loading = carriers_loading
        self.efficiency_factor = efficiency_factor
        self.min_loading_time = min_loading_time

        # Calculate slope length from coordinates and elevation
        self.slope_length = self._calculate_slope_length(
            start_lat, start_lon, start_elevation,
            end_lat, end_lon, end_elevation
        )

        # Calculate derived parameters
        self._line_speed_hour = self.line_speed * 3600
        self._total_carriers = math.floor(self.slope_length / self.carrier_spacing)
        self._calculate_service_parameters()

    def _calculate_service_parameters(self):
        """Calculate service rate considering all carriers in the system"""
        # Time for one complete circuit (up and down)
        self._cycle_time = (self.slope_length / self._line_speed_hour) * 2

        # Add minimum loading time to cycle time (convert to hours)
        self._cycle_time += (self.min_loading_time / 60)

        # How many circuits each carrier makes per hour
        circuits_per_hour = 1 / self._cycle_time

        # Total system capacity per hour (all carriers)
        system_capacity = (self._total_carriers * self.carrier_capacity * circuits_per_hour)

        # Apply efficiency factor to account for real-world conditions
        system_capacity *= self.efficiency_factor

        # Effective service rate per loading point
        self._service_rate = system_capacity / self.carriers_loading

        # Calculate system utilization
        self._utilization = self.arrival_rate / (self.carriers_loading * self._service_rate)

    def _factorial(self, n: int) -> float:
        if n > 170:  # Python's factorial limit?
            return float('inf')
        return math.factorial(n)

    def calculate_erlang_c(self) -> float:
        """
        Calculate the Erlang C probability (probability of waiting).

        Returns:
            float: Probability of waiting (between 0 and 1)
        """
        if self._utilization >= 1:
            return 1.0  # System is overloaded

        c = self.carriers_loading
        a = self.arrival_rate / self._service_rate

        # Calculate sum for denominator
        sum_term = 0
        for n in range(c):
            sum_term += (a ** n) / self._factorial(n)

        term1 = (a ** c) / self._factorial(c)
        term2 = 1 / (1 - self._utilization)

        return (term1 * term2) / (sum_term + (term1 * term2))

    def calculate_wait_time(self) -> Dict[str, float]:
        """
        Calculate expected waiting time statistics.

        Returns:
            Dict containing:
            - average_wait: Average wait time in minutes
            - max_wait: 95th percentile wait time in minutes
            - system_utilization: Percentage of system capacity being used
        """
        if self._utilization >= 1:
            return {
                'average_wait': float('inf'),
                'max_wait': float('inf'),
                'system_utilization': self._utilization * 100
            }

        pc = self.calculate_erlang_c()

        # Average wait time in minutes (including minimum loading time)
        base_wait = (pc / (self.carriers_loading * self._service_rate - self.arrival_rate)) * 60
        average_wait = base_wait + (self.min_loading_time * pc)

        # 95th percentile wait time
        max_wait = -math.log(0.05) * average_wait

        return {
            'average_wait': average_wait,
            'max_wait': max_wait,
            'system_utilization': self._utilization * 100
        }

    def calculate_queue_length(self) -> Dict[str, float]:
        """
        Calculate queue length statistics.

        Returns:
            Dict containing:
            - average_length: Average number of people in queue
            - max_length: 95th percentile queue length
            - space_needed: Estimated space needed for queue (meters²)
        """
        wait_times = self.calculate_wait_time()

        if math.isinf(wait_times['average_wait']):
            return {
                'average_length': float('inf'),
                'max_length': float('inf'),
                'space_needed': float('inf')
            }

        # Convert wait time back to hours for calculation
        average_wait_hours = wait_times['average_wait'] / 60
        average_length = self.arrival_rate * average_wait_hours

        # 95th percentile queue length
        max_length = self.arrival_rate * (wait_times['max_wait'] / 60)

        # Estimate space needed (assuming 1m² per person)
        space_needed = max_length * 1.0

        return {
            'average_length': average_length,
            'max_length': max_length,
            'space_needed': space_needed
        }

    def get_performance_metrics(self) -> Dict[str, float]:
        """
        Performance metrics for the lift queuing system.

        Returns:
            Dict containing all relevant performance metrics including
            wait times, queue lengths, and system utilization.
        """
        wait_metrics = self.calculate_wait_time()
        queue_metrics = self.calculate_queue_length()
        waiting_time = math.ceil(wait_metrics['average_wait'])

        return {
            **wait_metrics,
            **queue_metrics,
            'waiting_time [min]': waiting_time,
            'total_carriers': self._total_carriers,
            'cycle_time [min]': self._cycle_time * 60,
            'service_rate_per_loading_point': self._service_rate,
            'total_service_capacity': self._service_rate * self.carriers_loading,
            'theoretical_max_capacity': (self._line_speed_hour / self.carrier_spacing) * self.carrier_capacity,
            'effective_capacity': (self._line_speed_hour / self.carrier_spacing) * self.carrier_capacity * self.efficiency_factor
        }

    def _calculate_slope_length(
        self,
        start_lat: float,
        start_lon: float,
        start_elevation: float,
        end_lat: float,
        end_lon: float,
        end_elevation: float
    ) -> float:
        """
        Calculate the actual slope length considering both horizontal and vertical distance.

        Args:
            start_lat: Starting latitude
            start_lon: Starting longitude
            start_elevation: Starting elevation in meters
            end_lat: Ending latitude
            end_lon: Ending longitude
            end_elevation: Ending elevation in meters

        Returns:
            float: Slope length in meters
        """
        # Convert lat/lon to meters, approximate using equirectangular projection
        R = 6371000  # Earth's radius in meters
        x = math.radians(end_lon - start_lon) * math.cos(math.radians((start_lat + end_lat) / 2))
        y = math.radians(end_lat - start_lat)

        horizontal_distance = R * math.sqrt(x*x + y*y)
        vertical_distance = end_elevation - start_elevation

        # Calculate true length using Pythagorean theorem
        return math.sqrt(horizontal_distance**2 + vertical_distance**2)
