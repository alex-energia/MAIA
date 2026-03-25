# =========================
# ESTADO GLOBAL
# =========================
estado_maia = {
    "progreso": 0,
    "estado": "IDLE",
    "mensaje": ""
}

resultado_global = {}

# =========================
# CORE
# =========================
class MaiaCore:

    def progreso(self, val, msg):
        estado_maia["progreso"] = val
        estado_maia["mensaje"] = msg
        estado_maia["estado"] = "PROCESANDO"

        print(f"🧠 {val}% - {msg}")

        # 🔥 MÁS LENTO PARA VER PROGRESO REAL
        time.sleep(1)

    def analizar(self, idea):
        self.progreso(10, "🟢 Capa 1 → Analizando idea...")

        idea = idea.lower()
        peso = 5
        tipo = "general"

        if "incendio" in idea:
            peso += 6
            tipo = "emergencia"

        if "mineria" in idea:
            peso += 4
            tipo = "industrial"

        if "seguridad" in idea:
            peso += 2
            tipo = "vigilancia"

        return {"peso": peso, "tipo": tipo}

    def ejecutar(self, idea):
        global resultado_global

        try:
            print("🔥 Ejecutando MAIA:", idea)

            analisis = self.analizar(idea)

            self.progreso(40, "🔵 Capa 2 → Generando proyecto...")

            ruta = crear_proyecto(
                f"drone_{int(time.time())}",
                analisis["peso"]
            )

            self.progreso(70, "🔴 Capa 3 → IA simulando...")

            salida = ejecutar_main(ruta)

            zip_path = exportar_zip(ruta)

            self.progreso(100, "✅ Completado")

            resultado_global = {
                "viabilidad": "VIABLE ✅",
                "analisis": analisis,
                "salida": salida,
                "software_generado": ruta,
                "zip": zip_path
            }

            estado_maia["estado"] = "COMPLETADO"

        except Exception as e:
            print("💥 ERROR:", str(e))

            resultado_global = {
                "viabilidad": "ERROR ❌",
                "error": str(e)
            }

            estado_maia["estado"] = "ERROR"

# =========================
# THREAD
# =========================
def proceso_maia(idea):
    core = MaiaCore()
    core.ejecutar(idea)

# =========================
# ENDPOINT EVALUAR (MEJORADO)
# =========================
@app.route("/evaluar_drone", methods=["POST"])
def evaluar_drone():

    global estado_maia, resultado_global

    data = request.get_json(silent=True) or {}
    idea = data.get("idea", "")

    if len(idea.strip()) < 3:
        return jsonify({"error": "Idea muy corta"})

    # 🔥 RESET TOTAL (CLAVE)
    estado_maia["progreso"] = 0
    estado_maia["mensaje"] = "Iniciando..."
    estado_maia["estado"] = "PROCESANDO"
    resultado_global = {}

    # 🔥 THREAD REAL
    threading.Thread(
        target=proceso_maia,
        args=(idea,),
        daemon=True
    ).start()

    return jsonify({"status": "ok"})

# =========================
# PROGRESO
# =========================
@app.route("/maia_progreso")
def maia_progreso():
    return jsonify(estado_maia)

# =========================
# RESULTADO
# =========================
@app.route("/maia_resultado")
def maia_resultado():
    return jsonify(resultado_global)