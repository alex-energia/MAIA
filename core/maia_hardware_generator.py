def generar_hardware(analisis, fisica, mision=None):

    peso = analisis.get("peso", 5)
    tipo = analisis.get("tipo", "general")
    tipo_mision = (mision or {}).get("tipo", "general")

    # =========================
    # 🔥 SELECCIÓN BASE (TU LÓGICA)
    # =========================
    if peso < 2:
        motor_modelo = "2205 2300KV"
        kv = 2300
        bateria = {"tipo": "LiPo", "celdas": "3S", "capacidad": "2200mAh", "voltaje": 11.1}
        helice = "5x4"
        corriente_motor = 20

    elif peso < 5:
        motor_modelo = "2212 920KV"
        kv = 920
        bateria = {"tipo": "LiPo", "celdas": "4S", "capacidad": "5200mAh", "voltaje": 14.8}
        helice = "10x4.5"
        corriente_motor = 25

    else:
        motor_modelo = "3508 700KV"
        kv = 700
        bateria = {"tipo": "LiPo", "celdas": "6S", "capacidad": "10000mAh", "voltaje": 22.2}
        helice = "15x5"
        corriente_motor = 35

    # =========================
    # 🔥 AJUSTES POR MISIÓN (NUEVO 🔥)
    # =========================
    sensores_extra = []

    if tipo_mision == "rescate":
        sensores_extra = ["Cámara térmica FLIR", "Sensor de gas MQ-2"]
        bateria["capacidad"] = "12000mAh"

    elif tipo_mision == "carreras":
        motor_modelo = "2306 2600KV"
        kv = 2600
        helice = "5x4.3"
        bateria = {"tipo": "LiPo", "celdas": "4S", "capacidad": "1500mAh", "voltaje": 14.8}
        corriente_motor = 35
        sensores_extra = ["Cámara FPV HD", "VTX 5.8GHz"]

    elif tipo_mision == "carga":
        motor_modelo = "4114 400KV"
        kv = 400
        helice = "18x5.5"
        bateria["capacidad"] = "16000mAh"
        corriente_motor = 45
        sensores_extra = ["Sensor de peso", "Sensor corriente/voltaje"]

    elif tipo_mision == "agricola":
        sensores_extra = ["Sensor multiespectral", "Sensor humedad"]
        bateria["capacidad"] = "14000mAh"

    # =========================
    # 🔥 CÁLCULOS REALES (TU BASE)
    # =========================
    num_motores = 4

    empuje_total = peso * 9.81 * 2
    empuje_por_motor = empuje_total / num_motores

    consumo_total = corriente_motor * num_motores
    potencia_total = consumo_total * bateria["voltaje"]

    capacidad_ah = float(bateria["capacidad"].replace("mAh", "")) / 1000
    autonomia_min = round((capacidad_ah / consumo_total) * 60, 2)

    # =========================
    # 🔥 HARDWARE PRO FINAL
    # =========================
    hardware = {

        "motores": {
            "modelo": motor_modelo,
            "kv": kv,
            "cantidad": num_motores,
            "helice": helice,
            "empuje_por_motor_N": round(empuje_por_motor, 2)
        },

        "esc": {
            "corriente": f"{corriente_motor + 10}A",
            "tipo": "BLHeli_S",
            "compatibilidad": bateria["celdas"]
        },

        "bateria": bateria,

        "controlador": {
            "modelo": "Pixhawk 2.4.8",
            "firmware": ["PX4", "Ardupilot"],
            "modos": ["Stabilize", "Loiter", "Auto", "RTL"]
        },

        "frame": {
            "material": "Fibra de carbono",
            "tamano": "450mm" if peso < 5 else "680mm"
        },

        "sensores": [
            "MPU6050 (IMU)",
            "Neo-6M (GPS)",
            "Lidar Lite v3",
            "Cámara FPV"
        ] + sensores_extra,

        "conectividad": {
            "radio_control": "2.4GHz",
            "telemetria": "915MHz",
            "video": "5.8GHz FPV"
        },

        "conexionado": [
            "Batería → ESC",
            "ESC → Motores",
            "ESC → Controlador (PWM)",
            "GPS → UART",
            "IMU → I2C",
            "Telemetría → UART"
        ],

        # =========================
        # 🔥 NIVEL GLI REAL
        # =========================
        "analisis_electrico": {
            "corriente_total_A": consumo_total,
            "potencia_total_W": potencia_total,
            "autonomia_estimada_min": autonomia_min
        },

        "alertas": [
            "Verificar disipación térmica en ESC",
            "No descargar batería por debajo de 3.3V por celda",
            "Asegurar calibración de IMU antes de vuelo"
        ],

        # 🔥 NUEVO NIVEL PRO
        "mision": tipo_mision
    }

    return hardware
