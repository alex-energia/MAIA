# =========================
# MAVLINK HÍBRIDO (REAL + SIMULADO)
# =========================

import json
import time

try:
    from pymavlink import mavutil
    MAVLINK_ACTIVO = True
except:
    MAVLINK_ACTIVO = False


class MAVLinkDrone:

    def __init__(self, connection_string="udp:127.0.0.1:14550"):

        self.simulado = not MAVLINK_ACTIVO

        if self.simulado:
            print("⚠️ MAVLink no disponible → usando modo SIMULADO")
            self.estado = {
                "armado": False,
                "modo": "STANDBY",
                "posicion": [0, 0, 0]
            }
            self.master = None
            return

        try:
            self.master = mavutil.mavlink_connection(connection_string)
            self.master.wait_heartbeat()
            print("✅ MAVLink REAL conectado")
        except Exception as e:
            print("⚠️ Error MAVLink, usando SIMULADO:", e)
            self.simulado = True
            self.estado = {
                "armado": False,
                "modo": "STANDBY",
                "posicion": [0, 0, 0]
            }

    # =========================
    # ARMADO
    # =========================
    def armar(self):
        if self.simulado:
            self.estado["armado"] = True
            self.estado["modo"] = "ARMED"
            print("🟢 [SIM] Drone armado")
        elif self.master:
            self.master.arducopter_arm()

    # =========================
    # DESPEGUE
    # =========================
    def despegar(self, alt=10):
        if self.simulado:
            if not self.estado["armado"]:
                print("⚠️ [SIM] No armado")
                return
            self.estado["modo"] = "TAKEOFF"
            self.estado["posicion"][2] = alt
            print(f"🚀 [SIM] Despegando a {alt}m")
        elif self.master:
            self.master.mav.command_long_send(
                self.master.target_system,
                self.master.target_component,
                mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
                0, 0, 0, 0, 0, 0, 0, alt
            )

    # =========================
    # MOVIMIENTO
    # =========================
    def enviar_posicion(self, x, y, z):
        if self.simulado:
            self.estado["modo"] = "GUIDED"
            self.estado["posicion"] = [x, y, z]
            print(f"📍 [SIM] Moviendo a {x},{y},{z}")
        elif self.master:
            self.master.mav.set_position_target_local_ned_send(
                0,
                self.master.target_system,
                self.master.target_component,
                mavutil.mavlink.MAV_FRAME_LOCAL_NED,
                int(0b110111111000),
                x, y, -z,
                0, 0, 0,
                0, 0, 0,
                0, 0
            )

    # =========================
    # ATERRIZAJE
    # =========================
    def aterrizar(self):
        if self.simulado:
            self.estado["modo"] = "LAND"
            self.estado["posicion"][2] = 0
            print("🛬 [SIM] Aterrizando")
        elif self.master:
            self.master.mav.command_long_send(
                self.master.target_system,
                self.master.target_component,
                mavutil.mavlink.MAV_CMD_NAV_LAND,
                0, 0, 0, 0, 0, 0, 0, 0
            )

    # =========================
    # TELEMETRÍA
    # =========================
    def obtener_estado(self):
        if self.simulado:
            return self.estado
        return {"modo": "REAL"}

    def enviar_telemetria(self):
        if self.simulado:
            return json.dumps({
                "x": self.estado["posicion"][0],
                "y": self.estado["posicion"][1],
                "z": self.estado["posicion"][2],
                "modo": self.estado["modo"]
            })
        return "{}"