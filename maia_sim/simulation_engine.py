from maia_sim.environment_engine import EnvironmentEngine
from maia_sim.physics_engine import PhysicsEngine
from maia_sim.sensor_engine import SensorEngine
from maia_sim.energy_engine import EnergyEngine
from maia_sim.algorithm_engine import AlgorithmEngine


class Drone:

    def __init__(self,id):

        self.id=id

        self.lat=4.57
        self.lon=-74.29
        self.alt=100

        self.speed=0.00005

        self.energy=100


class SimulationEngine:

    def __init__(self):

        self.environment=EnvironmentEngine()

        self.physics=PhysicsEngine()

        self.sensors=SensorEngine()

        self.energy=EnergyEngine()

        self.algorithms=AlgorithmEngine()

        self.drones=[Drone(1)]

    def update(self):

        entorno=self.environment.update()

        data=[]

        for drone in self.drones:

            self.algorithms.ejecutar("ejemplo_algoritmo",drone)

            self.physics.apply_physics(drone,entorno)

            self.energy.update(drone)

            sensores=self.sensors.read_sensors(drone)

            data.append({
                "id":drone.id,
                "lat":drone.lat,
                "lon":drone.lon,
                "alt":drone.alt,
                "energia":drone.energy,
                "sensores":sensores,
                "entorno":entorno
            })

        return data


sim_engine=SimulationEngine()