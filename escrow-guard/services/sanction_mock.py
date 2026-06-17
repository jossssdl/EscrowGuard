# -*- coding: utf-8 -*-
"""
Servicio de simulación para verificación de sanciones (OFAC / PEP).
Desarrollado por el equipo Script Hunters.
"""

from typing import Dict, Any, Optional

class SanctionService:
    """
    Clase simulada para realizar consultas contra listas de sanciones internacionales.
    """
    def __init__(self):
        # Base de datos estática de personas sancionadas
        self._sancionados = [
            {
                "nombre_completo": "JUAN PEREZ",
                "fecha_nacimiento": "1975-04-12",
                "nacionalidad": "MEXICANA",
                "motivo": "Lavado de Dinero - Cartel de la Frontera",
                "gravedad": "ALTA"
            },
            {
                "nombre_completo": "ALEXIS SMITH",
                "fecha_nacimiento": "1988-11-23",
                "nacionalidad": "ESTADOUNIDENSE",
                "motivo": "Financiamiento de Actividades Ilícitas",
                "gravedad": "ALTA"
            }
        ]

    def verificar_persona(self, nombre: str) -> Optional[Dict[str, Any]]:
        """
        Busca a una persona en la lista de sanciones por nombre completo.
        Realiza una comparación insensible a mayúsculas/minúsculas.
        """
        nombre_normalizado = nombre.strip().upper()
        for registro in self._sancionados:
            if registro["nombre_completo"] == nombre_normalizado:
                return registro
        return None
