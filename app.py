from flask import Flask, render_template, request, jsonify
from proyectos import proyectos_bp, init_db
from maia_core_fisico import analizar_drone
from maia_validator import MaiaValidator
from core.maia_software_generator import generar_software_completo

import os, json, time, threading, subprocess, zipfile, re, sys

print("🔥 MAIA ULTRA STARTING...")

app = Flask(__name__, template_folder="templates")
app.secret_key = "maia_ultra"

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
# 🔥 MODELO 3D MEJORADO
# =========================
def generar_modelo_3d(base, peso):
    path = os.path.join(base, "models")
    os.makedirs(path, exist_ok=True)

    escala = max(1, peso / 2)

    partes = {
        "frame.obj": f"o frame\nv 0 0 0\nv {escala} 0 0\nv {escala} {escala} 0\nv 0 {escala} 0",
        "arm_1.obj": f"o arm\nv 0 0 0\nv {escala} 0 0",
        "arm_2.obj": f"o arm\nv 0 0 0\nv 0 {escala} 0",
        "payload.obj": f"o payload\nv 0 0 0\nv {escala/2} {escala/2} {escala/2}"
    }

    for nombre, contenido in partes.items():
        generar_archivo(os.path.join(path, nombre), contenido)

    return {
        "componentes": list(partes.keys()),
        "ruta": path,
        "preview": f"Drone industrial escala x{round(escala,2)}",
        "detalle": {
            "brazos": 4,
            "tipo": "quadcopter",
            "nivel": "semi-real"
        }
    }

# =========================
# EJECUCIÓN
# =========================
def ejecutar_main(ruta):
    try:
        main_path = os.path.join(ruta, "main.py")
        if not os.path.exists(main_path):
            return "###DATA_START###\n[{\"error\":\"main_missing\"}]\n###DATA_END###"

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
                salida += "\n⏱️ Corte inteligente MAIA"
                break
            time.sleep(0.05)

        stdout, stderr = proceso.communicate()
        salida += stdout

        if stderr:
            salida += "\n🔥 ERROR REAL:\n" + stderr

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
            self.progreso(10, "Analizando ingeniería...")

            core = analizar_drone(idea)
            analisis = core.get("analisis", {})
            fisica = core.get("fisica", {})

            peso = analisis.get("peso", 1)
            empuje = fisica.get("empuje", 0)

            # 🔥 ANALISIS PRO
            analisis_pro = {
                **analisis,
                "estructura": "Fibra de carbono",
                "configuracion": "Quadcopter X",
                "carga_util_kg": round(peso * 0.3, 2),
                "uso": "Agrícola / Industrial",
                "nivel_autonomia": "Alto",
                "resistencia_climatica": "Media-Alta"
            }

            # 🔥 FISICA PRO
            fisica_pro = {
                **fisica,
                "relacion_empuje_peso": round(empuje/(peso*9.81+1),2),
                "consumo_por_min": round(fisica.get("consumo",0)/60,2),
                "rendimiento": "Óptimo" if empuje > peso*9.81 else "Limitado"
            }

            self.progreso(40, "Validando...")

            validator = MaiaValidator()
            validacion = validator.validar(core)

            self.progreso(65, "Generando sistema...")

            nombre = f"drone_{int(time.time())}"
            base = f"maia_projects/{nombre}"
            os.makedirs(base, exist_ok=True)

            software_base = generar_software_completo(
                analisis.get("tipo","general")
            )

            for r, c in software_base["codigo"].items():
                generar_archivo(os.path.join(base, r), c)

            # init modules
            for root, dirs, files in os.walk(base):
                init_file = os.path.join(root, "__init__.py")
                if not os.path.exists(init_file):
                    open(init_file, "w").close()

            modelos = generar_modelo_3d(base, peso)

            salida = ejecutar_main(base)
            zip_path = exportar_zip(base)

            # 🔥 HARDWARE PRO
            hardware_pro = {
                "estructura": "Fibra de carbono",
                "frame": "650mm",
                "motores": "3508 700KV x4",
                "helices": "15x5",
                "esc": "40A BLHeli",
                "bateria": "LiPo 6S 10000mAh",
                "controlador": "Pixhawk",
                "sensores": ["GPS", "IMU", "Lidar", "FPV"],
                "extras": ["RTK opcional", "Cámara HD"]
            }

            # 🔥 SOFTWARE PRO (YA NO BÁSICO)
            software_pro = {
                "nivel": "Industrial",
                "arquitectura": "Modular distribuida",
                "modulos": [
                    "Control PID adaptativo",
                    "Navegación autónoma",
                    "Evasión de obstáculos IA",
                    "Telemetría en tiempo real",
                    "Planificador de rutas",
                    "Failsafe inteligente",
                    "Gestión energética"
                ]
            }

            # 🔥 NUEVOS BLOQUES
            mision = {
                "tipo": "Riego agrícola",
                "modo": "Autónomo",
                "area_cobertura_m2": round(peso * 100, 2),
                "eficiencia": "Alta"
            }

            self.progreso(100, "Completado")

            resultado_global = {
                "viabilidad": validacion.get("viabilidad","N/A"),
                "analisis": analisis_pro,
                "fisica": fisica_pro,
                "riesgos": [
                    "Sobrecalentamiento ESC",
                    "Fallo GPS urbano",
                    "Interferencia RF",
                    "Viento extremo",
                    "Batería crítica"
                ],
                "hardware": hardware_pro,
                "software": software_pro,
                "validacion": validacion,
                "mision": mision,
                "modelos_3d": modelos,
                "salida": salida,
                "zip": zip_path,
                "idea_original": idea
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