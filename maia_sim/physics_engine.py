class PhysicsEngine:

    def apply_physics(self, drone, environment):

        viento = environment["wind_speed"]

        drone.lat += viento * 0.000001
        drone.lon += viento * 0.000001

        if drone.alt < 0:
            drone.alt = 0