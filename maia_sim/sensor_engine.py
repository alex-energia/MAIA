import random

class SensorEngine:

    def read_sensors(self, drone):

        gps = {
            "lat": drone.lat + random.uniform(-0.00001,0.00001),
            "lon": drone.lon + random.uniform(-0.00001,0.00001),
            "alt": drone.alt
        }

        radar = {
            "objetos_detectados": random.randint(0,5)
        }

        camera = {
            "imagen": "frame_simulado"
        }

        return {
            "gps": gps,
            "radar": radar,
            "camera": camera
        }