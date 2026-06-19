import time
import logging

# Configuracion de logs simulando un sistema de Prevencion de Lavado de Dinero (PLD)
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger("API_PLD_Mexico")

# Base de datos simulada con instituciones mexicanas (UIF, SAT) y listas internacionales (OFAC)
# Se incluye un perfil ficticio para detonar el falso positivo con el PDF de la demo
LISTAS_RIESGO_MEXICO = {
    "JOSÉ CRISTIAN AVILA DIRCIO": {
        "institucion": "UIF (Unidad de Inteligencia Financiera)",
        "lista": "Lista de Personas Bloqueadas",
        "motivo": "Persona Expuesta Politicamente (PEP) - Operaciones con Recursos de Procedencia Ilicita",
        "nivel_riesgo": "CRITICO",
        "accion_requerida": "CONGELAR_CUENTAS_AVISO_CNBV",
        "fecha_nacimiento": "1980-05-15",
        "nacionalidad": "MEXICANA",
        "gravedad": "CRITICO"
    },
    "COMERCIALIZADORA FANTASMA SA DE CV": {
        "institucion": "SAT",
        "lista": "Articulo 69-B CFF (EFOS)",
        "motivo": "Facturacion de operaciones simuladas",
        "nivel_riesgo": "ALTO",
        "accion_requerida": "REVISION_MANUAL_REQUERIDA",
        "fecha_nacimiento": "N/A",
        "nacionalidad": "MEXICANA",
        "gravedad": "ALTO"
    },
    "JUAN PEREZ": {
        "institucion": "OFAC (Office of Foreign Assets Control)",
        "lista": "Specially Designated Nationals (SDN)",
        "motivo": "Lavado de Dinero - Cartel de la frontera",
        "nivel_riesgo": "CRITICO",
        "accion_requerida": "CONGELAR_CUENTAS_INMEDIATO",
        "fecha_nacimiento": "1975-04-12",
        "nacionalidad": "MEXICANA",
        "gravedad": "CRITICO"
    }
}

import unicodedata

def eliminar_acentos(texto: str) -> str:
    return "".join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')

def consultar_listas_nacionales(nombre_entidad: str) -> dict:
    logger.info(f"Iniciando cruce de datos con listas UIF y SAT para: '{nombre_entidad}'")
    
    # Latencia para simular la consulta a los servidores gubernamentales
    time.sleep(2.0)
    
    nombre_normalizado = eliminar_acentos(nombre_entidad.strip().upper())
    
    # Caso 1: Coincidencia exacta (Bloqueo y reporte)
    if nombre_normalizado in LISTAS_RIESGO_MEXICO:
        logger.warning(f"ALERTA: Entidad localizada en listas negras nacionales/internacionales: {nombre_normalizado}")
        return {
            "estado_pld": "BLOQUEADO",
            "tipo_alerta": "COINCIDENCIA_EXACTA_UIF_SAT",
            "detalles_institucion": LISTAS_RIESGO_MEXICO[nombre_normalizado]
        }
        
    # Caso 2: Falso Positivo (Homonimia para la demostracion)
    for nombre_sancionado, datos in LISTAS_RIESGO_MEXICO.items():
        partes_sancionado = nombre_sancionado.split()
        if len(partes_sancionado) >= 2:
            apellidos_sancionados = partes_sancionado[-2:] if len(partes_sancionado) >= 3 else [partes_sancionado[-1]]
            apellidos_sancionados = [eliminar_acentos(ap).upper() for ap in apellidos_sancionados]
            
            palabras_comprador = [eliminar_acentos(p).upper() for p in nombre_normalizado.split()]
            
            coincidencias = [ap for ap in apellidos_sancionados if ap in palabras_comprador]
            
            if coincidencias:
                logger.warning(f"Posible homonimo detectado. El usuario comparte apellidos con PEP: {coincidencias}")
                detalles = datos.copy()
                detalles.update({
                    "institucion": "SISTEMA_INTERNO_ESCROWGUARD",
                    "motivo": f"Apellidos coinciden con entidad de alto riesgo ({nombre_sancionado}).",
                    "nivel_riesgo": "MEDIO",
                    "accion_requerida": "REQUIERE_DESBLOQUEO_OFICIAL_CUMPLIMIENTO"
                })
                return {
                    "estado_pld": "RETENIDO_EN_GARANTIA",
                    "tipo_alerta": "POSIBLE_HOMONIMO_PEP",
                    "detalles_institucion": detalles
                }
            
    # Caso 3: Usuario limpio
    logger.info("Entidad validada correctamente. Constancia de Situacion Fiscal e historial UIF limpios.")
    return {
        "estado_pld": "APROBADO",
        "tipo_alerta": "NINGUNA",
        "detalles_institucion": None
    }

class SanctionService:
    """
    Clase que encapsula el servicio de control y validación de personas en listas de sanciones.
    """
    def __init__(self):
        pass

    def consultar_nombre(self, nombre_completo: str) -> dict:
        """
        Consulta listas nacionales e internacionales simuladas y retorna el diccionario de estado de prevención de lavado de dinero.
        """
        return consultar_listas_nacionales(nombre_completo)

    def verificar_persona(self, nombre_completo: str) -> dict:
        """
        Verifica si una persona está en las listas de sanciones. Retorna los detalles de la sanción o None si está limpio.
        """
        nombre_normalizado = eliminar_acentos(nombre_completo.strip().upper())
        if nombre_normalizado in LISTAS_RIESGO_MEXICO:
            return LISTAS_RIESGO_MEXICO[nombre_normalizado]
        
        for nombre_sancionado, datos in LISTAS_RIESGO_MEXICO.items():
            partes_sancionado = nombre_sancionado.split()
            if len(partes_sancionado) >= 2:
                apellidos_sancionados = partes_sancionado[-2:] if len(partes_sancionado) >= 3 else [partes_sancionado[-1]]
                apellidos_sancionados = [eliminar_acentos(ap).upper() for ap in apellidos_sancionados]
                
                palabras_comprador = [eliminar_acentos(p).upper() for p in nombre_normalizado.split()]
                
                coincidencias = [ap for ap in apellidos_sancionados if ap in palabras_comprador]
                if coincidencias:
                    return datos
        
        return None