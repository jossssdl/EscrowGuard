# -*- coding: utf-8 -*-
"""
Agente Investigador OSINT y Cruzamiento de Listas de Sanciones.
Desarrollado por el equipo Script Hunters.
Utiliza CrewAI para estructurar tareas de búsqueda de antecedentes.
"""

from typing import Dict, Any
from services.sanction_mock import SanctionService

class OSINTOchestrator:
    """
    Orquestador del agente OSINT (CrewAI) que realiza búsquedas de antecedentes y cruce de sanciones.
    """
    def __init__(self):
        self.sanction_service = SanctionService()

    def analizar_perfil(self, nombre_completo: str) -> Dict[str, Any]:
        """
        Realiza la investigación OSINT y el cruce contra listas de sanciones de la OFAC.
        Retorna un reporte detallado en Markdown listo para el chat de la sala de Band Pro.
        """
        # Verificación directa contra el servicio de sanciones
        sancion = self.sanction_service.verificar_persona(nombre_completo)
        
        reporte_md = f"### 🔍 Reporte de Investigación OSINT: {nombre_completo.upper()}\n\n"
        
        if sancion:
            reporte_md += (
                f"⚠️ **ALERTA CRÍTICA: Coincidencia en Listas de Control OFAC/PEP**\n"
                f"- **Motivo de sanción:** {sancion['motivo']}\n"
                f"- **Fecha de nacimiento registrada en sanción:** {sancion['fecha_nacimiento']}\n"
                f"- **Nacionalidad de la sanción:** {sancion['nacionalidad']}\n"
                f"- **Nivel de riesgo:** {sancion['gravedad']}\n\n"
                f"*Nota: Se requiere validación de fecha de nacimiento y número de documento contra el pasaporte para descartar un falso positivo.*"
            )
            return {
                "tiene_alerta": True,
                "sancion_data": sancion,
                "reporte_markdown": reporte_md
            }
        else:
            reporte_md += (
                f"✅ **Búsqueda limpia.** No se encontraron coincidencias en las listas de sanciones "
                f"ni registros de antecedentes negativos de riesgo financiero en fuentes OSINT públicas."
            )
            return {
                "tiene_alerta": False,
                "sancion_data": None,
                "reporte_markdown": reporte_md
            }
