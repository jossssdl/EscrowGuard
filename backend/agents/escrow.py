# -*- coding: utf-8 -*-
"""
Orquestador de Flujo de Negocio y Grafo de Estados (LangGraph).
Desarrollado por el equipo Script Hunters.
Gestiona el ciclo de vida de la transacción de custodia en garantía.
"""

from typing import TypedDict, Dict, Any, List, Optional
from langgraph.graph import StateGraph, END
from agents.extractor import extractor_agent
from agents.osint import OSINTOchestrator
from services.bank_mock import BankEscrowService

# Definición del Estado de la Transacción en el Grafo
class EscrowState(TypedDict):
    transaction_id: Optional[str]
    monto: float
    comprador_data: Optional[Dict[str, Any]]
    resultado_osint: Optional[Dict[str, Any]]
    estado_transaccion: str  # PENDING, HELD, SANCTION_FLAGGED, APPROVED, REJECTED
    archivo_entrada: Optional[str]  # Nombre del archivo PDF o texto de entrada
    logs: List[str]

# Inicialización de servicios auxiliares locales
bank_service = BankEscrowService()
osint_orchestrator = OSINTOchestrator()

# Definición de los Nodos del Grafo

def nodo_extraccion(state: EscrowState) -> Dict[str, Any]:
    """
    Nodo de extracción de datos del comprador del pasaporte.
    """
    logs = list(state.get("logs", []))
    logs.append("Iniciando análisis de documento y extracción...")
    
    # Se recupera el archivo de entrada provisto, o se utiliza el caso por defecto
    archivo = state.get("archivo_entrada") or "Juan Pérez"
    logs.append(f"Leyendo documento: {archivo}")
    
    # Invocar al agente extractor de PydanticAI
    datos_comprador = extractor_agent.run_sync(archivo)
    
    logs.append(f"Datos extraídos con éxito: {datos_comprador.nombre_completo}")
    
    return {
        "comprador_data": datos_comprador.model_dump(),
        "logs": logs
    }

def nodo_deposito_preventivo(state: EscrowState) -> Dict[str, Any]:
    """
    Nodo que interactúa con el banco simulado para bloquear preventivamente los fondos.
    """
    logs = list(state.get("logs", []))
    logs.append("Solicitando retención preventiva de fondos al banco...")
    
    nombre_comprador = state["comprador_data"]["nombre_completo"] if state["comprador_data"] else "Desconocido"
    monto = state["monto"]
    
    # Llamar al servicio bancario
    transaccion = bank_service.crear_deposito(monto, nombre_comprador)
    
    logs.append(f"Fondos bloqueados. Transacción ID bancario: {transaccion['transaction_id']}")
    
    return {
        "transaction_id": transaccion["transaction_id"],
        "estado_transaccion": "HELD",
        "logs": logs
    }

def nodo_verificacion_osint(state: EscrowState) -> Dict[str, Any]:
    """
    Nodo de verificación del estatus del comprador en listas internacionales de sanciones.
    """
    logs = list(state.get("logs", []))
    logs.append("Iniciando cruce de información en listas de control OFAC y OSINT...")
    
    nombre_comprador = state["comprador_data"]["nombre_completo"]
    resultado = osint_orchestrator.analizar_perfil(nombre_comprador)
    
    logs.append("Cruce de listas finalizado.")
    
    # Guardamos los resultados
    return {
        "resultado_osint": resultado,
        "logs": logs
    }

def evaluador_de_riesgos(state: EscrowState) -> str:
    """
    Borde condicional que evalúa los riesgos del perfil para decidir la transición de estado.
    """
    resultado = state["resultado_osint"]
    comprador = state["comprador_data"]
    
    if resultado and resultado.get("tiene_alerta"):
        # Falso positivo inteligente: Comparar cumpleaños
        # Si el cumpleaños extraído del pasaporte coincide exactamente con el cumpleaños de la sanción,
        # la alerta es verdadera y se rechaza. Si no coinciden, se clasifica como coincidencia potencial
        # (falso positivo) y requiere intervención humana (HITL).
        fecha_pasaporte = comprador.get("fecha_nacimiento")
        fecha_sancion = resultado["sancion_data"].get("fecha_nacimiento")
        
        if fecha_pasaporte == fecha_sancion:
            # Los cumpleaños coinciden -> Rechazo directo (Riesgo Confirmado)
            return "rechazar"
        else:
            # El nombre coincide pero los cumpleaños no -> Coincidencia potencial / Falso Positivo -> HITL
            return "alerta_hitl"
            
    # Sin alertas de sanción -> Aprobación directa
    return "aprobar"

def nodo_alerta_sanccion(state: EscrowState) -> Dict[str, Any]:
    """
    Nodo al que transiciona el flujo cuando se detecta un posible falso positivo.
    """
    logs = list(state.get("logs", []))
    logs.append("⚠️ TRANSACCIÓN BLOQUEADA PREVENTIVAMENTE: Coincidencia potencial en lista de sanciones.")
    logs.append("Pausando ejecución de agentes. Esperando revisión interactiva por Oficial de Cumplimiento (DPO).")
    
    return {
        "estado_transaccion": "SANCTION_FLAGGED",
        "logs": logs
    }

def nodo_aprobado(state: EscrowState) -> Dict[str, Any]:
    """
    Nodo final que libera los fondos al vendedor tras validación exitosa.
    """
    logs = list(state.get("logs", []))
    tx_id = state["transaction_id"]
    
    # Liberamos en el banco
    bank_service.liberar_fondos(tx_id)
    logs.append(f"Fondos liberados para la transacción {tx_id}. Operación completada con éxito.")
    
    return {
        "estado_transaccion": "APPROVED",
        "logs": logs
    }

def nodo_rechazado(state: EscrowState) -> Dict[str, Any]:
    """
    Nodo final que reembolsa los fondos al comprador tras la denegación de la operación.
    """
    logs = list(state.get("logs", []))
    tx_id = state["transaction_id"]
    
    # Reembolsar fondos en el banco
    bank_service.reembolsar_fondos(tx_id)
    logs.append(f"⚠️ Fondos reembolsados y devueltos al comprador para la transacción {tx_id}. Operación denegada.")
    
    return {
        "estado_transaccion": "REJECTED",
        "logs": logs
    }

# Construcción e Hilado del Grafo de LangGraph
workflow = StateGraph(EscrowState)

# Agregar Nodos
workflow.add_node("extraer_documento", nodo_extraccion)
workflow.add_node("deposito_preventivo", nodo_deposito_preventivo)
workflow.add_node("verificar_osint", nodo_verificacion_osint)
workflow.add_node("alerta_sancion", nodo_alerta_sanccion)
workflow.add_node("aprobar_transaccion", nodo_aprobado)
workflow.add_node("rechazar_transaccion", nodo_rechazado)

# Definir Relaciones (Bordes)
workflow.set_entry_point("extraer_documento")
workflow.add_edge("extraer_documento", "deposito_preventivo")
workflow.add_edge("deposito_preventivo", "verificar_osint")

# Configurar el Borde Condicional desde la verificación OSINT
workflow.add_conditional_edges(
    "verificar_osint",
    evaluador_de_riesgos,
    {
        "aprobar": "aprobar_transaccion",
        "rechazar": "rechazar_transaccion",
        "alerta_hitl": "alerta_sancion"
    }
)

# Los nodos terminales conectan con el fin del grafo
workflow.add_edge("alerta_sancion", END)
workflow.add_edge("aprobar_transaccion", END)
workflow.add_edge("rechazar_transaccion", END)

# Compilación final del Grafo
escrow_flow = workflow.compile()
