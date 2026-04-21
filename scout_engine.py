# -*- coding: utf-8 -*-
# scout_engine.py

def get_market_scout():
    return [
        # AMÉRICA
        {"id": "SC-COL-01", "Nombre": "Eólico La Guajira", "Ubicación": "Colombia", "Valor_Est": "USD 45M", "Potencia": "120 MW", "Riesgo": "BAJO", "Calificacion_IA": "9.5/10", "Tipo": "Eléctrico", "Resumen": "Licitación para expansión de red en zona norte. Alta radiación eólica.", "Contacto": "proyectos@guajira.co", "Vigencia": "31-DIC-2026", "Fuente": "UPME"},
        {"id": "SC-USA-01", "Nombre": "Solar Texas Hub", "Ubicación": "USA", "Valor_Est": "USD 210M", "Potencia": "400 MW", "Riesgo": "MÍNIMO", "Calificacion_IA": "9.8/10", "Tipo": "Eléctrico", "Resumen": "Granja solar con almacenamiento de baterías Tesla Megapack.", "Contacto": "m&a@texashub.com", "Vigencia": "10-ENE-2027", "Fuente": "DOE"},
        {"id": "SC-BRA-01", "Nombre": "Amazonas Hydro", "Ubicación": "Brasil", "Valor_Est": "USD 180M", "Potencia": "300 MW", "Riesgo": "MEDIO", "Calificacion_IA": "8.2/10", "Tipo": "Eléctrico", "Resumen": "Proyecto hidroeléctrico de pasada con bajo impacto ambiental.", "Contacto": "invest@aneel.gov.br", "Vigencia": "15-MAR-2027", "Fuente": "ANEEL"},
        
        # EUROPA
        {"id": "SC-GER-01", "Nombre": "Offshore Báltico", "Ubicación": "Alemania", "Valor_Est": "USD 500M", "Potencia": "1 GW", "Riesgo": "BAJO", "Calificacion_IA": "9.0/10", "Tipo": "Eléctrico", "Resumen": "Parque eólico marino en aguas profundas. Tecnología Siemens.", "Contacto": "energy@bundes.de", "Vigencia": "20-JUN-2027", "Fuente": "BMWK"},
        {"id": "SC-SPA-01", "Nombre": "Fotovoltaica Sevilla", "Ubicación": "España", "Valor_Est": "USD 95M", "Potencia": "150 MW", "Riesgo": "MÍNIMO", "Calificacion_IA": "9.3/10", "Tipo": "Eléctrico", "Resumen": "Planta operativa con contrato PPA a 15 años firmado.", "Contacto": "ops@ree.es", "Vigencia": "30-SEP-2026", "Fuente": "IDAE"},
        
        # ASIA / ORIENTE
        {"id": "SC-CHN-01", "Nombre": "Giga-Grid Shanghai", "Ubicación": "China", "Valor_Est": "USD 1.2B", "Potencia": "5 GW", "Riesgo": "MEDIO", "Calificacion_IA": "7.5/10", "Tipo": "Eléctrico", "Resumen": "Modernización de red inteligente con IA para distribución urbana.", "Contacto": "grid@stategrid.cn", "Vigencia": "01-DIC-2027", "Fuente": "NEA"},
        {"id": "SC-SAU-01", "Nombre": "Neom H2 Plant", "Ubicación": "Arabia Saudita", "Valor_Est": "USD 900M", "Potencia": "2 GW", "Riesgo": "MEDIO", "Calificacion_IA": "8.9/10", "Tipo": "H2 Verde", "Resumen": "Producción de hidrógeno verde mediante electrolizadores masivos.", "Contacto": "m&a@neom.sa", "Vigencia": "01-FEB-2028", "Fuente": "PIF"},
        {"id": "SC-KOR-01", "Nombre": "Tidal Incheon", "Ubicación": "Corea del Sur", "Valor_Est": "USD 130M", "Potencia": "100 MW", "Riesgo": "BAJO", "Calificacion_IA": "9.1/10", "Tipo": "Mareomotriz", "Resumen": "Energía por mareas en el estrecho de Incheon. Alta eficiencia.", "Contacto": "biz@kepco.kr", "Vigencia": "12-NOV-2026", "Fuente": "MOTIE"}
    ]