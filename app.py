from flask import Flask, render_template, request, jsonify
from proyectos import proyectos_bp, init_db
from maia_core_fisico import analizar_drone
import os, time, zipfile

print("MAIA INDUSTRIAL CORE LEVEL 5")

app = Flask(__name__, template_folder="templates")
app.secret_key = "maia_ultra"

# =========================
# NO CACHE
# =========================
@app.after_request
def add_header(response):
    response.cache_control.no_store = True
    return response

init_db()
app.register_blueprint(proyectos_bp)

# =========================
# FILE WRITER
# =========================
def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

# =========================
# ANALISIS VIABILIDAD
# =========================
def analizar_viabilidad(idea):
    idea=idea.lower();score=0;justificacion=[];problemas=[];soluciones=[]
    if "incendio" in idea:score+=2;justificacion.append("Aplicacion a emergencia real")
    else:problemas.append("No enfocado a problema critico");soluciones.append("Aplicar a incendios o rescate")
    if "autonom" in idea:score+=2;justificacion.append("Sistema autonomo considerado")
    else:score+=1;problemas.append("Falta autonomia");soluciones.append("Implementar navegacion autonoma")
    if "sensor" in idea or "camara" in idea:score+=2;justificacion.append("Sistema de percepcion incluido")
    else:score+=1;problemas.append("Sin percepcion");soluciones.append("Agregar sensores termicos")
    estado="ALTAMENTE VIABLE" if score>=6 else "VIABLE" if score>=4 else "VIABLE CON MEJORAS"
    return {"estado":estado,"score":score,"justificacion":justificacion,"problemas":problemas,"soluciones":soluciones}

# =========================
# ANALISIS IDEA
# =========================
def analizar_idea(idea):
    return {"tipo_mision":"Extincion de incendios" if "incendio" in idea.lower() else "General","complejidad":"Alta","riesgo_tecnico":"Integracion de multiples sistemas","recomendacion":"Implementar control + IA + simulacion"}

# =========================
# HARDWARE
# =========================
def generar_hardware(peso):
    return {"estructura":{"material":"carbon fiber aerospace","tipo":"quad_x industrial"},"propulsion":{"motores":4,"kv":1200,"thrust_por_motor_kg":6.5,"esc":"BLHeli_32 45A"},"controlador_vuelo":"Pixhawk","energia":{"bateria":"LiPo 6S 10000mAh","voltaje":22.2},"sensores":{"termico":True,"lidar":True,"gps":True},"peso_total":peso}

# =========================
# SOFTWARE INDUSTRIAL
# =========================
def generar_software(base):
    root=os.path.join(base,"software")
    estructura={"main.py":"""import time,random
from threading import Thread

telemetry={}

class PID:
    def __init__(self,kp,ki,kd):
        self.kp=kp;self.ki=ki;self.kd=kd;self.i=0;self.prev=0
    def update(self,sp,meas,dt):
        e=sp-meas;self.i+=e*dt;d=(e-self.prev)/dt if dt>0 else 0;self.prev=e
        return self.kp*e+self.ki*self.i+self.kd*d

pid=PID(1.5,0.02,0.5)

def sensores():
    return {"altitude":random.uniform(8,12),"battery":random.uniform(50,100),"temperature":random.uniform(30,90)}

def control():
    while True:
        s=sensores();telemetry["sensors"]=s
        telemetry["throttle"]=pid.update(10,s["altitude"],0.02)
        time.sleep(0.02)

def ai():
    while True:
        s=telemetry.get("sensors",{})
        if s.get("temperature",0)>70:action="EXTINGUIR"
        elif s.get("battery",100)<30:action="RETORNAR"
        else:action="PATRULLAR"
        telemetry["decision"]=action
        print("AI:",action)
        time.sleep(0.1)

def mavlink():
    while True:
        print("MAVLINK:",telemetry.get("sensors",{}))
        time.sleep(0.5)

Thread(target=control).start()
Thread(target=ai).start()
Thread(target=mavlink).start()

while True:time.sleep(1)
"""}
    def crear(ruta,contenido):
        if isinstance(contenido,dict):
            for k,v in contenido.items():crear(os.path.join(ruta,k),v)
        else:write_file(ruta,contenido)
    crear(root,estructura)
    return estructura

# =========================
# RESTO
# =========================
def calcular_fisica(peso):
    thrust=26
    return {"thrust_total":thrust,"relacion":round(thrust/peso,2),"estado":"ESTABLE"}

def generar_telemetria():
    return {"variables":["x","y","z","battery"],"frecuencia_hz":10}

def generar_modelo_3d(base,peso):
    return {"tipo":"quad_x industrial","escala":peso}

def exportar_zip(path):
    zip_path=path+".zip"
    with zipfile.ZipFile(zip_path,'w') as zipf:
        for root,_,files in os.walk(path):
            for f in files:
                full=os.path.join(root,f)
                zipf.write(full,os.path.relpath(full,path))
    return zip_path

# =========================
# CORE
# =========================
class MaiaCore:
    def ejecutar_paso(self,idea,paso,data):
        if paso==0:
            return {"paso":1,"data":{"core":analizar_drone(idea),"viabilidad":analizar_viabilidad(idea),"analisis_idea":analizar_idea(idea)}}
        elif paso==1:
            data["hardware"]=generar_hardware(12);return {"paso":2,"data":data}
        elif paso==2:
            base=f"maia_projects/{int(time.time())}";os.makedirs(base,exist_ok=True)
            data["base"]=base;data["software"]=generar_software(base)
            return {"paso":3,"data":data}
        elif paso==3:
            data["fisica"]=calcular_fisica(data["hardware"]["peso_total"])
            data["telemetria"]=generar_telemetria()
            return {"paso":4,"data":data}
        elif paso==4:
            data["riesgos"]=["viento extremo","fallo bateria","perdida señal"]
            return {"paso":5,"data":data}
        elif paso==5:
            data["modelo_3d"]=generar_modelo_3d(data["base"],data["hardware"]["peso_total"])
            return {"paso":6,"data":data}
        elif paso==6:
            data["zip"]=exportar_zip(data["base"])
            data["nivel_maia"]="NIVEL 5 - INDUSTRIAL SYSTEM"
            return {"final":True,"resultado":data}

# =========================
# API
# =========================
@app.route("/maia_step",methods=["POST"])
def maia_step():
    req=request.get_json() or {}
    core=MaiaCore()
    return jsonify(core.ejecutar_paso(req.get("idea",""),int(req.get("paso",0)),req.get("data",{})))

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
if __name__=="__main__":
    app.run(host="0.0.0.0",port=10000)