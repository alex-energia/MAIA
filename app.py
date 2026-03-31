from flask import Flask, render_template, request, jsonify
from proyectos import proyectos_bp, init_db
from maia_core_fisico import analizar_drone
from maia_validator import MaiaValidator
from core.maia_software_generator import generar_software_completo

import os
import time
import zipfile
import json
import sys
import threading

print("🔥 MAIA ULTRA STARTING...")

app = Flask(__name__, template_folder="templates")
app.secret_key = "maia_ultra"

# 🔥 ANTI CACHE
@app.after_request
def add_header(response):
    response.cache_control.no_store = True
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

# INIT
init_db()
app.register_blueprint(proyectos_bp)

estado_maia = {"progreso": 0, "estado": "IDLE", "mensaje": ""}
resultado_global = {}

# =========================
# UTILIDADES
# =========================
def generar_archivo(ruta, contenido):
    try:
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(contenido)
    except Exception as e:
        print("ERROR generando archivo:", e)

# =========================
# MODELO 3D
# =========================
def generar_modelo_3d(base, peso):
    try:
        path = os.path.join(base, "models")
        os.makedirs(path, exist_ok=True)

        escala = max(1, peso / 3)

        partes = {
            "frame.obj": f"o frame\nv {-escala} 0 {-escala}\nv {escala} 0 {-escala}\nv {escala} 0 {escala}\nv {-escala} 0 {escala}",
            "arm_x.obj": f"o arm\nv {-escala} 0 0\nv {escala} 0 0",
            "arm_z.obj": f"o arm\nv 0 0 {-escala}\nv 0 0 {escala}",
        }

        for n, c in partes.items():
            generar_archivo(os.path.join(path, n), c)

        return {
            "componentes": list(partes.keys()),
            "escala": escala
        }

    except Exception as e:
        print("ERROR modelo 3D:", e)
        return {}

# =========================
# ZIP
# =========================
def exportar_zip(ruta):
    try:
        if not os.path.exists(ruta):
            return ""

        zip_path = ruta + ".zip"

        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for root, dirs, files in os.walk(ruta):
                for file in files:
                    full = os.path.join(root, file)
                    zipf.write(full, os.path.relpath(full, ruta))

        return zip_path

    except Exception as e:
        print("ERROR ZIP:", e)
        return ""

# =========================
# CORE
# =========================
class MaiaCore:
    def ejecutar_paso(self, idea, paso, data):
        try:
            print(f"➡️ Paso {paso}")

            if paso == 0:
                core = analizar_drone(idea)
                return {"paso": 1, "data": {"core": core}}

            elif paso == 1:
                analisis = data.get("core", {}).get("analisis", {})
                peso = analisis.get("peso", 1)
                factor = max(1, peso / 5)

                data["analisis_pro"] = {
                    **analisis,
                    "estructura": "Fibra de carbono",
                    "nivel_autonomia": "Alto" if factor > 2 else "Medio",
                    "carga_util_kg": round(peso * 0.3 * factor, 2)
                }

                return {"paso": 2, "data": data}

            elif paso == 2:
                validacion = MaiaValidator().validar(data.get("core", {}))
                data["validacion"] = validacion
                return {"paso": 3, "data": data}

            elif paso == 3:
                base = f"maia_projects/{int(time.time())}"
                os.makedirs(base, exist_ok=True)
                data["base"] = base
                return {"paso": 4, "data": data}

            elif paso == 4:
                peso = data.get("analisis_pro", {}).get("peso", 1)
                data["modelos_3d"] = generar_modelo_3d(data["base"], peso)
                return {"paso": 5, "data": data}

            elif paso == 5:
                data["zip"] = exportar_zip(data["base"])
                return {"paso": 6, "data": data}

            elif paso == 6:
                return {"final": True, "resultado": data}

        except Exception as e:
            print("ERROR paso:", e)
            return {"error": str(e)}

# =========================
# 🔥 MOTOR EN SEGUNDO PLANO
# =========================
def ejecutar_maia_background(idea):
    global estado_maia, resultado_global

    estado_maia["progreso"] = 0
    estado_maia["mensaje"] = "Iniciando..."

    core = MaiaCore()
    paso = 0
    data = {}

    while True:
        res = core.ejecutar_paso(idea, paso, data)

        if "error" in res:
            estado_maia["mensaje"] = "Error"
            resultado_global = res
            break

        if res.get("final"):
            estado_maia["progreso"] = 100
            estado_maia["mensaje"] = "Completado"
            resultado_global = res["resultado"]
            break

        paso = res.get("paso", paso + 1)
        data = res.get("data", {})

        estado_maia["progreso"] += 15
        estado_maia["mensaje"] = f"Paso {paso}..."

        time.sleep(0.5)

# =========================
# ENDPOINTS
# =========================
@app.route("/evaluar_drone", methods=["POST"])
def evaluar_drone():
    try:
        req = request.get_json() or {}
        idea = req.get("idea", "")

        hilo = threading.Thread(target=ejecutar_maia_background, args=(idea,))
        hilo.start()

        return jsonify({"ok": True})

    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/maia_progreso")
def maia_progreso():
    return jsonify(estado_maia)

@app.route("/maia_resultado")
def maia_resultado():
    return jsonify(resultado_global)

@app.route("/maia_step", methods=["POST"])
def maia_step():
    try:
        req = request.get_json() or {}
        idea = req.get("idea", "")
        paso = int(req.get("paso", 0))
        data = req.get("data", {})

        core = MaiaCore()
        resultado = core.ejecutar_paso(idea, paso, data)

        return jsonify(resultado)

    except Exception as e:
        print("ERROR /maia_step:", e)
        return jsonify({"error": str(e)})

# =========================
# VISTAS
# =========================
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
    app.run(host="0.0.0.0", port=port)