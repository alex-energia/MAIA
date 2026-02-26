class MAIA:

    def __init__(self):
        self.mode = "activo"
        self.modules = {
            "energia": True,
            "finanzas": True
        }

    def cambiar_modo(self, nuevo_modo):
        self.mode = nuevo_modo
        return f"Modo cambiado a {self.mode}"

    def estado(self):
        return {
            "modo": self.mode,
            "modulos_activos": self.modules
        }

    def analizar(self, texto):
        if "energia" in texto.lower():
            return "Módulo Energía listo para análisis."
        elif "finanza" in texto.lower():
            return "Módulo Finanzas listo para análisis."
        else:
            return "Consulta recibida. MAIA procesando..."