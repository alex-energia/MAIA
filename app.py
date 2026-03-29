from flask import Flask, render_template, request, jsonify, send_file
from proyectos import proyectos_bp, init_db
from maia_core_fisico import analizar_drone
from maia_validator import MaiaValidator
from core.maia_software_generator import generar_software_completo
from core.maia_hardware_generator import generar_hardware
from core.maia_mission_planner import analizar_mision

import os, json, time, threading, subprocess, zipfile, re, sys

print("🔥 MAIA STARTING...")

app = Flask(__name__, template_folder="templates")
app.secret_key = "maia_secret_ultra"

init_db()
app.register_blueprint(proyectos_bp)

estado_maia = {"progreso": 0, "estado": "IDLE", "mensaje": ""}
resultado_global = {}

# =========================
# UTILIDADES
# =========================
def nombre_seguro(nombre):
    return re.sub(r'[^a-zA-Z0-9_-]', '_', nombre)

def generar_archivo(ruta, contenido):
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(contenido)

# =========================
# MOTOR 3D (MEJORADO)
# =========================
def generar_modelo_3d(base, peso):
    model_path = os.path.join(base, "models")
    os.makedirs(model_path, exist_ok=True)

    escala = max(1, peso / 5)

    obj = f"""o Drone
v 0 0 0
v {escala} 0 0
v {escala} {escala} 0
v 0 {escala} 0
v 0 0 {escala}
v {escala} 0 {escala}
v {escala} {escala} {escala}
v 0 {escala} {escala}
f 1 2 3 4
f 5 6 7 8
"""

    stl = f"""solid drone
facet normal 0 0 0
outer loop
vertex 0 0 0
vertex {escala} 0 0
vertex {escala} {escala} 0
endloop
endfacet
endsolid drone
"""

    obj_path = f"{model_path}/drone.obj"
    stl_path = f"{model_path}/drone.stl"

    generar_archivo(obj_path, obj)
    generar_archivo(stl_path, stl)

    return {
        "obj": obj_path,
        "stl": stl_path
    }

# =========================
# PROYECTO
# =========================
def crear_proyecto(nombre, peso, tipo="general"):
    nombre = nombre_seguro(nombre)
    base = f"maia_projects/{nombre}"
    os.makedirs(base, exist_ok=True)

    software = generar_software_completo(tipo)

    for ruta_relativa, contenido in software["codigo"].items():
        generar_archivo(os.path.join(base, ruta_relativa), contenido)

    generar_archivo(
        os.path.join(base, "config/config.json"),
        json.dumps(software["config"], indent=4)
    )

    modelos = generar_modelo_3d(base, peso)

    return base, software, modelos

# =========================
# EJECUCIÓN
# =========================
def ejecutar_main(ruta):
    try:
        result = subprocess.run(
            [sys.executable, "main.py"],
            cwd=ruta,
            capture_output=True,
            text=True,
            timeout=120
        )

        salida = result.stdout.strip()
        if not salida:
            salida = "⚠️ Sin salida"

        if "###DATA_START###" not in salida:
            salida += "\n\n###DATA_START###\n[{\"error\":\"sin telemetria\"}]\n###DATA_END###"

        return salida

    except subprocess.TimeoutExpired:
        return "⏱️ Timeout\n###DATA_START###\n[{\"error\":\"timeout_controlado\"}]\n###DATA_END###"

# =========================
# ZIP
# =========================
def exportar_zip(ruta):
    zip_path = ruta + ".zip"
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for root, _, files in os.walk(ruta):
            for file in files:
                full = os.path.join(root, file)
                zipf.write(full, os.path.relpath(full, ruta))
    return zip_path

# =========================
# CORE MAIA PRO
# =========================
class MaiaCore:

    def progreso(self, val, msg):
        estado_maia["progreso"] = val
        estado_maia["mensaje"] = msg
        estado_maia["estado"] = "PROCESANDO"
        time.sleep(0.2)

    def ejecutar(self, idea):
        global resultado_global

        try:
            self.progreso(10, "Analizando idea...")
            core_data = analizar_drone(idea)

            analisis = core_data.get("analisis", {})
            fisica = core_data.get("fisica", {})

            peso = analisis.get("peso", 1)
            empuje = fisica.get("empuje", 0)

            # =========================
            # 🔥 ANALISIS PRO
            # =========================
            analisis_pro = {
                "tipo": analisis.get("tipo"),
                "peso": peso,
                "configuracion": "Quadcopter X",
                "carga_util_kg": round(peso * 0.3, 2),
                "material": "Fibra de carbono",
                "resistencia_viento_kmh": 45,
                "temperatura_operativa": "-10°C a 45°C",
                "perfil_mision": "Emergencia / Incendios / Rescate",
                "riesgos": [
                    "Sobrecalentamiento de ESC",
                    "Fallo de GPS en zonas densas",
                    "Viento extremo",
                    "Interferencia RF",
                    "Saturación de sensores"
                ]
            }

            # =========================
            # 🔥 FISICA PRO
            # =========================
            energia = fisica.get("consumo", 1000) * (fisica.get("autonomia", 10) / 60)

            fisica_pro = {
                "empuje_total_N": empuje,
                "empuje_minimo_N": peso * 9.81 * 2,
                "relacion_empuje_peso": round(empuje / (peso * 9.81 + 1), 2),
                "energia_total_Wh": round(energia, 2),
                "eficiencia": "Alta" if empuje > peso * 9.81 else "Baja",
                "estabilidad": "Óptima" if empuje > peso * 12 else "Media"
            }

            self.progreso(40, "Validando...")
            validator = MaiaValidator()
            validacion = validator.validar(core_data)

            self.progreso(70, "Generando sistema...")
            ruta, software, modelos = crear_proyecto(
                f"drone_{int(time.time())}",
                peso,
                analisis.get("tipo", "general")
            )

            salida = ejecutar_main(ruta)
            zip_path = exportar_zip(ruta)

            hardware = generar_hardware(analisis, fisica)

            # =========================
            # 🔥 SOFTWARE NIVEL BRUTAL
            # =========================
            software_pro = {
                "nivel": "Autopiloto avanzado",
                "arquitectura": [
                    "Control PID",
                    "Navegación autónoma",
                    "IA de decisión",
                    "Failsafe inteligente",
                    "Comunicación MAVLink"
                ],
                "capacidades": [
                    "Evasión de obstáculos",
                    "Vuelo autónomo",
                    "Optimización energética",
                    "Telemetría en tiempo real",
                    "Integración con simuladores"
                ]
            }

            self.progreso(100, "Completado")

            resultado_global = {
                "viabilidad": validacion["viabilidad"],
                "analisis": analisis_pro,
                "fisica": fisica_pro,
                "riesgos": analisis_pro["riesgos"],
                "software": software_pro,
                "modelos_3d": modelos,
                "hardware": hardware,
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
    data = request.get_json(silent=True) or {}
    idea = data.get("idea", "")

    estado_maia["progreso"] = 0
    estado_maia["estado"] = "PROCESANDO"

    threading.Thread(target=proceso_maia, args=(idea,), daemon=True).start()

    return jsonify({"status": "ok"})

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