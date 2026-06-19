¡Claro que sí! Con mucho gusto te ayudo a estructurar tu propio documento técnico basándome en el formato, el tono y la estructura de los ejemplos que me acabas de proporcionar.

Este documento reflejará tu contribución esencial en el proyecto (Dev 2 - Mock Services & Data Simulation), manteniendo la estética y el nivel de detalle técnico (Mocks, UIF, SAT, JSON responses, SPEI, etc.) de la serie `Script Hunters - EscrowGuard`.

Aquí tienes tu documento en formato Markdown (`.md`):

---

# Technical Specification for Mock Services & Compliance Data Simulation (Dev 2)

🏢 Script Hunters - EscrowGuard

This document details the technical specification for the Mock Services and Data Simulation phase of EscrowGuard. Developed by Dev 2, it outlines the implementation of the simulated national compliance databases (UIF/SAT), the Escrow Trust Fund (SPEI simulation), the creation of synthetic test documents (PDFs), and the JSON payload structures required for frontend and backend integration.

## 🛠️ Mock Services Architecture

The mock services reside in the `services/` directory. They are designed to simulate real-world financial infrastructure and national regulatory lists, allowing the AI agents and LangGraph state machine to perform complex compliance decisions without requiring expensive or restricted API access to real banking or government networks.

## 🇲🇽 National Compliance Engine (UIF/SAT Simulation)

The module `services/sanction_mock.py` contains the `consultar_listas_nacionales()` function, which acts as a simulated API for Mexico's primary regulatory bodies:

* **UIF (Unidad de Inteligencia Financiera):** Simulates the "Lista de Personas Bloqueadas" (Blocked Persons List) for money laundering and PEP (Politically Exposed Persons) scenarios.
* **SAT (Servicio de Administración Tributaria):** Simulates the "Artículo 69-B" list for EFOS (Empresas que Facturan Operaciones Simuladas - Phantom Companies).

### Matching Logic & Scenarios

The engine normalizes the input name (uppercase, stripped) and executes a cascading validation:

1. **Exact Match (The True Positive):**
* *Trigger:* "COMERCIALIZADORA FANTASMA SA DE CV"
* *Action:* Immediately blocks the transaction. Simulates a severe SAT Art. 69-B violation.


2. **Surname Homonym Match (The False Positive / Demo Case):**
* *Trigger:* Names sharing the exact surnames with a critical profile (e.g., "DAMIAN CRISTIAN AVILA DIRCIO" matching the surnames of the fictitious sanctioned profile "JOSÉ CRISTIAN AVILA DIRCIO").
* *Action:* Flags the transaction as `RETENIDO_EN_GARANTIA` and triggers the `POSIBLE_HOMONIMO_PEP` alert, forcing a Human-in-the-Loop (HITL) intervention by the Compliance Officer.


3. **Clean Record (The Safe Client):**
* *Trigger:* Any name not found in the database or without matching surnames (e.g., "EDMUNDO JIMENEZ FILOMENO").
* *Action:* Approves the transaction (`APROBADO`) with no alerts.



## 🏦 Escrow Trust Fund & SPEI Simulation

The module `services/bank_mock.py` acts as the financial vault holding the funds during the verification process. It simulates Mexico's SPEI (Sistema de Pagos Electrónicos Interbancarios) network.

### Core Functions

* `retener_fondos_fideicomiso(id_contrato, monto_mxn)`: Simulates the initial deposit. Generates a unique SPEI tracking key (`clave_rastreo_spei` starting with "BNX") and logically locks the funds in the `cuentas_puente_activas` dictionary with the state `FONDOS_ASEGURADOS_EN_FIDEICOMISO`.
* `liquidar_pago_vendedor(clave_rastreo)`: Triggered by the Compliance Officer (HITL) or an automatic clean scan. It transitions the fund state to `LIQUIDADO_AL_VENDEDOR` and outputs the final electronic payment receipt log.

## 📄 Synthetic Test Documents (mock_docs/)

To trigger the distinct flows, three precise PDF documents were crafted using authentic bureaucratic syntax and formatting to be processed by the Extractor Agent (PydanticAI):

1. `solicitud_sat_damian.pdf` **(The Demo Artifact):** A highly realistic written request (Escrito Libre) for SAT PAC authorization. It contains the name "DAMIAN CRISTIAN AVILA DIRCIO", deliberately designed to trigger the Homonym (False Positive) HITL flow.
2. `empresa_fantasma_sat.pdf` **(The Block Artifact):** Formatted as a "Constancia de Situación Fiscal" (Tax Situation Proof). Contains the exact string "COMERCIALIZADORA FANTASMA SA DE CV" to trigger an automatic rejection.
3. `ine_edmundo_jimenez.pdf` **(The Clean Artifact):** Formatted as a Mexican National Voter ID (INE). Contains a generic name and simulated CURP to test the frictionless approval path.

## 📦 JSON Payload Structures

The mock services return strict dictionary structures intended to be easily parsed by both the LangGraph state machine (Dev 5) and the Frontend Client (Dev 6).

**Approved Payload (Green State):**

```json
{
  "estado_pld": "APROBADO",
  "tipo_alerta": "NINGUNA",
  "detalles_institucion": null
}

```

**Retained / HITL Payload (Amber State - Demo):**

```json
{
  "estado_pld": "RETENIDO_EN_GARANTIA",
  "tipo_alerta": "POSIBLE_HOMONIMO_PEP",
  "detalles_institucion": {
    "institucion": "SISTEMA_INTERNO_ESCROWGUARD",
    "motivo": "Apellidos coinciden con entidad de alto riesgo (JOSÉ CRISTIAN AVILA DIRCIO).",
    "nivel_riesgo": "MEDIO",
    "accion_requerida": "REQUIERE_DESBLOQUEO_OFICIAL_CUMPLIMIENTO"
  }
}

```

**Blocked Payload (Red State):**

```json
{
  "estado_pld": "BLOQUEADO",
  "tipo_alerta": "COINCIDENCIA_EXACTA_UIF_SAT",
  "detalles_institucion": {
    "institucion": "SAT",
    "lista": "Articulo 69-B CFF (EFOS)",
    "motivo": "Facturacion de operaciones simuladas",
    "nivel_riesgo": "ALTO",
    "accion_requerida": "REVISION_MANUAL_REQUERIDA"
  }
}

```

## 🚀 Running & Verification Instructions

* **Execution:** These functions are passive and execute synchronously when called by the Agents or the FastAPI server.
* **Logging:** The modules utilize Python's built-in `logging` library, simulating terminal output for a PLD (Prevención de Lavado de Dinero) API and a Banxico Trust Fund to enhance the visual presentation of the backend execution logs.
