def generar_hardware(analisis, fisica):

    peso = analisis.get("peso", 5)

    # 🔥 Selección inteligente según peso
    if peso < 2:
        motor = "2205 2300KV"
        bateria = "LiPo 3S 2200mAh"
        helice = "5x4"
    elif peso < 5:
        motor = "2212 920KV"
        bateria = "LiPo 4S 5200mAh"
        helice = "10x4.5"
    else:
        motor = "3508 700KV"
        bateria = "LiPo 6S 10000mAh"
        helice = "15x5"

    hardware = {
        "componentes": {
            "motores": motor,
            "helices": helice,
            "esc": "40A BLHeli",
            "bateria": bateria,
            "controlador": "Pixhawk 2.4.8",
            "frame": "Fibra de carbono"
        },
        "sensores": [
            "MPU6050 (IMU)",
            "Neo-6M (GPS)",
            "Lidar Lite v3",
            "Cámara FPV"
        ],
        "conexionado": [
            "ESC1 → PWM1",
            "ESC2 → PWM2",
            "ESC3 → PWM3",
            "ESC4 → PWM4",
            "GPS → UART2",
            "IMU → I2C",
            "Lidar → I2C"
        ]
    }

    return hardware