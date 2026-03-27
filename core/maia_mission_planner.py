def analizar_mision(idea: str):

    idea = idea.lower()

    mision = {
        "tipo": "general",
        "prioridad": [],
        "sensores_extra": [],
        "modo_vuelo": [],
        "perfil": {}
    }

    if "incendio" in idea or "rescate" in idea:
        mision["tipo"] = "rescate"
        mision["prioridad"] = ["autonomia", "estabilidad"]
        mision["sensores_extra"] = ["Cámara térmica", "Sensor de gas"]
        mision["modo_vuelo"] = ["Auto", "RTL", "Loiter"]

    elif "carrera" in idea or "fpv" in idea:
        mision["tipo"] = "carreras"
        mision["prioridad"] = ["velocidad", "respuesta"]
        mision["sensores_extra"] = ["Cámara FPV HD"]
        mision["modo_vuelo"] = ["Acro", "Manual"]

    elif "carga" in idea:
        mision["tipo"] = "carga"
        mision["prioridad"] = ["empuje", "estabilidad"]
        mision["sensores_extra"] = ["Sensor de peso"]
        mision["modo_vuelo"] = ["Stabilize", "Auto"]

    elif "agricola" in idea:
        mision["tipo"] = "agricola"
        mision["prioridad"] = ["autonomia", "cobertura"]
        mision["sensores_extra"] = ["Sensor multiespectral"]
        mision["modo_vuelo"] = ["Auto", "Waypoint"]

    else:
        mision["tipo"] = "general"
        mision["prioridad"] = ["balance"]
        mision["sensores_extra"] = []
        mision["modo_vuelo"] = ["Stabilize"]

    return mision
