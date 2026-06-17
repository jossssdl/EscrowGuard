# Especificación Técnica de Integración y API (Dev 1)

## 🏢 Script Hunters - EscrowGuard

Este documento detalla la especificación de integración técnica a cargo del **Dev 1**. Contempla la configuración de la API web con FastAPI, la conexión interactiva mediante el SDK de Band Pro y la articulación de la lógica de los agentes bajo el paradigma *Human-in-the-Loop* (HITL).

---

## 🛠️ Arquitectura de la Solución

El script principal `main.py` actúa como la pasarela central de comunicaciones de EscrowGuard, sirviendo a dos frentes principales:

```mermaid
graph LR
    subgraph Frontend (Simulador Web)
        UI[Landing Page / UI]
    end
    
    subgraph Backend Core (FastAPI)
        API[API Endpoints]
        Listener[EscrowRoomListener]
    end
    
    subgraph Sindicato de Agentes & Servicios
        LG[LangGraph Flow]
        Ext[Extractor PydanticAI]
        OS[OSINT CrewAI]
        Bank[Bank Mock Service]
    end
    
    subgraph Plataforma Externa
        Band[Band Pro SDK / Chat Room]
    end

    UI <-- HTTP / JSON --> API
    API --> LG
    Listener <-- WebSockets / Events --> Band
    Listener --> LG
    LG --> Ext
    LG --> OS
    LG --> Bank
```

---

## 🌐 Endpoints de la API de Simulación (FastAPI)

Para permitir que el simulador frontend envíe transacciones y visualice las transiciones del grafo de LangGraph en tiempo real, se define el siguiente endpoint:

### 📥 1. Simular Flujo de Custodia (`POST /api/simulate`)
* **Descripción:** Recibe la información simulada de un pasaporte (o un payload que represente los datos extraídos de un documento) e inicia el grafo orquestador de LangGraph.
* **Cuerpo de la Petición (JSON):**
  ```json
  {
    "transaction_id": "ESC-88741B",
    "monto": 5000000.00,
    "comprador": {
      "nombre_completo": "JUAN PEREZ",
      "fecha_nacimiento": "1980-05-15",
      "numero_documento": "MX-998877",
      "nacionalidad": "MEXICANA",
      "tipo_documento": "Pasaporte"
    }
  }
  ```
* **Respuesta Exitosa (200 OK):**
  ```json
  {
    "status": "success",
    "current_state": "SANCTION_FLAGGED",
    "message": "Alerta de cumplimiento detectada. El flujo requiere aprobación humana.",
    "transaction_details": {
      "transaction_id": "ESC-88741B",
      "monto_retenido": 5000000.00,
      "discrepancia_detectada": true
    }
  }
  ```

---

## 💬 Integración con Band Pro SDK

La interacción en tiempo real en la sala de chat del hackathon se gestiona heredando del listener base del SDK.

### Clase `EscrowRoomListener(RoomListener)`
Este módulo escucha los eventos del canal y realiza la siguiente secuencia de eventos al detectar un archivo PDF:

1. **Carga y Lectura del PDF:** Al detectar un adjunto en `message.attachments`, el listener descarga el archivo de forma temporal o simula su contenido si es una ejecución de prueba.
2. **Invocación del Agente Extractor:** Pasa el documento al agente extractor de PydanticAI para obtener la estructura JSON validada.
3. **Bloqueo Preventivo de Fondos:** Invoca el servicio del banco para realizar la retención en garantía e informa a la sala del identificador de custodia.
4. **Ejecución OSINT e Investigación OFAC:** Dispara al agente investigador para validar el nombre e identificar coincidencias en la base de datos simulada de la OFAC.
5. **Evaluación en LangGraph:** Ejecuta el grafo de estados. Si hay coincidencia de nombres con discrepancia en fecha de nacimiento, el estado transiciona a `SANCTION_FLAGGED`.
6. **HITL (Human-in-the-Loop):** El listener suspende el estado del grafo y emite un mensaje estructurado en Markdown al canal solicitando acción del oficial de cumplimiento.
7. **Resolución de Alerta:** Si un oficial de cumplimiento escribe `APROBAR` en el chat:
   - Se reanuda el grafo de LangGraph.
   - El estado de la transacción cambia a `APPROVED`.
   - Se invoca el método de liberación de fondos en el servicio bancario.
   - Se notifica el éxito de la transacción a la sala.

---

## ⚙️ Variables de Entorno Requeridas (`.env`)

Para la correcta ejecución del backend y su integración, se deben configurar las siguientes variables de entorno en el archivo `.env` del directorio `escrow-guard/`:

```bash
# Configuración del Servidor API
PORT=8000
HOST=0.0.0.0

# SDK de Band Pro
BAND_API_KEY=tu_api_key_de_band_pro
BAND_ROOM_ID=tu_room_id_de_la_sala

# Proveedores de Modelos de Lenguaje (LLM)
OPENAI_API_KEY=tu_openai_api_key
GEMINI_API_KEY=tu_gemini_api_key

# Configuración de Entorno
ENVIRONMENT=development
```
