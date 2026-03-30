from flask import Flask, render_template, request, jsonify
from proyectos import proyectos_bp, init_db
from maia_core_fisico import analizar_drone
from maia_validator import MaiaValidator
from core.maia_software_generator import generar_software_completo

import os, time, threading, zipfile, json, sys

print("🔥 MAIA ULTRA STARTING...")

app = Flask(__name__, template_folder="templates")
app.secret_key = "maia_ultra"

init_db()
app.register_blueprint(proyectos_bp)

estado_maia = {"progreso": 0, "estado": "IDLE", "mensaje": ""}
resultado_global = {}

# =========================
# JSON SEGURO
# =========================
def guardar_json_seguro(path, data):
    try:
        tmp = path + ".tmp"
        with open(tmp, "w") as f:
            json.dump(data, f)
        os.replace(tmp, path)
    except Exception as e:
        print("ERROR guardando JSON:", e)

# =========================
# ARCHIVOS
# =========================
def generar_archivo(ruta, contenido):
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(contenido)

# =========================
# MODELO 3D
# =========================
def generar_modelo_3d(base, peso):
    path = os.path.join(base, "models")
    os.makedirs(path, exist_ok=True)

    escala = max(1, peso / 3)

    partes = {
        "frame.obj": f"o frame\nv {-escala} 0 {-escala}\nv {escala} 0 {-escala}\nv {escala} 0 {escala}\nv {-escala} 0 {escala}",
        "arm_x.obj": f"o arm\nv {-escala} 0 0\nv {escala} 0 0",
        "arm_z.obj": f"o arm\nv 0 0 {-escala}\nv 0 0 {escala}",
        "motor_1.obj": f"o motor\nv {escala} 0 {escala}",
        "motor_2.obj": f"o motor\nv {-escala} 0 {escala}",
        "motor_3.obj": f"o motor\nv {escala} 0 {-escala}",
        "motor_4.obj": f"o motor\nv {-escala} 0 {-escala}",
    }

    for n, c in partes.items():
        generar_archivo(os.path.join(path, n), c)

    return {
        "componentes": list(partes.keys()),
        "escala": escala,
        "detalle": "Quadcopter estructural"
    }

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
# CORE MAIA
# =========================
class MaiaCore:

    def progreso(self, val, msg):
        estado_maia["progreso"] = val
        estado_maia["mensaje"] = msg
        estado_maia["estado"] = "PROCESANDO"
        guardar_json_seguro("estado.json", estado_maia)
        time.sleep(0.05)

    # 🔥 NUEVO: ejecución por pasos (para Render FREE)
    def ejecutar_paso(self, idea, paso, data):
        try:
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
                nombre = f"drone_{int(time.time())}"
                base = f"maia_projects/{nombre}"
                os.makedirs(base, exist_ok=True)

                data["base"] = base
                return {"paso": 4, "data": data}

            elif paso == 4:
                peso = data.get("analisis_pro", {}).get("peso", 1)
                modelos = generar_modelo_3d(data["base"], peso)
                data["modelos_3d"] = modelos
                return {"paso": 5, "data": data}

            elif paso == 5:
                zip_path = exportar_zip(data["base"])
                data["zip"] = zip_path
                return {"paso": 6, "data": data}

            elif paso == 6:
                return {"final": True, "resultado": data}

        except Exception as e:
            return {"error": str(e)}

    # 🔥 TU SISTEMA ORIGINAL (NO TOCADO)
    def ejecutar(self, idea):
        global resultado_global
        try:
            self.progreso(10, "Analizando...")
            core = analizar_drone(idea)

            analisis = core.get("analisis", {})
            fisica = core.get("fisica", {})

            peso = analisis.get("peso", 1)
            empuje = fisica.get("empuje", 0)
            factor = max(1, peso / 5)

            analisis_pro = {
                **analisis,
                "estructura": "Fibra de carbono",
                "nivel_autonomia": "Alto" if factor > 2 else "Medio",
                "carga_util_kg": round(peso * 0.3 * factor, 2)
            }

            consumo = round(peso * 120 * factor, 2)

            fisica_pro = {
                **fisica,
                "relacion_empuje_peso": round(empuje/(peso*9.81+1),2),
                "consumo_w": consumo,
                "autonomia_estimada_min": round((10000/consumo)*60,2)
            }

            self.progreso(40, "Validando...")
            validacion = MaiaValidator().validar(core)

            self.progreso(65, "Construyendo sistema...")

            nombre = f"drone_{int(time.time())}"
            base = f"maia_projects/{nombre}"
            os.makedirs(base, exist_ok=True)

            software_gen = generar_software_completo(
                analisis.get("tipo","general")
            )

            for ruta, codigo in software_gen.get("codigo", {}).items():
                generar_archivo(os.path.join(base, ruta), codigo)

            modelos = generar_modelo_3d(base, peso)
            zip_path = exportar_zip(base)

            self.progreso(100, "Completado")

            resultado_global = {
                "viabilidad": validacion.get("viabilidad","N/A"),
                "analisis": analisis_pro,
                "fisica": fisica_pro,
                "modelos_3d": modelos,
                "zip": zip_path
            }

            guardar_json_seguro("resultado.json", resultado_global)
            estado_maia["estado"] = "COMPLETADO"

        except Exception as e:
            print("ERROR MAIA:", e)
            resultado_global = {"error": str(e)}
            estado_maia["estado"] = "ERROR"

# =========================
# THREAD ORIGINAL (SE CONSERVA)
# =========================
def proceso_maia(idea):
    try:
        MaiaCore().ejecutar(idea)
    except Exception as e:
        print("ERROR THREAD:", e)

# =========================
# ENDPOINT ORIGINAL
# =========================
@app.route("/evaluar_drone", methods=["POST"])
def evaluar_drone():
    data = request.get_json() or {}
    idea = data.get("idea","")

    estado_maia["progreso"] = 0
    estado_maia["estado"] = "PROCESANDO"

    for f in ["estado.json", "resultado.json"]:
        try:
            os.remove(f)
        except:
            pass

    threading.Thread(
        target=proceso_maia,
        args=(idea,),
        daemon=True
    ).start()

    return jsonify({"ok": True})

# =========================
# 🔥 NUEVO ENDPOINT (CLAVE FREE)
# =========================
@app.route("/maia_step", methods=["POST"])
def maia_step():
    data = request.get_json() or {}

    idea = data.get("idea", "")
    paso = data.get("paso", 0)
    estado = data.get("data", {})

    core = MaiaCore()
    resultado = core.ejecutar_paso(idea, paso, estado)

    return jsonify(resultado)

# =========================
# PROGRESO
# =========================
@app.route("/maia_progreso")
def maia_progreso():
    try:
        with open("estado.json") as f:
            return jsonify(json.load(f))
    except:
        return jsonify(estado_maia)

# =========================
# RESULTADO
# =========================
@app.route("/maia_resultado")
def maia_resultado():
    try:
        with open("resultado.json") as f:
            return jsonify(json.load(f))
    except:
        return jsonify({"estado":"procesando"})

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
    app.run(host="0.0.0.0", port=port, threaded=True)