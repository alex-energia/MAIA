# ==============================
# COSTOS DETALLADOS MAIA
# ==============================

def desglose_capex(capex_total):

    capex = {

        "Ingenieria": {
            "Ingenieria conceptual": capex_total * 0.03,
            "Ingenieria basica": capex_total * 0.04,
            "Ingenieria de detalle": capex_total * 0.05
        },

        "Equipos": {
            "Equipos principales": capex_total * 0.35,
            "Equipos auxiliares": capex_total * 0.10,
            "Instrumentacion y control": capex_total * 0.05
        },

        "Procura": {
            "Compra de equipos": capex_total * 0.08,
            "Logistica": capex_total * 0.03,
            "Importacion": capex_total * 0.02
        },

        "Construccion": {
            "Obras civiles": capex_total * 0.10,
            "Montaje mecanico": capex_total * 0.07,
            "Montaje electrico": capex_total * 0.04
        },

        "Gestion proyecto": {
            "Project management": capex_total * 0.02,
            "Supervision": capex_total * 0.01,
            "Control calidad": capex_total * 0.01
        },

        "Permisos": {
            "Licencias": capex_total * 0.01,
            "Estudios regulatorios": capex_total * 0.01
        },

        "Contingencia": {
            "Reserva tecnica": capex_total * 0.03
        }

    }

    return capex


# ==============================
# OPEX DETALLADO
# ==============================

def desglose_opex(opex_total):

    opex = {

        "Operacion": {
            "Personal operativo": opex_total * 0.35,
            "Energia auxiliar": opex_total * 0.10,
            "Consumibles": opex_total * 0.08
        },

        "Mantenimiento": {
            "Mantenimiento preventivo": opex_total * 0.15,
            "Mantenimiento correctivo": opex_total * 0.10,
            "Repuestos": opex_total * 0.05
        },

        "Administracion": {
            "Personal administrativo": opex_total * 0.07,
            "Sistemas": opex_total * 0.03,
            "Seguros": opex_total * 0.02
        },

        "Logistica": {
            "Transporte": opex_total * 0.03,
            "Almacenamiento": opex_total * 0.01
        },

        "Regulacion": {
            "Cumplimiento ambiental": opex_total * 0.01
        }

    }

    return opex