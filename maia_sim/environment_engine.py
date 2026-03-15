import random

class EnvironmentEngine:

    def __init__(self):

        self.wind_speed = random.uniform(0,10)
        self.wind_direction = random.uniform(0,360)

        self.water_current = random.uniform(0,3)

        self.temperature = random.uniform(-10,40)

    def update(self):

        self.wind_speed += random.uniform(-0.2,0.2)

        return {
            "wind_speed": self.wind_speed,
            "wind_direction": self.wind_direction,
            "water_current": self.water_current,
            "temperature": self.temperature
        }