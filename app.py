from flask import Flask, render_template, request, jsonify, send_file
from proyectos import proyectos_bp, init_db
from maia_core_fisico import analizar_drone
from maia_validator import MaiaValidator
from core.maia_software_generator import generar_software_completo
from core.maia_hardware_generator import generar_hardware  # 🔥 NUEVO

import os, json, time, threading, subprocess, zipfile, re, sys

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

    software = generar_software_completo(tipo)

    for ruta_relativa, contenido in software["codigo"].items():
        generar_archivo(os.path.join(base, ruta_relativa), contenido)

    generar_archivo(
        os.path.join(base, "config/config.json"),
        json.dumps(software["config"], indent=4)
    )

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
            # =========================
            # CAPA 1
            # =========================
            self.progreso(20, "Analizando idea...")
            core_data = analizar_drone(idea)

            analisis = core_data.get("analisis", {})
            fisica = core_data.get("fisica", {})

            # 🔥 ANALISIS PRO
            analisis_pro = {
                "tipo": analisis.get("tipo"),
                "peso": analisis.get("peso"),
                "mision": "Operación autónoma en entorno real",
                "complejidad": "Media-Alta",
                "riesgos": [
                    "Fallo de batería",
                    "Pérdida de señal",
                    "Condiciones climáticas"
                ]
            }

            # =========================
            # CAPA 2
            # =========================
            self.progreso(50, "Validando...")
            validator = MaiaValidator()
            validacion = validator.validar(core_data)

            # 🔥 FISICA PRO
            empuje = fisica.get("empuje", 0)
            peso = analisis.get("peso", 1)

            fisica_pro = {
                "autonomia": fisica.get("autonomia"),
                "consumo": fisica.get("consumo"),
                "empuje": empuje,
                "empuje_minimo": peso * 9.81 * 2,
                "relacion_empuje_peso": round(empuje / (peso * 9.81 + 1), 2),
                "eficiencia": "Alta" if empuje > peso * 9.81 else "Baja"
            }

            # 🔥 DIAGNOSTICO PRO
            if validacion["viabilidad"] == "VIABLE ✅":
                diagnostico = f"""
Sistema viable desde el punto de vista aerodinámico.

- Relación empuje/peso adecuada
- Autonomía suficiente
- Consumo eficiente

El sistema puede operar en condiciones reales con estabilidad alta.
"""
            else:
                diagnostico = f"""
Sistema NO viable.

Problemas:
{chr(10).join(validacion["errores"])}

Requiere rediseño estructural y optimización energética.
"""

            # 🔥 SOLUCIONES PRO
            soluciones_pro = validacion["soluciones"] + [
                "Optimizar relación peso/empuje",
                "Usar baterías de mayor densidad energética",
                "Mejorar control PID",
                "Incorporar sensores redundantes"
            ]

            # =========================
            # CAPA 3
            # =========================
            self.progreso(75, "Generando sistema completo...")

            ruta, software = crear_proyecto(
                f"drone_{int(time.time())}",
                analisis.get("peso", 5),
                analisis.get("tipo", "general")
            )

            salida = ejecutar_main(ruta)
            zip_path = exportar_zip(ruta)

            # 🔥 HARDWARE PRO REAL
            hardware = generar_hardware(analisis, fisica)

            self.progreso(100, "Completado")

            resultado_global = {
                "viabilidad": validacion["viabilidad"],
                "analisis": analisis_pro,
                "fisica": fisica_pro,
                "diagnostico": diagnostico,
                "errores": validacion["errores"],
                "soluciones": soluciones_pro,
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
        "fase": 18,
        "capacidades": [
            "Ingeniería autónoma completa",
            "Generación de software real",
            "Diagnóstico profesional",
            "Simulación ejecutable",
            "Modelo 3D",
            "Hardware inteligente dinámico"
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
