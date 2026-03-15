import importlib

class AlgorithmEngine:

    def ejecutar(self, nombre_algoritmo, drone):

        try:

            modulo = importlib.import_module(
                f"maia_sim.algorithms.{nombre_algoritmo}"
            )

            modulo.run(drone)

        except Exception as e:

            print("Error algoritmo:", e)