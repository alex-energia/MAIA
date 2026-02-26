class AnalizadorFinanciero:

    def __init__(self):
        pass

    def calcular_van(self, inversion, flujos, tasa_descuento):
        van = -inversion
        for i, flujo in enumerate(flujos):
            van += flujo / ((1 + tasa_descuento) ** (i + 1))
        return van

    def calcular_tir(self, inversion, flujos, precision=0.0001):
        tasa = 0.1
        while True:
            van = -inversion
            for i, flujo in enumerate(flujos):
                van += flujo / ((1 + tasa) ** (i + 1))
            if abs(van) < precision:
                return tasa
            tasa += 0.0001