from flask import Flask, render_template, request, jsonify
from proyectos import proyectos_bp, init_db
from maia_core_fisico import analizar_drone
from maia_validator import MaiaValidator

import os
import time
import zipfile
import json

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

# =========================
# UTILIDADES
# =========================
def generar_archivo(ruta, contenido):
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(contenido)

def generar_modelo_3d(base, peso):
    path = os.path.join(base, "models")
    os.makedirs(path, exist_ok=True)

    escala = max(1, peso / 3)

    partes = {
        "frame.obj": f"o frame\nv {-escala} 0 {-escala}\nv {escala} 0 {-escala}\nv {escala} 0 {escala}\nv {-escala} 0 {escala}",
    }

    for n, c in partes.items():
        generar_archivo(os.path.join(path, n), c)

    return {"escala": escala}

def exportar_zip(ruta):
    if not os.path.exists(ruta):
        return ""

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

    def ejecutar_paso(self, idea, paso, data):
        try:
            if paso == 0:
                core = analizar_drone(idea)
                return {"paso": 1, "data": {"core": core}}

            elif paso == 1:
                analisis = data.get("core", {}).get("analisis", {})
                data["analisis_pro"] = analisis
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
                modelos = generar_modelo_3d(data["base"], 1)
                data["modelos_3d"] = modelos
                return {"paso": 5, "data": data}

            elif paso == 5:
                data["zip"] = exportar_zip(data["base"])
                return {"paso": 6, "data": data}

            elif paso == 6:
                return {"final": True, "resultado": data}

        except Exception as e:
            print("ERROR:", e)
            return {"error": str(e)}

# =========================
# ENDPOINT
# =========================
@app.route("/maia_step", methods=["POST"])
def maia_step():
    req = request.get_json() or {}
    idea = req.get("idea", "")
    paso = int(req.get("paso", 0))
    data = req.get("data", {})

    core = MaiaCore()
    return jsonify(core.ejecutar_paso(idea, paso, data))

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