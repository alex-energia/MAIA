class EnergyEngine:

    def update(self, drone):

        consumo = 0.05 + abs(drone.speed)

        drone.energy -= consumo

        if drone.energy < 0:
            drone.energy = 0