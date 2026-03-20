from flask import Flask, render_template, request, jsonify, session
from proyectos import proyectos_bp, init_db
import os
from bs4 import BeautifulSoup  # Para extraer nombres de drones desde HTML

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
# 🔥 CARGA DINÁMICA DE DRONES CON DATOS COMPLETOS
# =========================
def cargar_drones_base():
    drones = []
    carpeta_drones = os.path.join(app.template_folder, "drones")

    for archivo in os.listdir(carpeta_drones):
        if archivo.endswith(".html"):

            ruta = "/drones/" + archivo.replace(".html", "")
            path_completo = os.path.join(carpeta_drones, archivo)

            try:
                with open(path_completo, "r", encoding="utf-8") as f:
                    soup = BeautifulSoup(f, "html.parser")
                    titulo = soup.title.string.strip() if soup.title else archivo.replace(".html", "")
            except Exception:
                titulo = archivo.replace(".html", "")

            lower = archivo.lower()

            if "minas" in lower or "militar" in lower:
                categoria = "militar"
            elif "todo_terreno" in lower or "smartphone" in lower:
                categoria = "comercial"
            else:
                categoria = "industrial"

            drones.append({
                "nombre": titulo,
                "ruta": ruta,
                "categoria": categoria,
                "introduccion": f"Descripción completa de {titulo}.",
                "viabilidad": "Alta viabilidad para aplicaciones específicas.",
                "software": [
                    "Control inteligente via MAIA App",
                    "Detección automática de obstáculos",
                    "Modo seguimiento y selfie",
                    "Grabación de video HD"
                ],
                "hardware": [
                    "Motores brushless",
                    "Batería de larga duración",
                    "Cámara integrada 12MP",
                    "Sensores de proximidad y GPS",
                    "LEDs de iluminación"
                ]
            })

    return drones


# Variable global
DRONES_BASE = cargar_drones_base()

# =========================
# 🔥 RUTA PRINCIPAL
# =========================
@app.route("/")
def home():
    return render_template("index.html")

# =========================
# 🔥 API DRONES FILTRADO
# =========================
@app.route("/maia_drones_aprobados")
def maia_drones_aprobados():
    categoria = request.args.get("categoria")

    if categoria:
        filtrados = [d for d in DRONES_BASE if d["categoria"] == categoria]
        return jsonify(filtrados)

    return jsonify(DRONES_BASE)

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
# 🔥 INYECCIÓN GLOBAL
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

    respuesta = (
        f"MAIA IA avanzada:"
        f"Contexto previo:{contexto}"
        f"Nueva pregunta:{pregunta}"
        f"Respuesta: Análisis experto en ingeniería, energía, drones y sistemas inteligentes."
        f"Conclusión optimizada basada en memoria conversacional."
    )

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
# 🔥 RUTAS MÓDULOS EXTRA
# =========================
@app.route("/maia_simulador")
def maia_simulador():
    return render_template("maia_simulador.html")

@app.route("/maia_invent")
def maia_invent():
    return render_template("maia_invent.html")

@app.route("/maia_lab")
def maia_lab():
    return render_template("maia_lab.html")

@app.route("/maia_architect")
def maia_architect():
    return render_template("maia_architect.html")

# =========================
# ✅ 🔥 NUEVA RUTA (SOLUCIÓN ERROR 404)
# =========================
@app.route("/maia_chat")
def maia_chat():
    return render_template("maia_chat.html")

# =========================
# 🔥 RUTA DINÁMICA PARA DRONES
# =========================
@app.route("/drones/<drone_file>")
def abrir_drone(drone_file):
    ruta_html = f"drones/{drone_file}.html"

    if os.path.exists(os.path.join(app.template_folder, ruta_html)):
        return render_template(ruta_html)
    else:
        return "Drone no encontrado", 404

# =========================
# 🚀 Gunicorn maneja ejecución
# =========================