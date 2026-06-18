import time
import logging

# Configuracion de logs simulando un sistema de Prevencion de Lavado de Dinero (PLD)
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger("API_PLD_Mexico")

# Base de datos simulada con instituciones mexicanas (UIF, SAT)
# Se incluye un perfil ficticio para detonar el falso positivo con el PDF de la demo
LISTAS_RIESGO_MEXICO = {
    "JOSÉ CRISTIAN AVILA DIRCIO": {
        "institucion": "UIF (Unidad de Inteligencia Financiera)",
        "lista": "Lista de Personas Bloqueadas",
        "motivo": "Persona Expuesta Politicamente (PEP) - Operaciones con Recursos de Procedencia Ilicita",
        "nivel_riesgo": "CRITICO",
        "accion_requerida": "CONGELAR_CUENTAS_AVISO_CNBV"
    },
    "COMERCIALIZADORA FANTASMA SA DE CV": {
        "institucion": "SAT",
        "lista": "Articulo 69-B CFF (EFOS)",
        "motivo": "Facturacion de operaciones simuladas",
        "nivel_riesgo": "ALTO",
        "accion_requerida": "REVISION_MANUAL_REQUERIDA"
    }
}

def consultar_listas_nacionales(nombre_entidad: str) -> dict:
    logger.info(f"Iniciando cruce de datos con listas UIF y SAT para: '{nombre_entidad}'")
    
    # Latencia para simular la consulta a los servidores gubernamentales
    time.sleep(2.0)
    
    nombre_normalizado = nombre_entidad.strip().upper()
    
    # Caso 1: Coincidencia exacta (Bloqueo y reporte)
    if nombre_normalizado in LISTAS_RIESGO_MEXICO:
        logger.warning(f"ALERTA: Entidad localizada en listas negras nacionales: {nombre_normalizado}")
        return {
            "estado_pld": "BLOQUEADO",
            "tipo_alerta": "COINCIDENCIA_EXACTA_UIF_SAT",
            "detalles_institucion": LISTAS_RIESGO_MEXICO[nombre_normalizado]
        }
        
    # Caso 2: Falso Positivo (Homonimia para la demostracion)
    for nombre_sancionado, datos in LISTAS_RIESGO_MEXICO.items():
        # Extraemos los ultimos dos elementos del nombre (los apellidos) para buscar similitudes
        partes_nombre_malo = nombre_sancionado.split()
        if len(partes_nombre_malo) >= 2:
            apellido_sancionado = partes_nombre_malo[-2] + " " + partes_nombre_malo[-1]
            
            if apellido_sancionado in nombre_normalizado:
                logger.warning(f"Posible homonimo detectado. El usuario comparte apellidos con PEP: {apellido_sancionado}")
                return {
                    "estado_pld": "RETENIDO_EN_GARANTIA",
                    "tipo_alerta": "POSIBLE_HOMONIMO_PEP",
                    "detalles_institucion": {
                        "institucion": "SISTEMA_INTERNO_ESCROWGUARD",
                        "motivo": f"Apellidos coinciden con entidad de alto riesgo ({nombre_sancionado}).",
                        "nivel_riesgo": "MEDIO",
                        "accion_requerida": "REQUIERE_DESBLOQUEO_OFICIAL_CUMPLIMIENTO"
                    }
                }
            
    # Caso 3: Usuario limpio
    logger.info("Entidad validada correctamente. Constancia de Situacion Fiscal e historial UIF limpios.")
    return {
        "estado_pld": "APROBADO",
        "tipo_alerta": "NINGUNA",
        "detalles_institucion": None
    }