# -*- coding: utf-8 -*-
"""
Agente Extractor de Información de Documentos de Identidad (Pasaportes).
Desarrollado por el equipo Script Hunters.
Utiliza PydanticAI para estructurar los datos extraídos de PDFs.
"""

from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

# Esquema de datos esperado para el comprador
class CompradorSchema(BaseModel):
    nombre_completo: str = Field(..., description="Nombre completo tal como aparece en el documento")
    fecha_nacimiento: str = Field(..., description="Fecha de nacimiento en formato AAAA-MM-DD")
    numero_documento: str = Field(..., description="Número de pasaporte o identificación oficial")
    nacionalidad: str = Field(..., description="Nacionalidad del titular del documento")
    tipo_documento: str = Field(default="Pasaporte", description="Tipo de documento analizado")

class ExtractorAgent:
    """
    Simulación y base para el Agente de Extracción de PydanticAI.
    """
    def run_sync(self, input_text_or_pdf_path: str) -> CompradorSchema:
        """
        Método síncrono para ejecutar la extracción.
        Clasifica la información de retorno simulada según palabras clave en el nombre del archivo
        o texto para facilitar las pruebas de la demo (Casos: Válido, Falso Positivo e Identidad Confirmada).
        """
        texto = input_text_or_pdf_path.upper()
        
        # Caso 1: Riesgo Confirmado (Coincide nombre y cumpleaños 1975-04-12)
        if "CONFIRMADO" in texto or "SANCIONADO" in texto or "RIESGO" in texto:
            return CompradorSchema(
                nombre_completo="JUAN PEREZ",
                fecha_nacimiento="1975-04-12",
                numero_documento="MX-775533",
                nacionalidad="MEXICANA",
                tipo_documento="Pasaporte"
            )
            
        # Caso 2: Falso Positivo (Coincide nombre "JUAN PEREZ", cumpleaños difiere: 1980-05-15)
        elif "JUAN" in texto or "PEREZ" in texto or "SOSPECHOSO" in texto:
            return CompradorSchema(
                nombre_completo="JUAN PEREZ",
                fecha_nacimiento="1980-05-15",
                numero_documento="MX-998877",
                nacionalidad="MEXICANA",
                tipo_documento="Pasaporte"
            )
            
        # Caso 3: Transacción Válida limpia (Carlos Gómez, no coincide con sanciones)
        elif "VALIDO" in texto or "LIMPIO" in texto or "CARLOS" in texto:
            return CompradorSchema(
                nombre_completo="CARLOS GOMEZ",
                fecha_nacimiento="1990-08-20",
                numero_documento="MX-112233",
                nacionalidad="MEXICANA",
                tipo_documento="Pasaporte"
            )
            
        # Retorno base predeterminado si es otra entrada general
        return CompradorSchema(
            nombre_completo="CARLOS GOMEZ",
            fecha_nacimiento="1990-08-20",
            numero_documento="MX-112233",
            nacionalidad="MEXICANA",
            tipo_documento="Pasaporte"
        )

# Instancia global para importación simplificada
extractor_agent = ExtractorAgent()
