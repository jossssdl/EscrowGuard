# -*- coding: utf-8 -*-
"""
Servicio Principal de Backend y Pasarela de Integración - EscrowGuard.
Desarrollado por el equipo Script Hunters.
Integra la API FastAPI y la escucha en tiempo real de salas de Band Pro.
"""

import os
import uvicorn
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

# Carga de variables de entorno
load_dotenv()

# Intentar importar el SDK del Hackathon (Band Pro SDK)
# Si no está disponible en el entorno local, se provee una simulación para no interrumpir el desarrollo
try:
    from band_sdk import BandClient, RoomListener
except ImportError:
    # Definición de clases Mock para emular el SDK en local
    class Room:
        def __init__(self, room_id: str):
            self.room_id = room_id
        def send_message(self, text: str) -> None:
            print(f"[MOCK-ROOM-{self.room_id}] Enviando mensaje:\n{text}\n")

    class Message:
        def __init__(self, text: str, attachments: List[str] = None):
            self.text = text
            self.attachments = attachments or []

    class RoomListener:
        def on_message_received(self, room: Any, message: Any) -> None:
            pass

    class BandClient:
        def __init__(self, api_key: str):
            self.api_key = api_key
            print(f"[MOCK-SDK] Inicializado con clave API: {api_key[:4]}...")
        def register_room_listener(self, room_id: str, listener: RoomListener) -> None:
            print(f"[MOCK-SDK] Registrando listener en sala ID: {room_id}")

# Importación de los módulos del Sindicato de Agentes y Servicios
from agents.escrow import escrow_flow, bank_service, EscrowState

# Inicialización de la aplicación FastAPI
app = FastAPI(
    title="EscrowGuard - API de Integración",
    version="1.0.0",
    description="Backend unificado e integrador para el sindicato multiagente de EscrowGuard (Script Hunters)"
)

# Configuración de CORS para interconexión con el Simulador Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Modificar en producción según directivas de seguridad
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Modelos de Peticiones y Respuestas de la API ---

class CompradorInput(BaseModel):
    nombre_completo: str = Field(..., example="CARLOS AVILA DIRCIO")
    fecha_nacimiento: str = Field(..., example="1992-07-14")
    numero_documento: str = Field(..., example="MX-556677")
    nacionalidad: str = Field(..., example="MEXICANA")
    tipo_documento: str = Field(default="Pasaporte")

class SimularTransaccionInput(BaseModel):
    monto: float = Field(..., example=5000000.00)
    comprador: CompradorInput
    archivo_entrada: Optional[str] = Field(default=None, description="Nombre del archivo PDF simulado (ej: solicitud_sat.pdf)")

# Almacén local en memoria para mantener el estado actual de las simulaciones activas
# Clave: transaction_id, Valor: estado global del grafo
session_state_store: Dict[str, Dict[str, Any]] = {}

# --- Lógica de Integración de Band Pro SDK ---

class EscrowRoomListener(RoomListener):
    """
    Listener interactivo en tiempo real para eventos de salas de chat en Band Pro.
    """
    def __init__(self):
        super().__init__()
        self.transaccion_pendiente: Optional[str] = None  # Almacena el ID de transacción pausada para HITL

    def on_message_received(self, room: Any, message: Any) -> None:
        """
        Callback que se dispara al detectar un nuevo mensaje o archivo en la sala.
        """
        texto_mensaje = message.text.strip().upper()

        # Escucha de aprobación humana (Human-in-the-Loop)
        if self.transaccion_pendiente and (texto_mensaje == "APROBAR" or texto_mensaje == "RECHAZAR"):
            tx_id = self.transaccion_pendiente
            
            if texto_mensaje == "APROBAR":
                # Liberación de fondos a nivel bancario simulado
                exito = bank_service.liberar_fondos(tx_id)
                if exito:
                    room.send_message(
                        f"✅ **DECISIÓN REGISTRADA (DPO):** Transacción `{tx_id}` aprobada.\n"
                        f"Los fondos de garantía de custodia han sido liberados inmediatamente al vendedor.\n"
                        f"**Estatus actual:** Completada."
                    )
                    # Sincronizar con el almacén de sesiones
                    if tx_id in session_state_store:
                        session_state_store[tx_id]["estado_transaccion"] = "APPROVED"
                        session_state_store[tx_id]["logs"].append("👨‍⚖️ [DPO Chat] Decisión de cumplimiento recibida: APROBAR")
                        session_state_store[tx_id]["logs"].append(f"✅ Fondos liberados para la transacción {tx_id}. Operación completada con éxito.")
                else:
                    room.send_message(f"⚠️ Error al intentar liberar los fondos para `{tx_id}`.")
            else:
                # Reembolso de fondos
                exito = bank_service.reembolsar_fondos(tx_id)
                if exito:
                    room.send_message(
                        f"🚨 **DECISIÓN REGISTRADA (DPO):** Transacción `{tx_id}` rechazada.\n"
                        f"Los fondos han sido devueltos a la cuenta origen del comprador preventivamente.\n"
                        f"**Estatus actual:** Cancelada."
                    )
                    # Sincronizar con el almacén de sesiones
                    if tx_id in session_state_store:
                        session_state_store[tx_id]["estado_transaccion"] = "REJECTED"
                        session_state_store[tx_id]["logs"].append("👨‍⚖️ [DPO Chat] Decisión de cumplimiento recibida: RECHAZAR")
                        session_state_store[tx_id]["logs"].append(f"🚨 Fondos reembolsados y devueltos al comprador para la transacción {tx_id}. Operación denegada.")
                else:
                    room.send_message(f"⚠️ Error al intentar reembolsar los fondos para `{tx_id}`.")
            
            # Limpiar estado pendiente
            self.transaccion_pendiente = None
            return

        # Detección de archivos adjuntos (Pasaportes en PDF)
        if hasattr(message, 'attachments') and message.attachments:
            for adjunto in message.attachments:
                if adjunto.endswith(".pdf"):
                    room.send_message(
                        f"📥 **DOCUMENTO DETECTADO:** Iniciando análisis del pasaporte adjunto...\n"
                        f"Invocando al sindicato de agentes de **EscrowGuard**."
                    )
                    
                    # Simulación del disparo del grafo
                    # Inicializamos un estado inicial pasando el nombre del archivo PDF detectado en el adjunto
                    estado_inicial = EscrowState(
                        transaction_id=None,
                        monto=5000000.00,
                        comprador_data=None,
                        resultado_osint=None,
                        estado_transaccion="PENDING",
                        archivo_entrada=adjunto,
                        logs=[]
                    )
                    
                    try:
                        # Invocar el grafo compilado de LangGraph
                        resultado = escrow_flow.invoke(estado_inicial)
                        tx_id = resultado.get("transaction_id")
                        estado_final = resultado.get("estado_transaccion")
                        
                        # Guardamos el resultado en la caché de sesiones
                        if tx_id:
                            session_state_store[tx_id] = resultado
                        
                        # Reportar logs al chat de la sala
                        reporte_logs = "\n".join([f"- {log}" for log in resultado.get("logs", [])])
                        room.send_message(f"⚙️ **Logs de Procesamiento:**\n{reporte_logs}")
                        
                        # Si requiere intervención humana por posible coincidencia de nombre (falso positivo)
                        if estado_final == "SANCTION_FLAGGED":
                            self.transaccion_pendiente = tx_id
                            
                            # Obtener reporte OSINT
                            reporte_osint = resultado["resultado_osint"]["reporte_markdown"]
                            
                            room.send_message(
                                f"🚨 **ALERTA DE CUMPLIMIENTO:** Se ha detectado un posible Falso Positivo.\n"
                                f"{reporte_osint}\n\n"
                                f"🧑‍⚖️ **Oficial de Cumplimiento (DPO):** Responda a este mensaje escribiendo:\n"
                                f"- **`APROBAR`** para liberar los fondos y finalizar la transacción.\n"
                                f"- **`RECHAZAR`** para anular la transacción y reembolsar al comprador."
                            )
                        elif estado_final == "APPROVED":
                            room.send_message(f"✅ Transacción `{tx_id}` procesada y aprobada automáticamente.")
                        elif estado_final == "REJECTED":
                            room.send_message(f"🚨 Transacción `{tx_id}` rechazada automáticamente debido a riesgo confirmado.")
                            
                    except Exception as e:
                        room.send_message(f"❌ **FALLO CRÍTICO:** Ocurrió un error en el motor de ejecución: {str(e)}")

# --- Endpoints de FastAPI ---

@app.post("/api/simulate", response_model=Dict[str, Any])
def simular_transaccion(input_data: SimularTransaccionInput):
    """
    Endpoint HTTP que permite simular la ejecución del flujo completo del grafo de estados.
    Es utilizado directamente por el dashboard del Simulador Frontend.
    """
    # Construcción del estado inicial a partir de los datos recibidos en la petición HTTP
    # Si se provee archivo_entrada, este definirá el perfil simulado por el extractor
    estado_inicial = EscrowState(
        transaction_id=None,
        monto=input_data.monto,
        comprador_data=input_data.comprador.model_dump(),
        resultado_osint=None,
        estado_transaccion="PENDING",
        archivo_entrada=input_data.archivo_entrada,
        logs=[]
    )
    
    try:
        # Invocar la máquina de estados de LangGraph de manera síncrona
        resultado = escrow_flow.invoke(estado_inicial)
        tx_id = resultado.get("transaction_id")
        
        # Almacenamiento local del estado resultante
        if tx_id:
            session_state_store[tx_id] = resultado
            
        return {
            "status": "success",
            "transaction_id": tx_id,
            "estado_final": resultado.get("estado_transaccion"),
            "logs": resultado.get("logs", []),
            "comprador": resultado.get("comprador_data"),
            "osint": resultado.get("resultado_osint")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar la simulación: {str(e)}")


@app.get("/api/transaction/{transaction_id}", response_model=Dict[str, Any])
def obtener_estado_transaccion(transaction_id: str):
    """
    Recupera el estado actual de una transacción específica en memoria.
    """
    transaccion = session_state_store.get(transaction_id)
    if not transaccion:
        # Intentar buscar en el banco mock como plan de contingencia
        deposito = bank_service.obtener_deposito(transaction_id)
        if deposito:
            return {
                "transaction_id": transaction_id,
                "estado_transaccion": deposito["estado"],
                "logs": ["Recuperado del registro bancario histórico."],
                "comprador_data": {"nombre_completo": deposito["comprador"]}
            }
        raise HTTPException(status_code=404, detail="Transacción no encontrada.")
        
    return transaccion


class ResolveTransactionInput(BaseModel):
    decision: str = Field(..., example="APROBAR", description="La decisión del Oficial de Cumplimiento (DPO): APROBAR o RECHAZAR")

@app.post("/api/transaction/{transaction_id}/resolve", response_model=Dict[str, Any])
def resolver_transaccion(transaction_id: str, input_data: ResolveTransactionInput):
    """
    Registra la decisión manual del Oficial de Cumplimiento (DPO) en el backend.
    """
    transaccion = session_state_store.get(transaction_id)
    if not transaccion:
        raise HTTPException(status_code=404, detail="Transacción no encontrada.")
        
    decision = input_data.decision.upper().strip()
    if decision not in ["APROBAR", "RECHAZAR"]:
        raise HTTPException(status_code=400, detail="Decisión no válida. Debe ser 'APROBAR' o 'RECHAZAR'.")
        
    logs = list(transaccion.get("logs", []))
    logs.append(f"👨‍⚖️ [DPO Portal] Decisión de cumplimiento recibida: {decision}")
    
    if decision == "APROBAR":
        exito = bank_service.liberar_fondos(transaction_id)
        if not exito:
            raise HTTPException(status_code=500, detail="Error al liberar los fondos en el banco.")
        transaccion["estado_transaccion"] = "APPROVED"
        logs.append(f"✅ Fondos liberados para la transacción {transaction_id}. Operación completada con éxito.")
    else:
        exito = bank_service.reembolsar_fondos(transaction_id)
        if not exito:
            raise HTTPException(status_code=500, detail="Error al reembolsar los fondos en el banco.")
        transaccion["estado_transaccion"] = "REJECTED"
        logs.append(f"🚨 Fondos reembolsados y devueltos al comprador para la transacción {transaction_id}. Operación denegada.")
        
    transaccion["logs"] = logs
    session_state_store[transaction_id] = transaccion
    
    return {
        "status": "success",
        "transaction_id": transaction_id,
        "estado_final": transaccion["estado_transaccion"],
        "logs": transaccion["logs"],
        "comprador": transaccion.get("comprador_data"),
        "osint": transaccion.get("resultado_osint")
    }


# --- Bloque de Inicio de la Aplicación ---

def iniciar_servicios():
    """
    Configura e inicializa la API y el SDK Listener.
    """
    api_key = os.getenv("BAND_API_KEY", "mock_key")
    room_id = os.getenv("BAND_ROOM_ID", "mock_room")
    
    # Inicializar cliente SDK de Band Pro
    client = BandClient(api_key=api_key)
    listener = EscrowRoomListener()
    client.register_room_listener(room_id=room_id, listener=listener)

if __name__ == "__main__":
    # Iniciar conexión en segundo plano con el SDK del Hackathon
    iniciar_servicios()
    
    # Iniciar servidor web FastAPI en el puerto configurado
    puerto = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    uvicorn.run(app, host=host, port=puerto)
