# -*- coding: utf-8 -*-
"""
Agente Investigador OSINT y Cruzamiento de Listas de Sanciones.
Desarrollado por el equipo Script Hunters.
Utiliza CrewAI para estructurar tareas de búsqueda de antecedentes y cruce de cumplimiento.
"""

import os
import logging
from typing import Dict, Any
from crewai import Agent, Task, Crew, Process, LLM
from services.sanction_mock import SanctionService

# Configuración de logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger("OSINT_Orchestrator")

class OSINTOchestrator:
    """
    Orquestador del agente OSINT (CrewAI) que realiza búsquedas de antecedentes y cruce de sanciones.
    """
    def __init__(self, sanction_service=None):
        """
        Constructor que recibe opcionalmente el servicio mock de sanciones.
        Si no se provee, se inicializa la instancia por defecto.
        """
        if sanction_service is None:
            self.sanction_service = SanctionService()
        else:
            self.sanction_service = sanction_service
        
        # Configurar LLM para CrewAI dinámicamente según variables de entorno
        self.llm = self._inicializar_llm()

    def _inicializar_llm(self) -> Any:
        """
        Inicializa y configura el LLM a utilizar basándose en la disponibilidad de API Keys.
        """
        # Mapeos de compatibilidad de variables de entorno
        if "GEMINI_API_KEY" in os.environ and "GOOGLE_API_KEY" not in os.environ:
            os.environ["GOOGLE_API_KEY"] = os.environ["GEMINI_API_KEY"]
        if "GROK_API_KEY" in os.environ and "GROQ_API_KEY" not in os.environ:
            os.environ["GROQ_API_KEY"] = os.environ["GROK_API_KEY"]

        # Priorizar Groq (rápido y eficiente)
        if "GROQ_API_KEY" in os.environ and os.environ["GROQ_API_KEY"]:
            try:
                logger.info("Inicializando LLM de Groq (Llama 3.3 70b) para CrewAI.")
                return LLM(
                    model="groq/llama-3.3-70b-versatile",
                    api_key=os.environ["GROQ_API_KEY"]
                )
            except Exception as e:
                logger.error(f"Error al inicializar LLM de Groq: {e}. Reintentando con Gemini.")

        # Fallback a Gemini
        if "GOOGLE_API_KEY" in os.environ and os.environ["GOOGLE_API_KEY"]:
            try:
                logger.info("Inicializando LLM de Gemini (2.5 Flash) para CrewAI.")
                return LLM(
                    model="gemini/gemini-2.5-flash",
                    api_key=os.environ["GOOGLE_API_KEY"]
                )
            except Exception as e:
                logger.error(f"Error al inicializar LLM de Gemini: {e}.")

        logger.warning("No se encontraron claves de API válidas. CrewAI usará valores predeterminados o fallará.")
        return None

    def analizar_perfil(self, datos_usuario: Any) -> Dict[str, Any]:
        """
        Realiza la investigación OSINT y el cruce contra listas de sanciones.
        Acepta tanto un diccionario con datos estructurados como un string simple (nombre).
        Retorna un reporte unificado en Markdown listo para renderizarse.
        """
        # Normalizar inputs (soportando tanto strings como diccionarios)
        if isinstance(datos_usuario, str):
            nombre_completo = datos_usuario
            fecha_nacimiento = "No especificada"
            nacionalidad = "MEXICANA"
        elif isinstance(datos_usuario, dict):
            nombre_completo = datos_usuario.get("nombre_completo", "")
            fecha_nacimiento = datos_usuario.get("fecha_nacimiento", "No especificada")
            nacionalidad = datos_usuario.get("nacionalidad", "MEXICANA")
        else:
            nombre_completo = str(datos_usuario)
            fecha_nacimiento = "No especificada"
            nacionalidad = "MEXICANA"

        nombre_normalizado = nombre_completo.strip().upper()
        logger.info(f"Iniciando análisis OSINT y cruce de listas para: {nombre_normalizado}")

        # 1. Consulta paralela en la base de datos mock de sanciones
        # Soportar tanto verificar_persona como consultar_nombre
        sancion_data = None
        tiene_alerta = False
        ofac_res = {}
        try:
            # Primero probar verificar_persona (usado por escrow.py)
            if hasattr(self.sanction_service, "verificar_persona"):
                sancion_data = self.sanction_service.verificar_persona(nombre_normalizado)
            
            # También consultar_nombre (usado por el prompt del hackathon)
            if hasattr(self.sanction_service, "consultar_nombre"):
                ofac_res = self.sanction_service.consultar_nombre(nombre_normalizado)
                if ofac_res and ofac_res.get("estado_pld") in ["BLOQUEADO", "RETENIDO_EN_GARANTIA"]:
                    tiene_alerta = True
                    # Si no pudimos conseguir sanction_data anteriormente, extraer de detalles_institucion
                    if not sancion_data:
                        sancion_data = ofac_res.get("detalles_institucion")
            
            if sancion_data:
                tiene_alerta = True
        except Exception as e:
            logger.error(f"Error al consultar el servicio de sanciones: {e}")
            ofac_res = {"estado_pld": "ERROR", "mensaje": str(e)}

        # 2. Configurar y lanzar el agente de CrewAI
        web_report = ""
        try:
            agent = Agent(
                role="Investigador de Antecedentes y OSINT Financiero",
                goal="Buscar noticias negativas, lavado de dinero, historial regulatorio y reportes adversos del sujeto en la web.",
                backstory="Un experto analista de inteligencia financiera, ex-oficial de cumplimiento de banca internacional, especialista en auditorías AML.",
                llm=self.llm,
                verbose=False
            )

            task = Task(
                description=f"Investigar a la persona {nombre_normalizado} nacida el {fecha_nacimiento} y de nacionalidad {nacionalidad} en internet, buscando reportes de fraude, lavado de dinero o actividad delictiva.",
                expected_output="Un reporte estructurado en Markdown con los hallazgos y una conclusión final de nivel de riesgo.",
                agent=agent
            )

            crew = Crew(
                agents=[agent],
                tasks=[task],
                process=Process.sequential,
                verbose=False
            )

            logger.info("Ejecutando CrewAI para búsqueda web OSINT...")
            result = crew.kickoff()
            # crew.kickoff() devuelve un objeto CrewOutput que se puede convertir a str
            web_report = str(result)
        except Exception as e:
            logger.error(f"Error durante la ejecución del agente CrewAI: {e}")
            web_report = f"### ⚠️ Error en Investigación OSINT Web\nNo se pudo completar la búsqueda en la web: {str(e)}"

        # 3. Formatear y unificar el reporte Markdown para la interfaz de usuario
        reporte_markdown = f"### 🔍 Reporte de Investigación OSINT: {nombre_normalizado}\n\n"
        
        if tiene_alerta and sancion_data:
            reporte_markdown += (
                f"⚠️ **ALERTA CRÍTICA: Coincidencia en Listas de Control OFAC/PEP**\n"
                f"- **Institución/Lista:** {sancion_data.get('institucion', 'OFAC')}\n"
                f"- **Motivo de sanción:** {sancion_data.get('motivo', 'Riesgo de Cumplimiento')}\n"
                f"- **Fecha de nacimiento registrada en sanción:** {sancion_data.get('fecha_nacimiento', 'Desconocida')}\n"
                f"- **Nacionalidad de la sanción:** {sancion_data.get('nacionalidad', 'Desconocida')}\n"
                f"- **Nivel de riesgo:** {sancion_data.get('nivel_riesgo', 'ALTO')}\n\n"
                f"*Nota: Se requiere validación de fecha de nacimiento y número de documento contra el pasaporte para descartar un falso positivo.*\n\n"
            )
        else:
            reporte_markdown += "✅ **Estatus en Listas de Control:** Limpio. No figura en listas OFAC o PEP conocidas.\n\n"

        reporte_markdown += "#### 🌐 Hallazgos de Fuentes Abiertas (OSINT Web Agent):\n"
        reporte_markdown += web_report

        # 4. Retornar diccionario unificado compatible con todos los componentes
        return {
            "ofac": ofac_res,
            "web_report": web_report,
            "tiene_alerta": tiene_alerta,
            "sancion_data": sancion_data,
            "reporte_markdown": reporte_markdown
        }
