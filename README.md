# EscrowGuard - Multi-Agent Compliance System for High-Value Escrows

## 🏢 Script Hunters - Hackathon Project (Band of Agents)

EscrowGuard is a multi-agent platform designed to mitigate and resolve the operational friction caused by false positives in regulatory compliance checks (OFAC, PEP, and Anti-Money Laundering) in high-value escrow financial transactions.

This repository separates the project into a clean **Frontend/Backend** architecture to support independent scaling, clear division of concerns, and production-ready deployments.

---

## 🛠️ Complete System Architecture

EscrowGuard integrates intelligent LLM agents, a secure state machine, mock banking services, and an interactive frontend dashboard into a unified, scalable ecosystem:

```mermaid
graph TD
    subgraph Frontend Client (SPA)
        UI[Landing Page & Dashboard]
        Engine[Sandbox Simulation Engine]
        Controller[JS API Orchestrator]
    end
    
    subgraph Backend Core (FastAPI Server)
        API[FastAPI REST Endpoints]
        Listener[EscrowRoomListener]
        Store[(In-Memory Session Store)]
    end
    
    subgraph Sindicato de Agentes & Servicios
        LG[LangGraph Orchestrator]
        Ext[Extractor Agent - PydanticAI]
        OS[OSINT Agent - CrewAI]
        Bank[SPEI / Escrow Bank Mock]
        DB[OFAC / PEP Sanctions DB]
    end
    
    subgraph Plataforma Externa
        Band[Band.ai SDK / Chat Room]
    end

    UI --> Engine
    UI --> Controller
    Controller <-- HTTP / CORS --> API
    API --> LG
    API <-- Read/Write --> Store
    Listener <-- WebSockets / Events --> Band
    Listener --> LG
    Listener <-- Read/Write --> Store
    
    LG --> Ext
    LG --> OS
    LG --> Bank
    OS --> DB
    
    classDef client fill:#4f46e5,stroke:#c0c1ff,stroke-width:2px,color:#fff;
    classDef server fill:#0f172a,stroke:#38bdf8,stroke-width:2px,color:#fff;
    classDef agents fill:#065f46,stroke:#34d399,stroke-width:2px,color:#fff;
    classDef ext fill:#78350f,stroke:#fbbf24,stroke-width:2px,color:#fff;
    
    class UI,Engine,Controller client;
    class API,Listener,Store server;
    class LG,Ext,OS,Bank,DB agents;
    class Band ext;
```

---

## 📁 Project Directory Structure

The workspace is organized to isolate the client application from backend processing, ensuring clean versioning and easy containerization:

```text
HACKATHON_BAND_OF_AGENTS/
├── docs/                               # Technical specifications for each role
│   ├── dev1_integration.md             # Integration & API Specification
│   ├── dev3_extractor_integration.md   # Extractor Agent Specification
│   └── dev6_frontend_simulator.md      # Frontend Simulator Specification
├── frontend/                           # Client-side web interface (Dev 6)
│   ├── index.html                      # UI Dashboard & Simulation layout
│   └── index.css                       # Refined Glassmorphic stylesheet
├── backend/                            # Python Backend Server
│   ├── agents/                         # Syndicate of intelligent agents
│   │   ├── __init__.py
│   │   ├── extractor.py                # Extractor Agent (PydanticAI - Dev 3)
│   │   ├── osint.py                    # OSINT / Investigator Agent (CrewAI - Dev 4)
│   │   └── escrow.py                   # State Graph Orchestrator (LangGraph - Dev 5)
│   ├── services/                       # Simulation services and mocks (Dev 2)
│   │   ├── __init__.py
│   │   ├── bank_mock.py                # Escrow bank mock service (SPEI/SAT)
│   │   └── sanction_mock.py            # OFAC sanctions database mock
│   ├── mock_docs/                      # Sample PDF test documents (Dev 2)
│   ├── .env.example                    # Template for environment variables
│   ├── requirements.txt                # Python backend dependencies
│   └── main.py                         # FastAPI REST API & Band.ai Listener (Dev 1)
├── LICENSE                             # MIT Distribution License
└── README.md                           # Main repository documentation
```

---

## 👤 Developer Roles and Deliverables

The EscrowGuard system was built collaboratively by dividing the deliverables across 6 specialized development roles:

### 🛠️ Dev 1: Integration, REST API & SDK Core
* **Core Responsibilities:**
  - Configured the **FastAPI** backend, enabling CORS for cross-origin frontend communication.
  - Implemented the `POST /api/simulate` and `GET /api/transaction/{id}` endpoints.
  - Connected the backend to the hackathon chat rooms via the **Band Pro SDK**, handling real-time messaging, file attachments, and human interactive DPO feedback.

### 💰 Dev 2: Mock Services & Document Assets
* **Core Responsibilities:**
  - Programmed the simulated banking backend (`bank_mock.py`) supporting deposit locks, refunds, and final releases.
  - Engineered the OFAC database mock (`sanction_mock.py`) that returns structured compliance flags.
  - Built sample identity documents (`cliente_limpio.pdf`, `empresa_fantasma.pdf`, `solicitud_sat.pdf`) for validation scenarios.

### 🔍 Dev 3: Compliance Extractor Agent
* **Core Responsibilities:**
  - Built the extractor agent wrapper utilizing **PydanticAI** to convert raw identity documentation text into structured `EntidadesExtraidas` data.
  - Implemented secure text parsing using **PyPDF2** with exception safety.
  - Created environment-tolerant key mapping (`GEMINI_API_KEY` to `GOOGLE_API_KEY`, etc.) and dummy fallbacks to ensure zero-crash startup behaviors.

### 🌐 Dev 4: OSINT Web Investigator Agent
* **Core Responsibilities:**
  - Configured the OSINT investigator role using **CrewAI** to perform search intelligence for adverse media, PEP checks, and general financial warnings.
  - Enabled multi-provider LLM support (Gemini, Groq, Grok) with automatic fallback.
  - Structured the final output into a rich Markdown report combining OFAC records and web search results.

### ⛓️ Dev 5: State Machine Orchestrator
* **Core Responsibilities:**
  - Designed the secure transition graph using **LangGraph** to link each step of the compliance verification flow.
  - Implemented nodes for: *Document Extraction*, *Preventive Hold*, *OSINT Search*, *DPO Gate*, and *Funds Execution*.
  - Configured the paused-state flow to support **Human-in-the-Loop (HITL)** approvals without blocking server threads.

### 🎨 Dev 6: Frontend Dashboard & Simulation UX
* **Core Responsibilities:**
  - Designed a premium glassmorphic Single Page Application (SPA) dashboard in HTML/CSS aligning with the Stitch Design System.
  - Built a dual-mode engine (Sandbox Client-side / Live API Backend-side) to allow testing under any network conditions.
  - Implemented drag-and-drop file detection, interactive SVG node flow status highlights, and modal prompt overlays for compliance officers.

---

## 📈 Scalability and Production Architecture

To scale EscrowGuard beyond hackathon environments:
1. **Separation of Concerns:** Frontend and backend reside in separate directories. The frontend can be distributed via static CDNs (Vercel, Netlify, Cloudflare), reducing hosting costs.
2. **Containerization & Cloud Native:** The `backend` directory can be containerized using Docker and deployed on serverless container services (like Google Cloud Run or AWS Fargate) to auto-scale horizontally.
3. **Queue-Based Orchestration:** For production high-traffic scenarios, the in-memory state store (`session_state_store`) can be replaced with a Redis cache, and LangGraph states can be serialized to a PostgreSQL database (using LangGraph persistence layers), enabling cluster-wide resilience.

---

## 🚀 Running & Verification Instructions

### 1. Backend Setup
1. Enter the `backend/` folder:
   ```bash
   cd backend
   ```
2. Configure your environment variables in `.env` based on `.env.example`.
3. Activate your virtual environment and install packages:
   ```bash
   source ../.venv/bin/activate
   pip install -r requirements.txt
   ```
4. Run the FastAPI server:
   ```bash
   python main.py
   ```

### 2. Frontend Setup
1. Enter the `frontend/` folder:
   ```bash
   cd frontend
   ```
2. Serve the static files using a local server (to avoid CORS blockages):
   ```bash
   python3 -m http.server 8080
   # or
   npx -y live-server
   ```
3. Open `http://localhost:8080` in your web browser. Toggle between **Sandbox** (local client simulator) and **Live API** (connected to the FastAPI backend) modes to test.
