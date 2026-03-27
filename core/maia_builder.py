def generar_plan_construccion(hardware, mision):

    tipo_mision = (mision or {}).get("tipo", "general")

    plan = {
        "bom": [],
        "ensamblaje": [],
        "configuracion": {},
        "pruebas": []
    }

    # =========================
    # 🔩 BOM REAL
    # =========================
    plan["bom"] = [
        f"Motores: {hardware['motores']['modelo']} x{hardware['motores']['cantidad']}",
        f"ESC: {hardware['esc']['corriente']}",
        f"Batería: {hardware['bateria']['tipo']} {hardware['bateria']['capacidad']}",
        f"Controlador: {hardware['controlador']['modelo']}",
        f"Frame: {hardware['frame']['material']}"
    ]

    # =========================
    # 🔧 ENSAMBLAJE
    # =========================
    plan["ensamblaje"] = [
        "1. Montar estructura del frame",
        "2. Instalar motores en los brazos",
        "3. Soldar ESC a la distribución de energía",
        "4. Conectar ESC al controlador (PWM)",
        "5. Instalar GPS y sensores",
        "6. Conectar batería",
        "7. Verificar polaridad y voltajes"
    ]

    # =========================
    # ⚙️ CONFIGURACIÓN
    # =========================
    plan["configuracion"] = {
        "firmware": "PX4 / Ardupilot",
        "modos": ["Stabilize", "Loiter", "RTL"],
        "calibracion": [
            "Calibrar IMU",
            "Calibrar brújula",
            "Configurar failsafe"
        ]
    }

    # =========================
    # 🧪 PRUEBAS
    # =========================
    plan["pruebas"] = [
        "Encendido sin hélices",
        "Verificar sensores en tierra",
        "Prueba de motores",
        "Hover test",
        "Prueba de misión básica"
    ]

    # =========================
    # 🔥 AJUSTES POR MISIÓN
    # =========================
    if tipo_mision == "rescate":
        plan["pruebas"].append("Prueba de cámara térmica")

    if tipo_mision == "carga":
        plan["pruebas"].append("Prueba con carga progresiva")

    return plan