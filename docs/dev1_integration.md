# Technical Specification for Integration and API (Dev 1)

## 🏢 Script Hunters - EscrowGuard

This document details the technical integration specifications managed by **Dev 1**. It covers the configuration of the web API using FastAPI, the real-time interaction through the Band Pro SDK, and the orchestration of the agent logic under the Human-in-the-Loop (HITL) paradigm.

---

## 🛠️ Solution Architecture

The main script `main.py` acts as the central communications gateway for EscrowGuard, serving two main interfaces:

```mermaid
graph LR
    subgraph Frontend (Web Simulator)
        UI[Landing Page / UI]
    end
    
    subgraph Backend Core (FastAPI)
        API[API Endpoints]
        Listener[EscrowRoomListener]
    end
    
    subgraph Agents Syndicate & Services
        LG[LangGraph Flow]
        Ext[Extractor PydanticAI]
        OS[OSINT CrewAI]
        Bank[Bank Mock Service]
    end
    
    subgraph External Platform
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

## 🌐 Simulation API Endpoints (FastAPI)

To allow the frontend simulator to trigger transactions and visualize the LangGraph transitions in real time, the following endpoints are defined:

### 📥 1. Simulate Escrow Flow (`POST /api/simulate`)
* **Description:** Receives the simulated passport metadata (or a payload representing extracted document data) and triggers the LangGraph orchestrator.
* **Request Body (JSON):**
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
    },
    "archivo_entrada": "pasaporte_sospechoso.pdf"
  }
  ```
* **Success Response (200 OK):**
  ```json
  {
    "status": "success",
    "transaction_id": "ESC-88741B",
    "estado_final": "SANCTION_FLAGGED",
    "logs": [
      "Iniciando análisis de documento y extracción...",
      "Leyendo documento: pasaporte_sospechoso.pdf",
      "Datos extraídos con éxito: JUAN PEREZ",
      "Solicitando retención preventiva de fondos al banco...",
      "Fondos bloqueados. Transacción ID bancario: ESC-88741B",
      "Iniciando cruce de información en listas de control OFAC y OSINT...",
      "Cruce de listas finalizado.",
      "⚠️ TRANSACCIÓN BLOQUEADA PREVENTIVAMENTE: Coincidencia potencial en lista de sanciones.",
      "Pausando ejecución de agentes. Esperando revisión interactiva por Oficial de Cumplimiento (DPO)."
    ],
    "comprador": {
      "nombre_completo": "JUAN PEREZ",
      "fecha_nacimiento": "1980-05-15",
      "numero_documento": "MX-998877",
      "nacionalidad": "MEXICANA",
      "tipo_documento": "Pasaporte"
    },
    "osint": {
      "tiene_alerta": true,
      "sancion_data": {
        "nombre_completo": "JUAN PEREZ",
        "fecha_nacimiento": "1975-04-12",
        "nacionalidad": "MEXICANA",
        "motivo": "Lavado de Dinero - Cartel de la Frontera",
        "gravedad": "ALTA"
      },
      "reporte_markdown": "### 🔍 Reporte de Investigación OSINT: JUAN PEREZ..."
    }
  }
  ```

---

## 💬 Band Pro SDK Integration

Real-time interaction inside the hackathon chat room is managed by extending the base listener class from the SDK.

### Class `EscrowRoomListener(RoomListener)`
This module listens for incoming channel events and executes the following logic upon detecting a PDF attachment:

1. **PDF Detection and Loading:** When a PDF attachment is detected in `message.attachments`, the listener downloads the file temporarily or passes its filename to the state machine for simulation.
2. **Extractor Agent Invocation:** Passes the file metadata to the PydanticAI extractor agent to retrieve the structured buyer schema.
3. **Preventive Escrow Hold:** Triggers the mock bank service to block the transaction amount and announces the escrow ID to the room.
4. **OSINT and OFAC Search:** Runs the investigator agent to crosscheck the buyer's name against the simulated OFAC sanctions database.
5. **LangGraph Evaluation:** Executes the state graph. If the buyer's name matches a record but birthdates differ, the state transitions to `SANCTION_FLAGGED`.
6. **HITL (Human-in-the-Loop) Interruption:** The listener pauses execution, caches the transaction ID, and broadcasts a markdown message to the room requesting human action.
7. **Alert Resolution:** If the Compliance Officer (DPO) types `APROBAR` (approve) or `RECHAZAR` (reject) in the chat:
   - The state machine resumes.
   - The transaction state is updated to `APPROVED` or `REJECTED`.
   - The mock bank service is instructed to release or refund the escrowed funds.
   - The final status is reported back to the room.

---

## ⚙️ Required Environment Variables (`.env`)

To run the backend service locally, the following environment variables must be defined in the `escrow-guard/.env` file:

```bash
# API Server Settings
PORT=8000
HOST=0.0.0.0

# Band Pro SDK Configs
BAND_API_KEY=your_band_api_key_here
BAND_ROOM_ID=your_room_id_here

# LLM Providers (Required by agents)
OPENAI_API_KEY=your_openai_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here

# Environment Settings
ENVIRONMENT=development
```
