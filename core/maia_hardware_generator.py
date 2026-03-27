def generar_hardware(analisis, fisica):

    peso = analisis.get("peso", 5)
    tipo = analisis.get("tipo", "general")

    # =========================
    # 🔥 SELECCIÓN BASE (TU LÓGICA MEJORADA)
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
    # 🔥 CÁLCULOS REALES
    # =========================
    num_motores = 4
    empuje_total = peso * 9.81 * 2
    empuje_por_motor = empuje_total / num_motores

    consumo_total = corriente_motor * num_motores
    potencia_total = consumo_total * bateria["voltaje"]

    capacidad_ah = float(bateria["capacidad"].replace("mAh", "")) / 1000
    autonomia_min = round((capacidad_ah / consumo_total) * 60, 2)

    # =========================
    # 🔥 HARDWARE PRO
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
            "compatibilidad": f"{bateria['celdas']}"
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
        ],

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
        # 🔥 NIVEL GLI / INGENIERÍA REAL
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
        ]
    }

    return hardware