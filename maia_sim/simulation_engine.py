import random

class Drone:

    def __init__(self, drone_id):

        self.id = drone_id
        self.lat = 4.5709
        self.lon = -74.2973
        self.alt = 100
        self.speed = 0.00005

    def move(self):

        self.lat += random.uniform(-self.speed, self.speed)
        self.lon += random.uniform(-self.speed, self.speed)

    def telemetry(self):

        return {
            "id": self.id,
            "lat": self.lat,
            "lon": self.lon,
            "alt": self.alt
        }


class SimulationEngine:

    def __init__(self):

        self.drones = []

        self.create_default_drones()

    def create_default_drones(self):

        for i in range(3):

            drone = Drone(i+1)

            self.drones.append(drone)

    def update(self):

        data = []

        for drone in self.drones:

            drone.move()

            data.append(drone.telemetry())

        return data


sim_engine = SimulationEngine()