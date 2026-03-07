from flask import Blueprint, render_template, request, redirect
import sqlite3

# =========================
# BLUEPRINT
# =========================

proyectos_bp = Blueprint("proyectos", __name__)

DB = "maia.db"

# =========================
# CONEXION BASE DE DATOS
# =========================

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

# =========================
# CREAR TABLA
# =========================

def init_db():
    conn = get_db()
    conn.execute("""
    CREATE TABLE IF NOT EXISTS proyectos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        capex_inicial REAL,
        opex_anual REAL,
        ingresos_anuales REAL,
        vida_util INTEGER,
        tasa_descuento REAL
    )
    """)
    conn.commit()
    conn.close()

# =========================
# DESGLOSE CAPEX
# =========================

def desglose_capex(capex):

    return [

        {"actividad":"Ingeniería","valor":round(capex*0.15,2)},
        {"actividad":"Equipos","valor":round(capex*0.40,2)},
        {"actividad":"Construcción","valor":round(capex*0.25,2)},
        {"actividad":"Permisos","valor":round(capex*0.10,2)},
        {"actividad":"Contingencia","valor":round(capex*0.10,2)}

    ]

# =========================
# DESGLOSE OPEX
# =========================

def desglose_opex(opex):

    return [

        {"actividad":"Operación","valor":round(opex*0.35,2)},
        {"actividad":"Mantenimiento","valor":round(opex*0.25,2)},
        {"actividad":"Administración","valor":round(opex*0.15,2)},
        {"actividad":"Logística","valor":round(opex*0.15,2)},
        {"actividad":"Regulación","valor":round(opex*0.10,2)}

    ]

# =========================
# MOTOR GENERACION VALOR
# =========================

def generar_valor(capex, ingresos, opex, vida, tasa):

    flujo_operativo = ingresos - opex

    valor_ingresos = ingresos * vida

    valor_costos = opex * vida

    eficiencia_capital = flujo_operativo / capex if capex != 0 else 0

    van = 0

    for i in range(1, vida+1):

        van += flujo_operativo / ((1+tasa)**i)

    van -= capex

    valor = [

        {
        "driver":"Ingresos operacionales totales",
        "valor":round(valor_ingresos,2)
        },

        {
        "driver":"Costos operacionales totales",
        "valor":round(valor_costos,2)
        },

        {
        "driver":"Flujo operativo anual",
        "valor":round(flujo_operativo,2)
        },

        {
        "driver":"Eficiencia del capital",
        "valor":round(eficiencia_capital,3)
        },

        {
        "driver":"Valor presente del proyecto",
        "valor":round(van,2)
        }

    ]

    return valor

# =========================
# LISTA PROYECTOS
# =========================

@proyectos_bp.route("/proyectos")

def lista_proyectos():

    conn = get_db()

    proyectos = conn.execute(
        "SELECT * FROM proyectos"
    ).fetchall()

    conn.close()

    return render_template(
        "proyectos.html",
        proyectos=proyectos
    )

# =========================
# CREAR PROYECTO
# =========================

@proyectos_bp.route("/proyectos/nuevo", methods=["GET","POST"])

def nuevo_proyecto():

    if request.method == "POST":

        nombre = request.form["nombre"]
        capex = float(request.form["capex"])
        opex = float(request.form["opex"])
        ingresos = float(request.form["ingresos"])
        vida = int(request.form["vida"])
        tasa = float(request.form["tasa"])

        conn = get_db()

        conn.execute("""

        INSERT INTO proyectos
        (nombre,capex_inicial,opex_anual,ingresos_anuales,vida_util,tasa_descuento)
        VALUES (?,?,?,?,?,?)

        """,(nombre,capex,opex,ingresos,vida,tasa))

        conn.commit()

        conn.close()

        return redirect("/proyectos")

    return render_template("nuevo_proyecto.html")

# =========================
# DASHBOARD PROYECTO
# =========================

@proyectos_bp.route("/proyectos/<int:proyecto_id>")

def dashboard_proyecto(proyecto_id):

    conn = get_db()

    proyecto = conn.execute(
        "SELECT * FROM proyectos WHERE id=?",
        (proyecto_id,)
    ).fetchone()

    conn.close()

    if not proyecto:

        return "Proyecto no encontrado"

    capex = proyecto["capex_inicial"]
    opex = proyecto["opex_anual"]
    ingresos = proyecto["ingresos_anuales"]
    vida = proyecto["vida_util"]
    tasa = proyecto["tasa_descuento"]

    flujo_anual = ingresos - opex

    # =========================
    # FLUJOS
    # =========================

    flujos = [-capex]

    for i in range(vida):

        flujos.append(flujo_anual)

    # =========================
    # VAN
    # =========================

    van = 0

    for i,f in enumerate(flujos):

        van += f / ((1+tasa)**i)

    # =========================
    # TIR
    # =========================

    tir = None

    try:

        r = 0.1

        for i in range(100):

            van_temp = 0
            dvan = 0

            for t,f in enumerate(flujos):

                van_temp += f / ((1+r)**t)

                if t > 0:

                    dvan += -t*f/((1+r)**(t+1))

            r = r - van_temp/dvan

        tir = r

    except:

        tir = None

    # =========================
    # PAYBACK
    # =========================

    acumulado = 0

    payback = None

    for i,f in enumerate(flujos):

        acumulado += f

        if acumulado > 0:

            payback = i

            break

    # =========================
    # EVALUACION
    # =========================

    if van > 0:

        evaluacion = "Proyecto rentable"
        recomendacion = "Invertir"

    else:

        evaluacion = "Proyecto no rentable"
        recomendacion = "No invertir"

    # =========================
    # DESGLOSE COSTOS
    # =========================

    capex_detallado = desglose_capex(capex)

    opex_detallado = desglose_opex(opex)

    # =========================
    # GENERACION DE VALOR
    # =========================

    valor_generado = generar_valor(
        capex,
        ingresos,
        opex,
        vida,
        tasa
    )

    # =========================
    # INDICADORES FINANCIEROS AVANZADOS
    # =========================

    indicadores_financieros = motor_financiero_avanzado(
        capex,
        ingresos,
        opex,
        vida,
        tasa
    )

    # =========================
    # RENDER
    # =========================

    return render_template(

        "proyecto_dashboard.html",

        proyecto=proyecto,
        flujo_anual=round(flujo_anual,2),
        van=round(van,2),
        tir=round(tir,4) if tir else None,
        payback=payback,
        evaluacion=evaluacion,
        recomendacion=recomendacion,
        flujos=flujos,
        capex_detallado=capex_detallado,
        opex_detallado=opex_detallado,
        valor_generado=valor_generado,
        indicadores_financieros=indicadores_financieros

    )

# ============================================================
# MOTOR FINANCIERO AVANZADO MAIA
# ============================================================

def motor_financiero_avanzado(
    capex,
    ingresos,
    opex,
    vida,
    tasa,
    deuda=0,
    equity=None,
    tasa_impuesto=0.30,
    costo_deuda=0.08,
    costo_equity=0.12
):

    if equity is None:
        equity = capex - deuda

    flujo_operativo = ingresos - opex

    depreciacion = capex / vida if vida != 0 else 0

    ebitda = flujo_operativo

    ebit = ebitda - depreciacion

    impuestos = ebit * tasa_impuesto if ebit > 0 else 0

    utilidad_neta = ebit - impuestos

    roi = ((flujo_operativo * vida) - capex) / capex if capex != 0 else 0

    roa = utilidad_neta / capex if capex != 0 else 0

    roe = utilidad_neta / equity if equity != 0 else 0

    roic = ebit / capex if capex != 0 else 0

    margen_ebitda = ebitda / ingresos if ingresos != 0 else 0

    margen_operativo = ebit / ingresos if ingresos != 0 else 0

    margen_neto = utilidad_neta / ingresos if ingresos != 0 else 0

    total_capital = deuda + equity if (deuda + equity) != 0 else 1

    wacc = (
        (equity / total_capital) * costo_equity +
        (deuda / total_capital) * costo_deuda * (1 - tasa_impuesto)
    )

    van = 0

    for i in range(1, vida + 1):

        van += flujo_operativo / ((1 + tasa) ** i)

    van -= capex

    indice_rentabilidad = (van + capex) / capex if capex != 0 else 0

    relacion_bc = (flujo_operativo * vida) / capex if capex != 0 else 0

    acumulado = -capex

    payback_desc = None

    for i in range(1, vida + 1):

        flujo_desc = flujo_operativo / ((1 + tasa) ** i)

        acumulado += flujo_desc

        if acumulado > 0:

            payback_desc = i
            break

    flujo_caja_operativo = flujo_operativo

    flujo_caja_libre = flujo_operativo - depreciacion

    rotacion_activos = ingresos / capex if capex != 0 else 0

    indicadores = {

        "EBITDA": round(ebitda,2),
        "EBIT": round(ebit,2),
        "Utilidad Neta": round(utilidad_neta,2),
        "ROI": round(roi,4),
        "ROA": round(roa,4),
        "ROE": round(roe,4),
        "ROIC": round(roic,4),
        "Margen EBITDA": round(margen_ebitda,4),
        "Margen Operativo": round(margen_operativo,4),
        "Margen Neto": round(margen_neto,4),
        "WACC": round(wacc,4),
        "Indice de Rentabilidad": round(indice_rentabilidad,4),
        "Relacion Beneficio/Costo": round(relacion_bc,4),
        "Payback Descontado": payback_desc,
        "Flujo Caja Operativo": round(flujo_caja_operativo,2),
        "Flujo Caja Libre": round(flujo_caja_libre,2),
        "Rotacion de Activos": round(rotacion_activos,4),
        "VAN Financiero": round(van,2)

    }

    return indicadores