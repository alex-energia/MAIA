from flask import Flask, render_template, request, jsonify, send_file
from proyectos import proyectos_bp, init_db
from maia_core_fisico import analizar_drone
from maia_validator import MaiaValidator
from core.maia_software_generator import generar_software_completo

import os
import json
import time
import threading
import subprocess
import zipfile
import re
import sys

print("🔥 MAIA STARTING...")

# =========================
# APP
# =========================
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
# 🧊 MOTOR 3D
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

    generar_archivo(f"{model_path}/drone.obj", obj)
    generar_archivo(f"{model_path}/drone.stl", stl)

# =========================
# 🧠 CREAR PROYECTO REAL
# =========================
def crear_proyecto(nombre, peso, tipo="general"):
    nombre = nombre_seguro(nombre)
    base = f"maia_projects/{nombre}"

    os.makedirs(base, exist_ok=True)

    # 🔥 GENERAR SOFTWARE COMPLETO
    software = generar_software_completo(tipo)

    # 🔥 CREAR ARCHIVOS REALES
    for ruta_relativa, contenido in software["codigo"].items():
        ruta_completa = os.path.join(base, ruta_relativa)
        generar_archivo(ruta_completa, contenido)

    # 🔥 CONFIG
    generar_archivo(
        os.path.join(base, "config/config.json"),
        json.dumps(software["config"], indent=4)
    )

    # 🔥 MODELO 3D
    generar_modelo_3d(base, peso)

    return base, software

# =========================
# EJECUCIÓN
# =========================
def ejecutar_main(ruta):
    try:
        main_path = os.path.join(ruta, "main.py")

        if not os.path.exists(main_path):
            return "⚠️ main.py no encontrado"

        result = subprocess.run(
            [sys.executable, "main.py"],
            cwd=ruta,
            capture_output=True,
            text=True,
            timeout=5
        )

        return result.stdout or result.stderr

    except Exception as e:
        return str(e)

def exportar_zip(ruta):
    zip_path = ruta + ".zip"

    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for root, _, files in os.walk(ruta):
            for file in files:
                full = os.path.join(root, file)
                zipf.write(full, os.path.relpath(full, ruta))

    return zip_path

# =========================
# 🧠 CORE MAIA
# =========================
class MaiaCore:

    def progreso(self, val, msg):
        estado_maia["progreso"] = val
        estado_maia["mensaje"] = msg
        estado_maia["estado"] = "PROCESANDO"
        time.sleep(1)

    def ejecutar(self, idea):
        global resultado_global

        try:
            # CAPA 1
            self.progreso(20, "Analizando idea...")
            core_data = analizar_drone(idea)

            analisis = core_data.get("analisis", {})
            fisica = core_data.get("fisica", {})

            # CAPA 2
            self.progreso(50, "Validando...")
            validator = MaiaValidator()
            validacion = validator.validar(core_data)

            # 🔥 EXPLICACIÓN PROFESIONAL
            if validacion["viabilidad"] == "VIABLE ✅":
                explicacion = (
                    f"El sistema es viable. Empuje: {fisica.get('empuje')} N, "
                    f"Autonomía: {fisica.get('autonomia')} min. "
                    f"La relación empuje/peso es adecuada para vuelo estable."
                )
            else:
                explicacion = (
                    "Sistema NO viable por:\n"
                    + "\n".join(validacion["errores"])
                    + "\nSoluciones:\n"
                    + "\n".join(validacion["soluciones"])
                )

            # CAPA 3
            self.progreso(75, "Generando sistema completo...")

            ruta, software = crear_proyecto(
                f"drone_{int(time.time())}",
                analisis.get("peso", 5),
                analisis.get("tipo", "general")
            )

            salida = ejecutar_main(ruta)
            zip_path = exportar_zip(ruta)

            # 🔥 HARDWARE REAL
            hardware = [
                "Motores brushless KV adecuados",
                "ESC 30A–60A",
                "Batería LiPo 3S/4S",
                "Controlador Pixhawk",
                "GPS + IMU",
                "Frame de fibra de carbono"
            ]

            self.progreso(100, "Completado")

            resultado_global = {
                "viabilidad": validacion["viabilidad"],
                "explicacion": explicacion,
                "analisis": analisis,
                "fisica": fisica,
                "errores": validacion["errores"],
                "soluciones": validacion["soluciones"],
                "software": software,
                "hardware": hardware,
                "modelo_3d": f"{ruta}/models/drone.obj",
                "salida": salida,
                "software_generado": ruta,
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
    estado_maia["mensaje"] = "Iniciando..."
    estado_maia["estado"] = "PROCESANDO"

    threading.Thread(target=proceso_maia, args=(idea,), daemon=True).start()

    return jsonify({"status": "ok"})

@app.route("/maia_progreso")
def maia_progreso():
    return jsonify(estado_maia)

@app.route("/maia_resultado")
def maia_resultado():
    return jsonify(resultado_global)

@app.route("/maia_capacidades")
def maia_capacidades():
    return jsonify({
        "fase": 17,
        "capacidades": [
            "Generación de software real",
            "Arquitectura modular tipo PX4",
            "Drivers de sensores",
            "IA de decisión",
            "Modelo 3D automático",
            "Validación física",
            "Proyecto descargable"
        ]
    })

@app.route("/descargar_proyecto")
def descargar_proyecto():
    zip_path = resultado_global.get("zip")

    if zip_path and os.path.exists(zip_path):
        return send_file(zip_path, as_attachment=True)

    return "No disponible", 404

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
