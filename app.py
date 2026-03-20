from flask import Flask, render_template, request, jsonify, redirect, session
from proyectos import proyectos_bp, init_db, get_db
import os
import random

# =========================
# APP
# =========================
app = Flask(__name__, template_folder="templates")
app.secret_key = "maia_secret_ultra"

# =========================
# INIT
# =========================
init_db()
app.register_blueprint(proyectos_bp)

# =========================
# 🔥 RUTA PRINCIPAL (SOLUCION 404)
# =========================
@app.route("/")
def home():
    return render_template("index.html")

# =========================
# 🔥 MEMORIA MAIA
# =========================
def obtener_memoria():
    if "historial" not in session:
        session["historial"] = []
    return session["historial"]

def guardar_memoria(pregunta, respuesta):
    historial = obtener_memoria()
    historial.append({"pregunta": pregunta, "respuesta": respuesta})

    if len(historial) > 10:
        historial.pop(0)

    session["historial"] = historial

# =========================
# 🔥 INYECCIÓN GLOBAL (MAIA EN TODAS LAS VISTAS)
# =========================
@app.context_processor
def inyectar_maia():
    return dict(maia_global=True)

# =========================
# 🔥 MAIA VOZ INTELIGENTE
# =========================
@app.route("/maia_voz", methods=["POST"])
def maia_voz():
    data = request.get_json()
    pregunta = data.get("pregunta", "")

    historial = obtener_memoria()
    contexto = ""

    for h in historial:
        contexto += f"Usuario: {h['pregunta']}\nMAIA: {h['respuesta']}\n"

    respuesta = f"""
MAIA IA avanzada:

Contexto previo:
{contexto}

Nueva pregunta:
{pregunta}

Respuesta:
Análisis experto en ingeniería, energía, drones y sistemas inteligentes.
Conclusión optimizada basada en memoria conversacional.
"""

    guardar_memoria(pregunta, respuesta)

    return jsonify({"respuesta": respuesta})

# =========================
# 📎 SUBIR ARCHIVOS
# =========================
@app.route("/maia_subir_archivo", methods=["POST"])
def maia_subir_archivo():
    archivos = request.files.getlist('archivos')
    nombres = [a.filename for a in archivos]
    return jsonify({"archivos": nombres})

# =========================
# 🧠 RESET MEMORIA
# =========================
@app.route("/reset_maia")
def reset_maia():
    session.pop("historial", None)
    return jsonify({"status": "memoria borrada"})

# =========================
# 🚀 RUN
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)