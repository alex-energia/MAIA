from flask import Flask, render_template, request, jsonify
from proyectos import proyectos_bp, init_db
from maia_core_fisico import analizar_drone
from maia_validator import MaiaValidator
from core.maia_software_generator import generar_software_completo

import os, time, threading, subprocess, zipfile, sys

print("🔥 MAIA ULTRA STARTING...")

app = Flask(__name__, template_folder="templates")
app.secret_key = "maia_ultra"

init_db()
app.register_blueprint(proyectos_bp)

estado_maia = {"progreso": 0, "estado": "IDLE", "mensaje": ""}
resultado_global = {}

# =========================
# UTILIDAD
# =========================
def generar_archivo(ruta, contenido):
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(contenido)

# =========================
# 🔥 MODELO 3D REAL
# =========================
def generar_modelo_3d(base, peso):

    path = os.path.join(base, "models")
    os.makedirs(path, exist_ok=True)

    escala = max(1, peso / 3)

    partes = {
        "frame.obj": f"""
o frame
v {-escala} 0 {-escala}
v {escala} 0 {-escala}
v {escala} 0 {escala}
v {-escala} 0 {escala}
""",

        "arm_x.obj": f"""
o arm_x
v {-escala} 0 0
v {escala} 0 0
""",

        "arm_z.obj": f"""
o arm_z
v 0 0 {-escala}
v 0 0 {escala}
""",

        "motor_1.obj": f"o motor\nv {escala} 0 {escala}",
        "motor_2.obj": f"o motor\nv {-escala} 0 {escala}",
        "motor_3.obj": f"o motor\nv {escala} 0 {-escala}",
        "motor_4.obj": f"o motor\nv {-escala} 0 {-escala}",

        "payload.obj": f"""
o payload
v 0 0 0
v {escala/2} {escala/2} {escala/2}
"""
    }

    for nombre, contenido in partes.items():
        generar_archivo(os.path.join(path, nombre), contenido)

    return {
        "componentes": list(partes.keys()),
        "escala": escala,
        "detalle": "Modelo estructural quadcopter realista"
    }

# =========================
# EJECUCIÓN
# =========================
def ejecutar_main(ruta):
    try:
        main_path = os.path.join(ruta, "main.py")

        if not os.path.exists(main_path):
            return "###DATA_START###\n[{\"modo\":\"fallback\"}]\n###DATA_END###"

        proceso = subprocess.Popen(
            [sys.executable, "main.py"],
            cwd=ruta,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        salida = ""
        start = time.time()

        while True:
            if proceso.poll() is not None:
                break
            if time.time() - start > 25:
                proceso.kill()
                break
            time.sleep(0.05)

        stdout, stderr = proceso.communicate()
        salida += stdout

        if stderr:
            salida += "\nERROR:\n" + stderr

        if "###DATA_START###" not in salida:
            salida += "\n###DATA_START###\n[{\"modo\":\"fallback\"}]\n###DATA_END###"

        return salida

    except Exception as e:
        return f"###DATA_START###\n[{{\"error\":\"{str(e)}\"}}]\n###DATA_END###"

# =========================
# ZIP
# =========================
def exportar_zip(ruta):
    zip_path = ruta + ".zip"
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for root, dirs, files in os.walk(ruta):
            for file in files:
                full = os.path.join(root, file)
                zipf.write(full, os.path.relpath(full, ruta))
    return zip_path

# =========================
# CORE
# =========================
class MaiaCore:

    def progreso(self, val, msg):
        estado_maia["progreso"] = val
        estado_maia["mensaje"] = msg
        estado_maia["estado"] = "PROCESANDO"
        time.sleep(0.1)

    def ejecutar(self, idea):

        global resultado_global

        try:
            self.progreso(10, "Analizando...")

            core = analizar_drone(idea)
            analisis = core.get("analisis", {})
            fisica = core.get("fisica", {})

            peso = analisis.get("peso", 1)
            empuje = fisica.get("empuje", 0)

            # 🔥 ESCALA REAL
            factor = max(1, peso / 5)

            # =========================
            # ANALISIS
            # =========================
            analisis_pro = {
                **analisis,
                "estructura": "Fibra de carbono",
                "nivel_autonomia": "Alto" if factor > 2 else "Medio",
                "carga_util_kg": round(peso * 0.3 * factor, 2)
            }

            # =========================
            # FISICA REAL
            # =========================
            consumo_estimado = round(peso * 120 * factor, 2)

            fisica_pro = {
                **fisica,
                "relacion_empuje_peso": round(empuje/(peso*9.81+1),2),
                "consumo_w": consumo_estimado,
                "autonomia_estimada_min": round((10000 / consumo_estimado) * 60, 2),
                "rendimiento": "Óptimo" if factor > 2 else "Limitado"
            }

            self.progreso(40, "Validando...")

            validator = MaiaValidator()
            validacion = validator.validar(core)

            self.progreso(65, "Construyendo sistema...")

            nombre = f"drone_{int(time.time())}"
            base = f"maia_projects/{nombre}"
            os.makedirs(base, exist_ok=True)

            # =========================
            # SOFTWARE REAL
            # =========================
            software_gen = generar_software_completo(
                analisis.get("tipo","general")
            )

            for ruta, codigo in software_gen.get("codigo", {}).items():
                generar_archivo(os.path.join(base, ruta), codigo)

            software_pro = {
                "nivel": "Industrial",
                "arquitectura": "Modular distribuida",
                "modulos": []
            }

            for ruta, codigo in software_gen.get("codigo", {}).items():

                nombre_mod = ruta.split("/")[-1].replace(".py","")

                software_pro["modulos"].append({
                    "nombre": nombre_mod,
                    "categoria": ruta.split("/")[0],
                    "archivo": ruta,
                    "codigo": codigo[:4000]
                })

            # =========================
            # 3D
            # =========================
            modelos = generar_modelo_3d(base, peso)

            salida = ejecutar_main(base)
            zip_path = exportar_zip(base)

            # =========================
            # 🔥 HARDWARE REAL
            # =========================
            thrust_needed = peso * 9.81 * 2
            motor_thrust = round(thrust_needed / 4, 2)

            hardware_pro = {
                "estructura": {
                    "material": "Fibra de carbono",
                    "frame": f"{650 + int(factor*150)}mm",
                    "peso_estructura_kg": round(peso * 0.25,2)
                },
                "propulsion": {
                    "motores": f"{motor_thrust}N thrust x4",
                    "helices": f"{15 + int(factor)} pulgadas",
                    "esc": f"{40 + int(factor*15)}A"
                },
                "energia": {
                    "bateria": f"{6 + int(factor)}S {10000 + int(factor*4000)}mAh",
                    "consumo_estimado_w": consumo_estimado
                },
                "control": {
                    "flight_controller": "Pixhawk / PX4",
                    "redundancia": "IMU dual + GPS dual" if factor > 2 else "Básica"
                },
                "capacidades": [
                    "Vuelo autónomo",
                    "RTL",
                    "Failsafe activo",
                    "Navegación inteligente"
                ]
            }

            self.progreso(100, "Completado")

            resultado_global = {
                "viabilidad": validacion.get("viabilidad","N/A"),
                "analisis": analisis_pro,
                "fisica": fisica_pro,
                "hardware": hardware_pro,
                "software": software_pro,
                "validacion": validacion,
                "modelos_3d": modelos,
                "salida": salida,
                "zip": zip_path
            }

            estado_maia["estado"] = "COMPLETADO"

        except Exception as e:
            resultado_global = {"error": str(e)}
            estado_maia["estado"] = "ERROR"

# =========================
# THREAD
# =========================
def proceso_maia(idea):
    MaiaCore().ejecutar(idea)

# =========================
# ENDPOINTS
# =========================
@app.route("/evaluar_drone", methods=["POST"])
def evaluar_drone():
    data = request.get_json() or {}
    idea = data.get("idea","")

    estado_maia["progreso"] = 0
    estado_maia["estado"] = "PROCESANDO"

    threading.Thread(
        target=proceso_maia,
        args=(idea,),
        daemon=True
    ).start()

    return jsonify({"ok": True})

@app.route("/maia_progreso")
def maia_progreso():
    return jsonify(estado_maia)

@app.route("/maia_resultado")
def maia_resultado():
    return jsonify(resultado_global)

@app.route("/maia_invent")
def maia_invent():
    return render_template("maia_invent.html")

@app.route("/")
def home():
    return render_template("index.html")

# =========================
# RUN
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, threaded=True)